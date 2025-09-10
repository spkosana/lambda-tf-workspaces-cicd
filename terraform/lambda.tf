resource "aws_lambda_function" "users_lambda" {
  function_name = "${terraform.workspace}-${var.app_name}"
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.users.repository_url}:latest"
  role          = aws_iam_role.iam_for_lambda.arn
  architectures = ["arm64"]

  depends_on = [aws_iam_role.iam_for_lambda, aws_ecr_repository.users, null_resource.image_build]

  # Timeout
  timeout = var.timeout # In seconds (up to 900 seconds or 15 minutes)

  # Memory
  memory_size = var.memory_size # In MB (from 128 MB to 10240 MB)

  image_config {
    command = ["handler.lambda_handler"]
  }


  tags = {
    Name = "Users generator Lambda function in ${terraform.workspace}"
  }

}