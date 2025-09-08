# lambda-tf-workspaces-cicd
This repository contains Terraform code to create AWS Lambda functions with multiple workspaces and CI/CD pipeline using GitHub Actions.

## Project has three segments
- OIDC connect For AWS role
- GitHub Environments
- Terraform 
  - Used workspaces feature as demo
  - [docs](https://developer.hashicorp.com/terraform/cloud-docs/workspaces#creating-workspaces)

## OpenID Connect
- [openid-connect Docs](https://docs.github.com/en/actions/concepts/security/openid-connect)
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

## Github Environments
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


## Pre-requistes: before running terraform
- AWS Role - created using OIDC to interact from Github Workflow actions and with neccessary permissions
- bucket = "aws-glue-terraform-state-kspr"
- key= "lambda-tf-workspaces-cicd/terraform.tfstate"
- dynamodb_table = "eks-terraform"


# Ready for some action? 

## Steps to follow along
1. Clone the repository
    ### Note
    - Make sure to update the bucket name, key and dynamodb_table in the backend.tf file
    - Make sure to update the AWS_ACCOUNT_NUMBER in the IAM role trust relationship policy
    - Make sure to update the RepoOwner in the IAM role trust relationship policy
    - Make sure to update the role name in the GitHub Environments
    - Make sure to update the region value in the GitHub Environments
2. For the initial process only keep backend.tf and variables.tf with the values that are relavant to your aws environment and push the code to repo
3. Go to the GitHub Actions tab
    - Right side top corner there is an option Run workflow , make sure you check the branch as main or relavant branch before running the pipeline
      - Click on Run workflow button - There is a check box that is available where the default value will be false
        - false (default): This will run the terraform init and apply plan and will initiate the process and registers terratform.tfstate file in s3 location
        - true: select the check box and it will pass value true and it will init the terraform plan and applies the plan , Please refere the plan and verify the resources in aws account
    - As part of my CICD pipeline i made it in a way to create a workspace called prod ( SDLC ) , that will be created in the s3 location where you have mentioned
      - Here is the S3 location where you can see the terraform state file.
        - If branch name is main , i mapped it to create a workspace name called prod (SDLC) , here is how you will see the location in s3 bucket
          - s3://aws-glue-terraform-state-kspr/env:/prod/lambda-tf-workspaces-cicd/workspaces/terraform.tfstate
        - if branch name is develop, i mapped it to create a workspace name called dev (SDLC) , here is how you will see the location in s3 bucket
          - s3://aws-glue-terraform-state-kspr/env:/dev/lambda-tf-workspaces-cicd/workspaces/terraform.tfstate
        - if any other feature branch in this format "feature/1111-kosana" ( as lower SDLC ) for creating sdlc branches
          - In this scenario , i wrote in cicd pipeline to split the name on "-" and get the right value into creating workspace , in this case it will be "kosana"
          - In this case as the workspace name which will be created is "kosana" , the location will be created a follows
            - s3://aws-glue-terraform-state-kspr/env:/kosana/lambda-tf-workspaces-cicd/workspaces/terraform.tfstate
      - When terraform is runing it will create a record in dynamodb (eks-terraform) with LockId as the below string
        - aws-glue-terraform-state-kspr/env:/prod/lambda-tf-workspaces-cicd/workspaces/terraform.tfstate-md5
4. Add ecr.tf in terraform folder and push the code in the repo
5. Go to the GitHub Actions tab
    - Follow the same steps to run your workflow as you did in step 3. 
    - Now this will show creation of ECR repo in the workspace prod as the pipeline is running using main branch
    - Verify the tfplan step in the workflow to see if the appropriate resources creation is in the plan
    - once you have verified that plan is being populated as expected , re run the action now by enabling the checkbox and once the plan is successfully complete you can see the aws resource will generate as shown in the plan from above step

### Develop Lifecycle 
1. Create a branch called develop from main
2. Push the code to repo
3. Go to the GitHub Actions tab
    - Follow the same steps to run your workflow as you did in step 3. 
    - Now this will show creation of ECR repo in the workspace dev as the pipeline is running using develop branch
    - Verify the tfplan step in the workflow to see if the appropriate resources creation is in the plan
    - once you have verified that plan is being populated as expected , re run the action now by enabling the checkbox and once the plan is successfully complete you can see the aws resource will generate as shown in the plan from above step
