# Output for IAM role name:
output "aws_iam_role_lambda" {
  value = aws_iam_role.ReadDailyBill_clops.name
}
output "aws_iam_role_eventbridge" {
  value = aws_iam_role.Amazon_EventBridge_Scheduler_LAMBDA_role_Terraform.name
}

# Lambda function name
output "aws_lambda_function_name" {
  value = aws_lambda_function.monitoring_lambda_function.function_name
}

# scheduler name
output "aws_scheduler_schedule_name" {
  value = aws_scheduler_schedule.lambda_terraform.name
}

# cron expression
output "schedule_expression_cronValue" {
  value = aws_scheduler_schedule.lambda_terraform.schedule_expression
}

# output for email identity
output "email_identity_vishal" {
  value = data.aws_sesv2_email_identity.vishal.email_identity
}
output "email_verification_status_vishal" {
  value = data.aws_sesv2_email_identity.vishal.verified_for_sending_status
}
