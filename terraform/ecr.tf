locals {
  #   docker_source_hash = filesha256("${path.module}/../backend/Dockerfile") # Or include other source files/directories
  dir_content_hash = sha256(join("", [for f in fileset(path.module, "../src/**/*") : filesha256("${path.module}/../src/${f}")]))
}


data "aws_caller_identity" "current" {}
resource "aws_ecr_repository" "users" {
  name                 = "${terraform.workspace}-${var.app_name}"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${terraform.workspace}-${var.app_name}"
    Team = "AmazingTeam"
  }

}


resource "null_resource" "image_build" {

  provisioner "local-exec" {
    command = <<EOF
	    aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin ${data.aws_caller_identity.current.account_id}.dkr.ecr.us-east-2.amazonaws.com;
	    docker build --platform linux/arm64 --provenance false --tag "${aws_ecr_repository.users.repository_url}:latest" -f ${path.module}/../src/Dockerfile ${path.module}/../src/ ;
	    docker push "${aws_ecr_repository.users.repository_url}:latest"
	    EOF
  }


  triggers = {
    source_hash = local.dir_content_hash
  }


  depends_on = [
    aws_ecr_repository.users
  ]
}