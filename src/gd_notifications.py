import os
import json
import urllib.request
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta, timezone

def format_game_data(game):
    status = game.get("Status", "Unknown")
    away_team = game.get("AwayTeam", "Unknown")
    home_team = game.get("HomeTeam", "Unknown")
    final_score = f"{game.get('AwayTeamScore', 'N/A')}-{game.get('HomeTeamScore', 'N/A')}"
    start_time = game.get("DateTime", "Unknown")
    channel = game.get("Channel", "Unknown")
    
    # Format quarters
    quarters = game.get("Quarters", [])
    quarter_scores = ', '.join([f"Q{q['Number']}: {q.get('AwayScore', 'N/A')}-{q.get('HomeScore', 'N/A')}" for q in quarters])
    
    if status == "Final":
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Final Score: {final_score}\n"
            f"Start Time: {start_time}\n"
            f"Channel: {channel}\n"
            f"Quarter Scores: {quarter_scores}\n"
        )
    elif status == "InProgress":
        last_play = game.get("LastPlay", "N/A")
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Current Score: {final_score}\n"
            f"Last Play: {last_play}\n"
            f"Channel: {channel}\n"
        )
    elif status == "Scheduled":
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Start Time: {start_time}\n"
            f"Channel: {channel}\n"
        )
    else:
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Details are unavailable at the moment.\n"
        )

class AWSServices:
    def __init__(self):
        # Initialize AWS services with default config
        self.sns = boto3.client('sns')
        self.ssm = boto3.client('ssm')
        
    def get_secret(self, parameter_name):
        """Retrieve a secret from Parameter Store"""
        try:
            response = self.ssm.get_parameter(
                Name=parameter_name,
                WithDecryption=True
            )
            return response['Parameter']['Value']
        except ClientError as e:
            print(f"Error retrieving parameter {parameter_name}: {e}")
            raise
            
    def publish_sns_message(self, topic_arn, message, subject):
        """Publish a message to SNS with error handling"""
        try:
            response = self.sns.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=subject
            )
            print(f"Message published successfully. MessageId: {response['MessageId']}")
            return response
        except ClientError as e:
            print(f"Error publishing to SNS: {e}")
            raise

def fetch_nba_data(api_url):
    """Fetch NBA data with error handling"""
    try:
        with urllib.request.urlopen(api_url) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        print(f"URLError: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error fetching NBA data: {e}")
        raise

def lambda_handler(event, context):
    try:
        # Initialize AWS services
        aws = AWSServices()
        
        # Get configuration from environment or Parameter Store
        api_key = os.getenv("NBA_API_KEY") or aws.get_secret("/nba/api-key")
        sns_topic_arn = os.getenv("SNS_TOPIC_ARN") or aws.get_secret("/nba/sns-topic-arn")
        
        # Calculate Central Time
        utc_now = datetime.now(timezone.utc)
        central_time = utc_now - timedelta(hours=6)
        today_date = central_time.strftime("%Y-%m-%d")
        print(f"Fetching games for date: {today_date}")
        
        # Fetch NBA data
        api_url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{today_date}?key={api_key}"
        data = fetch_nba_data(api_url)
        
        # Process game data
        messages = [format_game_data(game) for game in data]
        final_message = "\n---\n".join(messages) if messages else "No games available for today."
        
        # Publish to SNS
        aws.publish_sns_message(
            topic_arn=sns_topic_arn,
            message=final_message,
            subject=f"NBA Game Updates - {today_date}"
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Data processed and sent to SNS successfully",
                "timestamp": utc_now.isoformat(),
                "games_processed": len(messages)
            })
        }
        
    except ClientError as e:
        error_message = f"AWS Service Error: {str(e)}"
        print(error_message)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": error_message})
        }
        
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        print(error_message)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": error_message})
        }