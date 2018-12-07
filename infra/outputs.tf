output "jenkins_url" {
  value       = "http://${aws_instance.jenkins_master.public_ip}"
  description = "Public IP of the Jenkins Master."
}
