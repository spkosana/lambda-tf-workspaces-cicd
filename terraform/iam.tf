// Create IAM role for AWS Lambda
resource "aws_iam_role" "iam_for_lambda" {
  name = "${terraform.workspace}-${app_name}-role"
  tags = {
    Name = "Users generator Lambda Role"
  }

  assume_role_policy = <<-EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "lambda_access_policy" {
  name        = "${terraform.workspace}-${app_name}-access-policy"
  description = "Policy for Lambda function to access S3 and CloudWatch Logs"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
        ]
        Resource = ["arn:aws:s3:::capstone-kspr/*"]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
    ]
  })
  tags = {
    Name = "Users generator Lambda Access Policy to S3 and Cloudwatch logs"
  }
}

#iam_policy_attachment
resource "aws_iam_policy_attachment" "policy_attachment" {
  name       = "${terraform.workspace}-${app_name}-access-role-policy"
  roles      = [aws_iam_role.iam_for_lambda.name]
  policy_arn = aws_iam_policy.lambda_access_policy.arn
}