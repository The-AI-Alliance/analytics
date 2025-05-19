drop table aialliance.github_analytics

/* Table definition */
CREATE EXTERNAL TABLE IF NOT EXISTS aialliance.github_analytics(
	timestamp_utc timestamp,
	repository_name string,
    stars int,
    watchers int,
    forks_total int,
    open_issues_total int,   
    network_count int,
    size_kb int,
    language string,
    created_at_utc timestamp,
    pushed_at_utc timestamp,
    archived boolean,
    disabled boolean,        
    has_issues boolean,
    has_projects boolean,   
    has_wiki boolean,
    has_pages boolean,
    has_downloads boolean,
    has_discussions boolean,
    license string,
    contributors_count_total int,
    releases_count_tota int,
    forks_new_last_period int,
    contributors_additions_recent_weeks int,
    traffic_views_last_day_total int,
    traffic_views_last_day_unique int,
    traffic_clones_last_day_total int,
    traffic_clones_last_day_unique int,
    traffic_top_referrers_date ARRAY <string>,
    /*traffic_top_paths_data ARRAY <string>, https://github.com/The-AI-Alliance/gofannon/issues/289 */
    issues_opened_last_period int,
    issues_closed_last_period int,
    prs_opened_last_period int,
    prs_closed_last_period int,
    prs_merged_last_period int,
    issue_comments_last_period int,
    pr_comments_last_period int,
    discussions_opened_last_period int,
    discussions_comments_last_period int
)
partitioned by (service string, repository string, `date` date)
STORED AS PARQUET
LOCATION "s3://<bucket>/service=github/"


/* Need to execute this to process new partitions*/
MSCK REPAIR TABLE aialliance.github_analytics

/* Test */
select * from aialliance.github_analytics order by timestamp_utc desc