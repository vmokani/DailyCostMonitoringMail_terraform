//Email Identity for Vishal Mokani
data "aws_sesv2_email_identity" "vishal" {
  email_identity = "vishal.mokani@jeavio.com"
}

# // Email Identity for Jayesh Patel
# data "aws_sesv2_email_identity" "jayesh" {
# email_identity = "jayesh@jeavio.com"
# }

# output "email_identity_jayesh" {
#   value = data.aws_sesv2_email_identity.jayesh.email_identity
# }
# output "email_verification_status_jayesh" {
#   value = data.aws_sesv2_email_identity.jayesh.verified_for_sending_status
# }