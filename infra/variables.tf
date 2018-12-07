variable "name" {
  description = "Your own name that will identify some of the resources."
  default     = "jonny"
}

variable "vpc_id" {}

variable "subnet_id" {}

variable "allow_cidr_blocks" {
  type = "list"
}
