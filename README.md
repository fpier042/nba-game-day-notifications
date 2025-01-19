# 🏀 NBA Game Day Notifications/ Live Sports Alerts ⛹🏾‍♂️ (30 Days Dev Ops Challenge)

## 📖 Table of Contents 📖
- [Project Intro](#project-intro)
  - [Architecture Overview](#architecture-overview)
  - [System Workflow](#system-workflow)
- [Project Structure](#project-structure)
- [Application Features](#application-features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [User Guides](#user-guides)
- [Project Process,Step-by-step](#project-process)
- [Testing the System](#testing-system)
- [Potential Future Improvements](#potential-future-improvements)
- [How to Contribute](#how-to-contribute)
- [License](#license)
- [Contact](#contact)

## 💻 Project Intro 💻

Here is documentation detailing how to develop a system which retrieves real-time NBA game scores and automatically sends such updates to subscribers through SMS or email. Perfect for hard-core sports fans! It runs on AWS (Amazon Web Services) using cloud-based architecture, making it cost-effective and scalable; and it utilizes an external API (application programming interface) and AWS Lambda, EventBridge, and SNS.

This project taught me (and demonstrates to other learners) both principles of cloud computing and mechanisms for providing efficient notification(s) delivery, through:

- Python programming 🐍
- API integration 🔑
- AWS services (SNS, Lambda, EventBridge) 🚚
- Environment variable management 🌱
- Asynchronous programming ⛓️‍💥

And aims to provide the user valuable insight on serverless systems whether you're a developer learning more about Python and AWS (like myself), or someone who is an NBA fanatic!  

### Architecture Overview (A breakdown of the technologies/systems being utilized):

![image](https://github.com/user-attachments/assets/c9a7eb8d-1ab2-4489-adf5-897a98f836a1)

- **External API** : Fetches data related to NBA games
- **AWS Lambda** : Responsible for executing code in response to triggers
- **EventBridge** : Acts as an event bus that triggers the Lambda function on a cron-based schedule
- **Amazon SNS** : Sends notifications to users about upcoming games

### System Workflow:

- **Event Scheduling**: AWS EventBridge triggers the Lambda function based on a predefined cron (or time-based) schedule (e.g., once a
  day, or every hour)
- **API Call**: The Lambda function makes an HTTP request to an external API to fetch current NBA game information
- **Data Processing**: The function processes the obtained data to extract relevant details (e.g., game time, teams, game-status, channel, scores e.t.c)
- **User Notification**: The processed data is sent to subscribed users via Amazon SNS

## ⚙️ Project Structure

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

## ⚡️Application Features

- Real-time NBA game scores, using an external API
- Formatted score updates sent to subscribers via SMS and email notifications, using Amazon SNS
- Scheduled automation for regular updates via Amazon EventBridge
- Secure AWS IAM role configuration

## 🛠️ Getting Started

### 🔖Prerequisites

Before beginning the project, ensure you have the following set up on your machine/computer 🖥️:

- Basic familiarity with AWS services and Python
- Python 3.7 or higher
- A NBA API key of your choice 
- An AWS account with access to SNS, Lambda, and EventBridge
- A GitHub account with SSH authentication [https://docs.github.com/en/authentication/connecting-to-github-with-ssh]

### 📘 User Guides

And here are some general resources to provide you further context and ground you as you move through the project:

- [AWS SNS Documentation]([https://docs.aws.amazon.com/s3/index.html](https://docs.aws.amazon.com/sns/)): How to use AWS SNS
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/): How to use AWS Lambda
- [AWS EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/): How to use AWS EventBriddge

## 👨🏾‍💻 Project Process, Step-by-step

### Clone the Repository:

```bash
git clone https://github.com/fpier042/nba-game-day-notifications.git
cd game-day-notifications

```
### Create an SNS Topic:
1. Go to AWS Management Console → SNS (Simple Notification Services)
2. Click "Create topic"
3. Select "Standard" type
4. Name your topic (e.g., `nba_notifications`)
5. Create topic and save the ARN (Amazon Resource Name)

### Add a Subscription:
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

### Set Up IAM Permissions:

#### Create an SNS Policy:
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

#### Create a Lambda Role:
1. Go to IAM → Roles → Create Role
2. Select AWS Lambda as the service
3. Attach these policies:
   - Your SNS policy (`nba_sns_policy`)
   - `AWSLambdaBasicExecutionRole`
4. Name the role (e.g., `nba_lambda_role`)
5. Save the role ARN

### Deploy the Lambda Function:
1. Go to AWS Lambda
2. Create function:
   - Author from scratch
   - Name: `nba_score_notifications`
   - Runtime: Python 3.x
   - Role: Use the role created above
3. Add environment variables:
   - `NBA_API_KEY`: Your chosen API key
   - `SNS_TOPIC_ARN`: Your SNS topic ARN
4. Copy the function code from this repository's `lambda_function.py`

### Set Up EventBridge:
1. Go to EventBridge → Rules
2. Create rule:
   - Name: `nba_score_updates`
   - Schedule: Fixed rate (e.g., 1 hour)
3. Add target:
   - Select your Lambda function
   - Save the rule

## Testing the System 🧪

1. In Lambda console, click "Test"
2. Create a test event (i.e test1, or empty `{}` is fine)
3. Run test and check:
   - CloudWatch Logs for errors
   - Your subscribed email/phone for notifications

## 🚧 Common Issues and Solutions 🚧

Here are some challenges you might encounter:

1. No notifications received:
   - Check SNS subscription confirmation
   - Verify Lambda execution role permissions
   - Check CloudWatch Logs for errors

2. Lambda timeout:
   - Increase timeout in Lambda configuration
   - Optimize API calls

## 🛸 Potential Future Improvements

1. Add support for NFL (and other sports) scores
2. Store user preferences in DynamoDB
3. Create web interface for subscription management
4. Add support for favorite teams
5. Include more detailed game statistics

## 🫱🏻‍🫲🏾 How to Contribute

Contributions are what allow for the open-source community to serve as a valuable resource for developers to learn various tools, inspire others, and create their best work

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🪪License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📲 Contact Information

Felton Pierre: [Linkedin](https://www.linkedin.com/in/felton-pierre-90/)

Project Link: https://github.com/fpier042/nba-game-day-notifications.git
