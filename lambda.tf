resource "aws_lambda_function" "monitoring_lambda_function" {
  function_name = var.lambda_function_name
  handler       = var.handler         # Your entry point (file.function)
  runtime       = var.runtime_version # Specify the runtime varsion I.e python3.14
  role          = aws_iam_role.ReadDailyBill_clops.arn
  # Source Code
  filename         = var.lambda_zip_filename //lambda zip filename
  source_code_hash = filebase64sha256(var.lambda_zip_filename)
}

# //Add Permissions to Allow Lambda Invocation
# resource "aws_lambda_permission" "allow_invoke" {
#   statement_id  = "AllowExecutionFromApiGateway"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.monitoring_lambda_function.function_name
#   principal     = "apigateway.amazonaws.com"
# }