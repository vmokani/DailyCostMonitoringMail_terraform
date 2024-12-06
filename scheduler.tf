resource "aws_scheduler_schedule" "lambda_terraform" {
  name = var.scheduler_name
  flexible_time_window {
    mode = var.flexible_time_window
  }

  schedule_expression          = var.scheduler_cron_expression
  schedule_expression_timezone = var.schedule_expression_timezone
  target {
    arn      = aws_lambda_function.monitoring_lambda_function.arn
    role_arn = aws_iam_role.Amazon_EventBridge_Scheduler_LAMBDA_role_Terraform.arn
    #input     = jsonencode({ "key": "value" })
  }
}