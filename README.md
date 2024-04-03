# Project-4_Automatic_Data_Collection_and_Storage_System_with_AWS_Lambda_and_Slack_Integration

Title: Designing an Automatic Data Collection and Storage System with AWS Lambda and Slack Integration for Server Availability Monitoring and Slack Notification

**Goal:**
To create an AWS Lambda function that will periodically fetch data from an API and store it in an Amazon RDS instance. The function should be triggered by an Amazon CloudWatch Event that occurs every 15 seconds.

**Technologies used:**
    Language - Python
    AWS services - AWS Lambda, AWS CloudWatch, AWS SNS, AWS RDS
    Slack - Slack API, Slack Workspace

**Steps:**
**fetch data**
1. Create a Lambda function that fetches data from the specified API and inserts it into a PostgreSQL database.
2. Download and include the required packages (requests and psycopg2) in the Lambda layer.
3. Handle the API request, extract relevant data, and establish a connection to the PostgreSQL database.
4. Insert the retrieved data into the "iss-position" table.
5. Return a success response if the server status_code is "200", otherwise send a failure slack message.

**Slack integration:**
For integrating slack, the following steps were followed
1.	Create a new slack App
2.	Add basic functionality and install the App 
3.	Copy the webhook URL and integrate it with the lambda function
4.	Your setup is done and the slack Api will launch your project with specific channel for automated message receipt
5.	For this project we have setup the slack Api as to receive error messages if the given URL is not accessible.

**SNS Topic:**
Create an SNS topic that triggers Lambda-function for Slack notifications.

**CloudWatch Alarm:**
1. Create a CloudWatch alarm that triggers based on Lambda-function failure.
2. Select the appropriate Lambda metric and set the threshold value.
3. Add the SNS topic to the alarm configuration.
    
**Testing:**
1. Manually modify the code in Lambda-function to simulate a server failure.
2. The failure triggers the CloudWatch alarm, which in turn triggers Lambda-function to send a Slack notification.
