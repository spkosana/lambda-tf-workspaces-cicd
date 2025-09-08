resource "aws_ecr_repository" "users" {
  name                 = "${terraform.workspace}-${var.app_name}"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${terraform.workspace}-generate-users"
    Env  = terraform.workspace
    Team = "AmazingTeam"
  }

}