import pypistats
from time import sleep
from os import getenv, makedirs, remove, listdir, rmdir
from os.path import join, exists
from datetime import datetime, timedelta
import pandas as pd
import boto3  # For S3 interaction

# Ensure pyarrow is installed for to_parquet: pip install pyarrow pandas boto3 pypistats

# --- Configuration from Environment Variables ---
projects_str = getenv("PROJECTS")
if not projects_str:
    print("Error: PROJECTS environment variable not set.")
    exit(1)
projects = projects_str.lower().split(",")

cool_off_s_str = getenv("COOL_OFF_S", "1")  # Default to 1 second if not set
try:
    cool_off_s = int(cool_off_s_str)
except ValueError:
    print(
        f"Warning: Invalid COOL_OFF_S value '{cool_off_s_str}'. Defaulting to 1 second."
    )
    cool_off_s = 1

full_hx = getenv("LOAD_FULL_HX", "false").lower() == "true"  # Default to false
aws_s3_bucket = getenv("AWS_S3_BUCKET")

if not aws_s3_bucket:
    print("Error: AWS_S3_BUCKET environment variable not set.")
    exit(1)

# --- Initialize S3 Client ---
try:
    s3_client = boto3.client("s3")
except Exception as e:
    print(
        f"Error initializing S3 client: {e}. Ensure AWS credentials and region are configured."
    )
    exit(1)

# --- Determine Date for 'Recent Data Only' ---
yesterday = datetime.now().date() - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")

# --- Temporary local storage for Parquet files ---
TEMP_DIR = "temp_data_pypi"
if not exists(TEMP_DIR):
    makedirs(TEMP_DIR)
    print(f"Created temporary directory: {TEMP_DIR}")

