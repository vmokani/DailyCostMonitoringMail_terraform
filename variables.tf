// Variable for AWS
variable "aws_region" {
  description = "AWS region where function needs to create"
  type        = string
}
// Variables for IAM Policies
variable "lambda_execution_policy_name" {
  description = "IAM policy name for lamda execution role"
  type        = string
}

variable "event_bridge_policy_name" {
  description = "IAM policy name for eventbridge scheduler role"
  type        = string
}

// Variables for IAM Roles
variable "lambda_execution_role_name" {
  description = "IAM role for lambda execution role"
  type        = string
}

variable "event_bridge_scheduler_role_name" {
  description = "IAM role for event bridge scheduler role"
  type        = string
}

// Variables for lambda function
variable "lambda_function_name" {
  description = "Lambda function name"
  type        = string
}

variable "handler" {
  description = "Entry point for lambda function i.e def handler (event,context)"
  type        = string
}

variable "runtime_version" {
  description = "Runtime version for lambda function I.e Python version"
  type        = string
}

variable "lambda_zip_filename" {
  description = "Source file or ZIP file for lamda function"
  type        = string
}

// Variables for Event bridge Scheduler
variable "scheduler_name" {
  description = "Event Bridge scheduler Name"
  type        = string
}

variable "scheduler_cron_expression" {
  description = "Cron expression for scheduler. Enter cron expression in form of 'Minute Hour DayOfMonth Month DayOfWeek Year' I.e: cron(* 17 * * ? *) "
  type        = string
}

variable "flexible_time_window" {
  description = "FlexiBle time window for scheduler to run cron job [OFF in case of disable]"
  type        = string
}

variable "schedule_expression_timezone" {
  description = "TimeZone for which cronjob needs to be run I.e Asia/Calcutta"
  type        = string
}



