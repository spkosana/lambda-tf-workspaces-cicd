terraform {
  required_version = "~> 1.1"

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
    required_providers {
    external = {
      source  = "hashicorp/external"
      version = ">= 2.0.0"
    }
  }
}

data "external" "repo_name" {
  program = [
    "bash",
    "-c",
    <<-EOT
      REPO_NAME=$(git config --get remote.origin.url | cut -d'/' -f5 | cut -d'.' -f1)
      printf '{"repo_name": "%s"}' "$REPO_NAME"
    EOT
  ]
}
locals {
  repo_name = data.external.repo_name.result.repo_name
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Environment = terraform.workspace
      Project     = "LAMBDA-TF-WORKSPACES-CICD"
      Owner       = "Surya Kosana"
      Repository  = local.repo_name
    }
  }
}

