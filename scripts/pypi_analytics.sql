CREATE EXTERNAL TABLE IF NOT EXISTS aialliance.pypi(
	with_mirrors_downloads		double,
	without_mirrors_downloads   double
)
partitioned by (project string, `date` date)
STORED AS PARQUET
LOCATION "s3://<bucket>/service=pypi";