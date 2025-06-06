terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_dynamodb_table" "tasks" {
  name           = "Tasks"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "N"
  }
}
