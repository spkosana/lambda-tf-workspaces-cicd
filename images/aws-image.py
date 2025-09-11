from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.aws.compute import ECR
from diagrams.aws.security import IAMRole,IAMPermissions

with Diagram("AWS Architecture", show=False,direction="LR",filename="aws_architecture",):
    iam_role = IAMRole("prod-generate-users-role")
    lambda_function = Lambda("prod-generate-users")
    s3_bucket = S3("capstone-kspr")
    cloudwatch_logs = Cloudwatch("CloudWatch Logs")
    ecr_repo = ECR("prod-generate-users")
    cloudwatch_policy = IAMPermissions("cloudWatch-access-policy")
    s3_policy = IAMPermissions("s3-access-policy")
    _ = iam_role >> [s3_policy,cloudwatch_policy] 
    _ = lambda_function >> Edge(label="runs from docker image in ECR") >> ecr_repo
    _ = lambda_function >> Edge(label="writes users file to") >> s3_bucket
    _ = lambda_function >> Edge(label="logs to") >> cloudwatch_logs
    
    _ = iam_role >> Edge(label="attached to") >> lambda_function