# NBA Game Day Notifications/ Live Sports Alerts

## Project Overview:
This system fetches NBA game scores and automatically sends updates to subscribers through SMS or email. It runs on AWS (Amazon Web Services) using cloud-based architecture, making it cost-effective and scalable.

---

## Features:
- Real-time NBA game score updates, using an external API
- Score updates sent to subscribers via SMS and email notifications (through Amazon SNS)
- Automated scheduling with Amazon EventBridge
- Secure AWS IAM role configuration
  
## Prerequisites
- AWS Account
- API key from [sportsdata.io](https://sportsdata.io/)
- Basic familiarity with AWS services

## Detailed Setup Guide: 

### Clone the Repository:

```bash
git clone https://github.com/fpier042/nba-game-day-notifications.git
cd game-day-notifications

```

### Create SNS Topic;
1. Go to AWS Management Console → SNS (Simple Notification Services)
2. Click "Create topic"
3. Select "Standard" type
4. Name your topic (e.g., `nba_notifications`)
5. Create topic and save the ARN (Amazon Resource Name)

### Add Subscriptions:
1. Select your SNS topic
2. Click "Create subscription"
3. For Email notifications:
   - Protocol: Email
   - Enter email address
   - Create subscription
   - Check email and confirm subscription
4. For SMS notifications:
   - Protocol: SMS
   - Enter phone number (+1XXXXXXXXXX)
   - Create subscription

### Set Up IAM Permissions

#### Create SNS Policy:
1. Go to IAM → Policies → Create Policy
2. Use JSON editor and paste:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish"
            ],
            "Resource": "arn:aws:sns:REGION:ACCOUNT_ID:nba_notifications"
        }
    ]
}
```
3. Replace REGION and ACCOUNT_ID with your values
4. Name the policy (e.g., `nba_sns_policy`)

#### Create Lambda Role:
1. Go to IAM → Roles → Create Role
2. Select AWS Lambda as the service
3. Attach these policies:
   - Your SNS policy (`nba_sns_policy`)
   - `AWSLambdaBasicExecutionRole`
4. Name the role (e.g., `nba_lambda_role`)
5. Save the role ARN

### Deploy Lambda Function:
1. Go to AWS Lambda
2. Create function:
   - Author from scratch
   - Name: `nba_score_notifications`
   - Runtime: Python 3.x
   - Role: Use the role created above
3. Add environment variables:
   - `NBA_API_KEY`: Your sportsdata.io API key
   - `SNS_TOPIC_ARN`: Your SNS topic ARN
4. Copy the function code from this repository's `lambda_function.py`

### Set Up EventBridge
1. Go to EventBridge → Rules
2. Create rule:
   - Name: `nba_score_updates`
   - Schedule: Fixed rate (e.g., 1 hour)
3. Add target:
   - Select your Lambda function
   - Save the rule

### Testing:
1. In Lambda console, click "Test"
2. Create a test event (i.e test1, or empty `{}` is fine)
3. Run test and check:
   - CloudWatch Logs for errors
   - Your subscribed email/phone for notifications

## Project Structure:
```
nba-notifications/
├── lambda_function.py          # Main Lambda function
├── tests/                      # Test cases
│   └── test_lambda.py
├── iam/                        # IAM policy templates
│   ├── sns_policy.json
│   └── lambda_role.json
└── README.md
```

## Troubleshooting:

Common issues and solutions:
1. No notifications received:
   - Check SNS subscription confirmation
   - Verify Lambda execution role permissions
   - Check CloudWatch Logs for errors

2. Lambda timeout:
   - Increase timeout in Lambda configuration
   - Optimize API calls

## Future Enhancements:

1. Add support for NFL (and other sports) scores
2. Store user preferences in DynamoDB
3. Create web interface for subscription management
4. Add support for favorite teams
5. Include more detailed game statistics

## Contributing:

Contributions are welcome! Please feel free to submit a Pull Request.

## License:
This project is licensed under the MIT License - see the LICENSE file for details.
