output "instance_public_ip" {
  description = "Public IP of the AnomalyX EC2 instance"
  value       = aws_instance.anomalyx_server.public_ip
}

output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.anomalyx_server.id
}