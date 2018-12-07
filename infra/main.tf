data "aws_ami" "amzn2_linux_latest" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

provider "aws" {
  region = "eu-west-1"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

data "aws_vpc" "selected" {
  id = "${var.vpc_id}"
}

data "template_file" "jenkins_master_provision_script" {
  template = "${file("${path.module}/templates/provision-jenkins-master.sh")}"
}

data "aws_subnet" "selected" {
  id = "${var.subnet_id}"
}

resource "aws_security_group" "jenkins_sg" {
  vpc_id      = "${var.vpc_id}"
  name        = "Jenkins Security Group"
  description = "Jenkins Security Group"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["${var.allow_cidr_blocks}"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["${var.allow_cidr_blocks}"]
  }
}

locals {
  public_key_filename  = "${path.root}/keys/public.pub"
  private_key_filename = "${path.root}/keys/private.pem"
}

resource "tls_private_key" "generated" {
  algorithm = "RSA"
}

resource "aws_key_pair" "generated" {
  key_name   = "fastai-${uuid()}"
  public_key = "${tls_private_key.generated.public_key_openssh}"

  lifecycle {
    ignore_changes = ["key_name"]
  }
}

resource "local_file" "public_key_openssh" {
  content  = "${tls_private_key.generated.public_key_openssh}"
  filename = "${local.public_key_filename}"
}

resource "local_file" "private_key_pem" {
  content  = "${tls_private_key.generated.private_key_pem}"
  filename = "${local.private_key_filename}"
}

resource "null_resource" "chmod" {
  depends_on = ["local_file.private_key_pem"]

  triggers {
    key = "${tls_private_key.generated.private_key_pem}"
  }

  provisioner "local-exec" {
    command = "chmod 600 ${local.private_key_filename}"
  }
}

resource "aws_instance" "jenkins_master" {
  ami                         = "${data.aws_ami.amzn2_linux_latest.image_id}"
  instance_type               = "t2.small"
  subnet_id                   = "${data.aws_subnet.selected.id}"
  availability_zone           = "${data.aws_subnet.selected.availability_zone}"
  vpc_security_group_ids      = ["${aws_security_group.jenkins_sg.id}"]
  key_name                    = "${aws_key_pair.generated.key_name}"
  user_data                   = "${data.template_file.jenkins_master_provision_script.rendered}"
  iam_instance_profile        = "${aws_iam_instance_profile.jenkins_profile.name}"
  tags                        = "${map("Name", var.name)}"
  associate_public_ip_address = true
}
