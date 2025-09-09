# lambda-tf-workspaces-cicd
## Overview

# Project has three segments
- OIDC connect For AWS role
- GitHub Environments
- Terraform 
  - Used workspaces feature as demo
  - [docs](https://developer.hashicorp.com/terraform/cloud-docs/workspaces#creating-workspaces)

# OpenID Connect
- [openid-connect Docs](https://docs.github.com/en/actions/concepts/security/openid-connect)
- [oidc-in-aws](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
- Go to Aws Console
  - Click on IAM 
  - Click on Identiry providers
  - Click on Add provider 
  - Select OpenID Connect 
  - In provider URL give below address
    - https://token.actions.githubusercontent.com
  - Audience
    - sts.amazonaws.com
  - Click on Add provider
- Create a IAM role
  - Add permissions
    - Attach existing policies directly
    - Select AdministratorAccess (for demo purpose only, for production create custom policy)
  - Click on Trust Relationships
    - Click on Edit trust relationship
      - Add your prinicpal which created in above opendi connect steps
      - Add aud "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
      - Add sub "token.actions.githubusercontent.com:sub": "repo:RepoOwner/individualProject/*"
    - Replace the existing policy with below policy
    ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Federated": "arn:aws:iam::AWS_ACCOUNT_NUMBER:oidc-provider/token.actions.githubusercontent.com"
                    },
                    "Action": "sts:AssumeRoleWithWebIdentity",
                    "Condition": {
                        "StringEquals": {
                            "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                        },
                        "StringLike": {
                            "token.actions.githubusercontent.com:sub": "repo:RepoOwner/*"
                        }
                    }
                }
            ]
        }
    ```

# Github Environments
- Go to the Project Settings
- Click on Environments
- Click on New environment
- Name the environments
  - production - Production account details
    - Click on Add Environment Variables
      - Add name AWS_IAM_ROLE and add the role name 
      - Add name AWS_REGION and add the region value 
  - development - Development account details
    - Click on Add Environment Variables
      - Add name AWS_IAM_ROLE and add the role name 
      - Add name AWS_REGION and add the region value 


# Getting Started

## Prerequisites
Before running Terraform, update these values:
- AWS Role ARN in trust relationship policy (replace `AWS_ACCOUNT_NUMBER` and `RepoOwner`)
- S3 bucket: `aws-glue-terraform-state-kspr`
- State file key: `lambda-tf-workspaces-cicd/workspaces/terraform.tfstate`
- DynamoDB table: `eks-terraform`
- GitHub Environment variables (AWS_IAM_ROLE and AWS_REGION)

## Initial Setup
1. **Clone the repository**
2. **Configure backend**: Keep only `backend.tf` and `variables.tf` with your AWS environment values
3. **Run initial workflow**:
  - Go to GitHub Actions → "aws-resources-apply" workflow
  - Select main branch → Click "Run workflow"
  - **Checkbox options**:
    - `false` (default): Init and plan only, creates state file in S3
    - `true`: Init, plan, and apply resources

## Workspace Mapping
Below is how the workspaces will be created from github actions workflow workspace-tf-plan and creates a lockid with files name in the dynamodb table
| Branch Pattern | Workspace | S3 State Location  |
|---|---|---|
| `main` | `prod` | `s3://bucket/env:/prod/...terraform.tfstate` |
| `develop` | `dev` | `s3://bucket/env:/dev/...terraform.tfstate` |
| `feature/1111-kosana` | `kosana` | `s3://bucket/env:/kosana/...terraform.tfstate` |
| `hotfix/0000-prakash` | `hotfix-prakash` | `s3://bucket/env:/hotfix-prakash/...terraform.tfstate` |

## Add Resources
1. Add `ecr.tf` to terraform folder
2. Push code to repository
3. Run workflow with checkbox enabled to apply changes

# Develop Lifecycle 
1. Create a branch called develop from main
2. Push the code to repo
3. Go to the GitHub Actions tab - Testing aws-resources-apply workflow for develop branch
    - Follow the same steps to run your workflow as you did before. 
    - workspace dev will be created with ECR repo
    - Verify the tfplan step in the workflow to see if the appropriate resources creation is in the plan
    - once you have verified that plan is being populated as expected , re run the action now by enabling the checkbox and once the plan is successfully complete you can see the aws resource will generate as shown in the plan from above step

# Individual contributor lifecycle - developer SDLC - Make sure you create branch starts with "feature/"
1. Create a branch called feature/1111-kosana from develop
2. Push the code to repo
3. Go to the GitHub Actions tab - Testing aws-resources-apply workflow for kosana/or any individual contributor branch
    - Follow the same steps to run your workflow as you did before. 
    - workspace kosana will be created with ECR repo
    - Follow the steps above to verify resources has been created in the aws environment
    - Now for testing change some values in the tags just for fun and add the code changes and push the code
    - Run the workflow again and observe the changes in your aws resources based on the changes in the code push
4. Its time to create merge request to develop
5. Create a pull request from feature/1111-kosana to develop branch
6. Once the PR is approved and merged , Go to the GitHub Actions tab,feature-branch-destory worflow complets the cleanup of aws resources and branch

# hotfix lifecycle - Make sure you create branch starts with "hotfix/"
1. Create a branch called hotfix/0000-prakash from main
2. Push the code to repo
3. Go to the GitHub Actions tab - Testing aws-resources-apply workflow for hotfix/0000-prakash
    - Follow the same steps to run your workflow as you did before. 
    - Now this will show creation of ECR repo in the workspace prakash as the pipeline is running using hotfix/0000-prakash branch
    - Follow the steps above to verify resources has been created in the aws environment
    - Now for testing change some values in the tags just for fun and add the code changes and push the code
    - Run the workflow again and observe the changes in your aws resources based on the changes in the code push
4. Its time to create a pull request to main
5. Create a pull request from hotfix/0000-prakash to main branch
6. Once the PR is approved and merged , Go to the GitHub Actions tab , hotfix-branch-destory worflow complets the cleanup of aws resources , branch and also sync main branch to develop after hotfix is deployed successfully.