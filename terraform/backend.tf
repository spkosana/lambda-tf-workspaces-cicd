terraform {

  # Comment this out when initialising resources.
  backend "s3" {
    region         = "us-east-2"
    bucket         = "aws-glue-terraform-state-kspr"
    key            = "lambda-tf-workspaces-cicd/workspaces/terraform.tfstate"
    dynamodb_table = "eks-terraform"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.11.0"
    }
  }
}

locals {
  repo_name = "$(basename -s .git `git config --get remote.origin.url`)"
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Environment = "${terraform.workspace}"
      Project     = "LAMBDA-TF-WORKSPACES-CICD"
      Owner       = "Surya Kosana"
      Repository  = local.repo_name
    }
  }
}

