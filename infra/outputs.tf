output "jenkins_url" {
  value       = "http://${aws_instance.jenkins_master.public_ip}:8080"
  description = "Public IP of the Jenkins Master."
}
