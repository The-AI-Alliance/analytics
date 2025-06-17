drop table aialliance.membership

CREATE EXTERNAL TABLE IF NOT EXISTS aialliance.membership(
	member string,
    type string,
    geography string,
    country string,
    state string,   
    city string,
    date_created string)
partitioned by (`date` date)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
LOCATION "<s3 bucket>"
TBLPROPERTIES ('skip.header.line.count'='1')

MSCK REPAIR TABLE aialliance.membership

create view aialliance.v_membership as
select * from aialliance.membership where date in (select max(date) from aialliance.membership)

select * from aialliance.v_membership
select * from aialliance.membership