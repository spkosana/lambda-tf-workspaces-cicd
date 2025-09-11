# cicd_terraform_backend.py
# pip install diagrams
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.vcs import Github
from diagrams.onprem.iac import Terraform

from diagrams.aws.security import IAMRole,IAMPermissions
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import VPC
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS

diagram_title = "CI/CD with GitHub Actions + Terraform (S3 Backend + DynamoDB Lock)"

with Diagram(diagram_title, filename="ci_cd_terraform_backend", show=False, direction="LR"):

    # Repo & branches
    with Cluster("GitHub Repository"):
        develop_branch = Github("branch: develop")
        main_branch    = Github("branch: main")

    gha = GithubActions("GitHub Actions\n(workflows on push/merge)")

    # OIDC role in AWS (recommended)
    oidc_role = IAMRole("IAM Role (OIDC)\nassumed by GHA")

    # Terraform runner
    tf = Terraform("Terraform CLI\ninit / plan / apply")

    # Terraform backend
    with Cluster("Terraform Backend"):
        tfstate_bucket = S3("S3 Bucket\n(tfstate)")
        ddb_lock_table = Dynamodb("DynamoDB Table\n(tfstate lock)")

    # Example target resources
    with Cluster("AWS Account (Target Infrastructure)"):
        vpc     = VPC("VPC / Networking")
        lambda_ = Lambda("Lambda Functions")
        db      = RDS("RDS / Database")
        logs    = Cloudwatch("CloudWatch Logs / Metrics")

    # Flow: branches -> GHA
    [develop_branch, main_branch] >> Edge(label="push / merge") >> gha

    # GHA assumes OIDC role, then runs Terraform
    gha >> Edge(label="assume-role (OIDC)") >> oidc_role >> tf

    # Terraform backend interactions
    tf >> Edge(label="backend: read/write state") >> tfstate_bucket
    tf >> Edge(label="state lock/unlock") >> ddb_lock_table

    # Terraform apply -> creates/updates AWS resources
    tf >> Edge(label="apply") >> [vpc, lambda_, db, logs]

    # Optional feedback loop to GitHub Actions (logs/artifacts)
    [vpc, lambda_, db, logs] >> Edge(label="status / outputs") >> gha
