resource "aws_iam_policy" "AWSLambdaBasicExecutionRole_Terraform" {
  name   = var.lambda_execution_policy_name
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:ap-south-1:381492240631:"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_policy" "Amazon_EventBridge_Scheduler_LAMBDA_Terraform" {
  name   = var.event_bridge_policy_name
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
EOF 
}

resource "aws_iam_role_policy_attachment" "AmazonSESFullAccess" {
  #name       = "AmazonSESFullAccess"
  role       = aws_iam_role.ReadDailyBill_clops.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSESFullAccess"
}

resource "aws_iam_role_policy_attachment" "Billing" {
  #name       = "Billing"
  role       = aws_iam_role.ReadDailyBill_clops.name
  policy_arn = "arn:aws:iam::aws:policy/job-function/Billing"
}

resource "aws_iam_role_policy_attachment" "AWSLambdaBasicExecutionRole_Terraform" {
  #name       = "AWSLambdaBasicExecutionRole_Terraform"
  role       = aws_iam_role.ReadDailyBill_clops.name
  policy_arn = aws_iam_policy.AWSLambdaBasicExecutionRole_Terraform.arn
}

resource "aws_iam_role_policy_attachment" "Amazon_EventBridge_Scheduler_LAMBDA_Terraform" {
  #name       = "Amazon_EventBridge_Scheduler_LAMBDA_Terraform"
  role       = aws_iam_role.Amazon_EventBridge_Scheduler_LAMBDA_role_Terraform.name
  policy_arn = aws_iam_policy.Amazon_EventBridge_Scheduler_LAMBDA_Terraform.arn
}