#!/bin/bash
cd terraform
IP=$(terraform output -raw instance_public_ip)
cd ../ansible

cat > inventory.ini <<EOF
[anomalyx]
$IP ansible_user=ubuntu ansible_ssh_private_key_file=/home/ridhima-2412/.ssh/anomalyx-key ansible_python_interpreter=/usr/bin/python3
EOF

echo "Inventory updated with IP: $IP"