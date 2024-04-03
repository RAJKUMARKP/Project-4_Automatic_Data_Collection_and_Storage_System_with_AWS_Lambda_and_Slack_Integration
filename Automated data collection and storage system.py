import json
import requests
import psycopg2
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import urllib3

def post_slack_message(webhook_url, message):
    client = WebClient()
    try:
        response = client.chat_postMessage(
            channel="data-engineering",
            text=message
        )
        return response
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")
        return None

def lambda_handler(event, context):
    url = "http://api.open-notify.org/iss-now.json"
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "en-GB,en;q=0.5",
               "Connection": "keep-alive",
               "Host": "api.open-notify.org",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"}
    response = requests.get(url, verify=False, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.content)
        latitude = data["iss_position"]["latitude"]
        longitude = data["iss_position"]["longitude"]
        timestamp = data["timestamp"]
        message = data["message"]

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host='database-1.c1m4s2ueijsg.us-east-1.rds.amazonaws.com',
            port = 5432,
            user='myusername',
            password='Ramkumar123!',
            database='mydb'
        )

        try:
            cursor = conn.cursor()
            # Insert the data into the PostgreSQL table
            sql = "INSERT INTO iss_position(latitude, longitude, timestamp, message) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (latitude, longitude, timestamp, message))
            conn.commit()

            return {
                "statusCode": 200,
                "body": "Data inserted successfully into the PostgreSQL database"
            }
        except Exception as e:
            webhook_url = "https://hooks.slack.com/services/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"
            slack_message = "Error occurred while inserting data into the PostgreSQL database: " + str(e)
            post_slack_message(webhook_url, slack_message)
            
            return {
                "statusCode": 500,
                "body": "Error occurred while inserting data into the PostgreSQL database: " + str(e)
            }
        finally:
            conn.close()
    else:
        webhook_url = "https://hooks.slack.com/services/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"
        slack_message = "Error occurred: " + str(response.status_code)
        post_slack_message(webhook_url, slack_message)
        
        return {
            "statusCode": response.status_code,
            "body": "Error occurred: " + str(response.status_code)
        }