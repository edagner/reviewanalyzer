# reviewanalyzer

ETL system built on AWS infrastructure to apply sentiment scores to Amazon product reviews

## Process Overview
![ArchDoc](/images/ReviewAnalyzer.jpg)

## How to initialize
```
nohup python review_analyzer.py > /dev/null
```

## How to set up AWS

### EC2 Postgres DB

1. Launch an instance and choose the Ubuntu Server 18.04 AMI 
2. Choose t2.micro
3. Skip Configure details
4. Add 20gb to root volume
5. Add tag; name: DB Server
6. Create new Security Group and add SSH type with source being restricted to your IP address
7. Install PostgresSQL

### SQS Job Queue

1. Create New Queue
2. Choose standard queue. Unfortunately, this is the only choice if you want to be able to set up event notifications from S3. Duplicate messages have to be handled within the application.
3. Set Default Visibility Timeout to 5 minutes

### S3 

1. Create bucket
2. Choose a bucket name and region
3. Skip configure details
4. Keep public access blocked
5. Create folder named upload. New objects created in this folder will trigger a new message in SQS.
6. Go to properties and click events
7. Click Add Notification
   1. Name the notification
   2. Choose All object create events under Events
   3. Enter in /uploads as Prefix
   4. Choose your newly created SQS queue under Send To