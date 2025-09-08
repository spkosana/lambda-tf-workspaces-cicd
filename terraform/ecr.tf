resource "aws_ecr_repository" "users" {
  name                 = "${terraform.workspace}-generate-users"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${terraform.workspace}-generate-users"
    Env  = terraform.workspace
  }

}