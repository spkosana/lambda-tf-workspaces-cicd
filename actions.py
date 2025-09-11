from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.security import IAM
from diagrams.aws.compute import ECR
from diagrams.aws.management import CloudFormation
from diagrams.onprem.ci import GitHubActions

with Diagram("GitHub Actions Workflow creates AWS resources using Terraform", show=True):
    github_actions = GitHubActions("GitHub Actions")
    workflow = github_actions.add_subgraph("Workflow")
    terraform = workflow.add_node(CloudFormation("Terraform"))
    iam = workflow.add_node(IAM("IAM Role"))
    ecr = workflow.add_node(ECR("ECR Repository"))
    lambda_func = workflow.add_node(Lambda("Lambda Function"))

    workflow.add_edge(github_actions, terraform, label="Trigger Terraform")
    workflow.add_edge(terraform, iam, label="Create IAM Role")
    workflow.add_edge(terraform, ecr, label="Create ECR Repository")
    workflow.add_edge(terraform, lambda_func, label="Create Lambda Function")
    workflow.add_edge(iam, ecr, label="Grant IAM Role access to ECR")
    workflow.add_edge(ecr, lambda_func, label="Use Docker image from ECR")

    github_actions >> workflow