# --- Main Processing Loop ---
for project in projects:
    project = project.strip()
    if not project:
        continue

    raw_data_from_pypi = None
    print(f"Processing project: {project}")

    if full_hx:
        print(f"  Mode: Loading Full History")
        try:
            raw_data_from_pypi = pypistats.overall(
                project, total="daily", format="pandas"
            )
        except Exception as e:
            print(f"  Error fetching full history for {project}: {e}")
            if cool_off_s > 0:
                sleep(cool_off_s)
            continue
    else:
        print(f"  Mode: Loading Recent Data Only (for {yesterday_str})")
        try:
            raw_data_from_pypi = pypistats.overall(
                project,
                total="daily",
                format="pandas",
                start_date=yesterday_str,
                end_date=yesterday_str,
            )
        except Exception as e:
            print(f"  Error fetching recent data for {project} on {yesterday_str}: {e}")
            if cool_off_s > 0:
                sleep(cool_off_s)
            continue

    if raw_data_from_pypi is None:
        print(f"  No data fetched for {project}. Skipping.")
        if cool_off_s > 0:
            sleep(cool_off_s)
        continue

    if raw_data_from_pypi.empty:
        print(f"  No data found for {project} (DataFrame is empty).")
        if cool_off_s > 0:
            sleep(cool_off_s)
        continue

    print(f"  Raw data for {project} (first 5 rows):\n{raw_data_from_pypi.head()}")
    print(
        f"  Initial index type: {type(raw_data_from_pypi.index)}, Initial columns: {raw_data_from_pypi.columns.tolist()}"
    )

    # --- Step 1: Data Transformation - Pivot to get category-specific download columns ---
    data_for_output = None
    try:
        required_cols_for_pivot = ["date", "category", "downloads"]
        if not all(
            col in raw_data_from_pypi.columns for col in required_cols_for_pivot
        ):
            # Handle cases where data might not have 'category' (e.g., already daily totals)
            # This fallback logic attempts to create a 'total_downloads' column.
            print(
                f"  WARN: Missing columns for pivot ({[c for c in required_cols_for_pivot if c not in raw_data_from_pypi.columns]}). Attempting to process as daily totals."
            )
            if (
                "date" in raw_data_from_pypi.columns
                and "downloads" in raw_data_from_pypi.columns
            ):
                # Convert 'date' to datetime and set as PeriodIndex, then sum downloads if multiple rows per date
                temp_df = raw_data_from_pypi.copy()
                temp_df["date"] = pd.to_datetime(temp_df["date"])
                # Group by date and sum downloads, in case there are multiple rows for the same date without category
                # For instance, if the original data was already pivoted but lost its PeriodIndex.
                if (
                    isinstance(temp_df.index, pd.RangeIndex)
                    and not temp_df.groupby("date").size().gt(1).any()
                ):
                    # If RangeIndex and no duplicate dates, assume it's simple daily data
                    temp_df = temp_df.set_index("date")
                else:  # Otherwise, group and sum
                    temp_df = temp_df.groupby("date")["downloads"].sum().to_frame()

                temp_df.index = pd.PeriodIndex(temp_df.index, freq="D", name="date")
                data_for_output = temp_df.rename(
                    columns={"downloads": "total_downloads"}
                )
                print(
                    f"    Processed as daily totals. Columns: {data_for_output.columns.tolist()}"
                )
            else:
                raise ValueError(
                    "Data is missing 'date' or 'downloads' column and cannot be processed as daily totals."
                )
        else:
            # Proceed with pivoting
            print(
                f"  Pivoting data for {project} to get downloads by category per day..."
            )
            # Ensure 'date' column is in datetime format for pivot_table's index
            # Use a copy to avoid SettingWithCopyWarning if raw_data_from_pypi is a slice
            df_to_pivot = raw_data_from_pypi.copy()
            df_to_pivot["date_dt"] = pd.to_datetime(df_to_pivot["date"])

            pivoted_df = df_to_pivot.pivot_table(
                index="date_dt",  # Use the datetime-converted date column
                columns="category",  # Unique values from 'category' become new columns
                values="downloads",  # Populate with 'downloads' values
                # NaNs will be used if a category is missing for a date
            )

            # Convert the DatetimeIndex to PeriodIndex 'D' and explicitly name it 'date'
            pivoted_df.index = pd.PeriodIndex(pivoted_df.index, freq="D", name="date")

            # Rename columns to a standard format: category_name_downloads
            pivoted_df.columns = [
                f"{str(col).replace(' ', '_').lower()}_downloads"
                for col in pivoted_df.columns
            ]
            data_for_output = pivoted_df

        if data_for_output is not None and not data_for_output.empty:
            print(
                f"  Transformation complete. Resulting columns: {data_for_output.columns.tolist()}"
            )
            print(f"  Transformed data head:\n{data_for_output.head()}")
        else:
            print(f"  WARN: Data for {project} is empty after transformation attempt.")

    except Exception as e:
        print(f"  ERROR: Failed to transform data for {project}: {e}")
        print(
            f"    Original DataFrame columns: {raw_data_from_pypi.columns.tolist()}, Index: {type(raw_data_from_pypi.index)}"
        )
        print(f"    Original DataFrame head:\n{raw_data_from_pypi.head()}")
        if cool_off_s > 0:
            sleep(cool_off_s)
        continue  # Skip to next project

    if (
        data_for_output is None or data_for_output.empty
    ):  # Check again after transformation block
        print(f"  No data available for {project} after transformation. Skipping.")
        if cool_off_s > 0:
            sleep(cool_off_s)
        continue

    # --- Step 2: Iterate, save each day to a separate Parquet file, and upload to S3 ---
    print(
        f"  Processing {len(data_for_output)} date(s) for {project} for Parquet conversion and S3 upload..."
    )
    files_to_upload = []

    for date_period_obj, row_data in data_for_output.iterrows():
        try:
            # date_period_obj is a pandas.Period object from the pivoted DataFrame's index
            current_date_str = date_period_obj.strftime("%Y-%m-%d")
        except (
            AttributeError
        ):  # Should not happen if pivot and index conversion succeeded
            print(
                f"    Internal Error: Index item for {project} is not a Period object: {date_period_obj} (Type: {type(date_period_obj)}). Skipping this row."
            )
            continue

        # row_data is a Series. Convert it to a DataFrame for saving.
        # Its index will be the column names from data_for_output (e.g., 'with_mirrors_downloads').
        # The index of single_day_df will be the date_period_obj.
        single_day_df = pd.DataFrame([row_data])
        single_day_df.columns = [
            str(col) for col in single_day_df.columns
        ]  # Ensure column names are strings

        local_parquet_path = join(TEMP_DIR, f"{project}_{current_date_str}.parquet")

        try:
            # index=True saves the PeriodIndex (the date) into the Parquet file.
            single_day_df.to_parquet(local_parquet_path, engine="pyarrow", index=True)
            files_to_upload.append(
                {
                    "local_path": local_parquet_path,
                    "date_str": current_date_str,
                    "project": project,
                }
            )
        except Exception as e:
            print(f"    Error writing Parquet for {project} on {current_date_str}: {e}")
            if exists(local_parquet_path):
                try:
                    remove(local_parquet_path)
                except Exception as rem_e:
                    print(
                        f"      Could not remove partially written file {local_parquet_path}: {rem_e}"
                    )

    # Upload generated Parquet files to S3
    for item in files_to_upload:
        local_path = item["local_path"]
        file_date_str = item["date_str"]
        file_project = item["project"]

        s3_key = (
            f"service=pypi/project={file_project}/date={file_date_str}/blob.parquet"
        )

        try:
            s3_client.upload_file(local_path, aws_s3_bucket, s3_key)
            print(
                f"    Successfully uploaded {file_project} for {file_date_str} to s3://{aws_s3_bucket}/{s3_key}"
            )
            remove(local_path)
        except boto3.exceptions.S3UploadFailedError as e:
            print(f"    Error uploading {local_path} to S3: {e}")
        except Exception as e:  # Catch broader exceptions for S3 or local file removal
            print(
                f"    An unexpected error occurred during S3 upload or cleanup for {local_path}: {e}"
            )

    if cool_off_s > 0 and len(projects) > 1:  # Only cool off if there are more projects
        print(f"  Cooling off for {cool_off_s}s after processing {project}...")
        sleep(cool_off_s)

print("All projects processed.")

# Optional: Clean up the temp directory if it's empty or only contains hidden files
try:
    if exists(TEMP_DIR):
        if not listdir(TEMP_DIR) or all(p.startswith(".") for p in listdir(TEMP_DIR)):
            rmdir(TEMP_DIR)
            print(f"Removed empty temporary directory: {TEMP_DIR}")
        else:
            print(f"Temporary directory {TEMP_DIR} is not empty. Skipping removal.")
except OSError as e:
    print(
        f"Could not remove temporary directory {TEMP_DIR} (it might not be empty or access denied): {e}"
    )
