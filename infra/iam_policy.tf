data "aws_iam_policy_document" "s3_access_policy_doc" {
  statement {
    sid       = "JenkinsAdminAccess"
    actions   = ["*"]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "s3_access_policy" {
  name   = "Allow_Jenkins_full_access"
  role   = "${aws_iam_role.jenkins_ec2_role.id}"
  policy = "${data.aws_iam_policy_document.s3_access_policy_doc.json}"
}

resource "aws_iam_role" "jenkins_ec2_role" {
  name               = "EC2_Jenkins_role"
  description        = "Provides the Jenkins EC2 instance with full access to AWS resources."
  assume_role_policy = "${data.aws_iam_policy_document.ec2_assume_role.json}"
}

resource "aws_iam_instance_profile" "jenkins_profile" {
  name = "Jenkins_instance_profile"
  role = "${aws_iam_role.jenkins_ec2_role.name}"
}
