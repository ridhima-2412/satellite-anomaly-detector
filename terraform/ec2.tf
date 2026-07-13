data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}
resource "aws_key_pair" "anomalyx_key" {
  key_name   = "anomalyx-key"
  public_key = file("${path.module}/anomalyx-key.pub")
}
resource "aws_instance" "anomalyx_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  key_name               = aws_key_pair.anomalyx_key.key_name
  vpc_security_group_ids = [aws_security_group.anomalyx_sg.id]

  tags = {
    Name = "anomalyx-server"
  }
}