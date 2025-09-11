# cicd_tf_backend_no_apply.py
from diagrams import Diagram, Edge
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.iac import Terraform
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.security import IAMRole

with Diagram(
    "CI/CD → Terraform Backend (State + Lock)",
    filename="cicd_tf_backend",
    show=False,
    direction="LR",
):
    # GitHub branches
    dev  = Github("develop branch")
    main = Github("main branch")

    # CI/CD pipeline (GitHub Actions → Terraform)
    gha = GithubActions("GitHub Actions")
    tf  = Terraform("Terraform\ninit / plan / apply")
    oidc_role = IAMRole("IAM Role (OIDC)\nTemporary Credentials")

    # Flow: branches → Actions → Terraform
    [dev, main] >> Edge(label="push/merge") >> gha >> Edge(label="runs")  >> oidc_role >> tf

    # Terraform backend only (no apply to resources)
    tfstate_bucket = S3("aws-glue-terraform-state-kspr\n(terraform.tfstate)")
    lock_table     = Dynamodb("eks-terraform")

    tf >> Edge(label="state read/write") >> tfstate_bucket
    tf >> Edge(label="lock/unlock") >> lock_table

