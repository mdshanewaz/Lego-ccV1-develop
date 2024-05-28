# terraform {
#   backend "s3" {
#     bucket         = "terraform-state-logo"
#     key            = "terraform.tfstate"
#     region         = "us-west-1"
#     dynamodb_table = "logowebterraform"
#   }
# }