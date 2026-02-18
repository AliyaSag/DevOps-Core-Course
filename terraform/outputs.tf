output "vm_public_ip" {
  description = "Public IP address of the VM"
  value       = yandex_compute_instance_group.devops_vm_withup.instances[0].network_interface[0].nat_ip_address
}

output "vm_private_ip" {
  description = "Private IP address of the VM"
  value       = yandex_compute_instance_group.devops_vm_withup.instances[0].network_interface[0].ip_address
}

output "ssh_command" {
  description = "SSH command to connect to VM"
  value       = "ssh ubuntu@${yandex_compute_instance_group.devops_vm_withup.instances[0].network_interface[0].nat_ip_address}"
}

output "vm_id" {
  description = "VM Instance ID"
  value       = yandex_compute_instance_group.devops_vm_withup.instances[0].instance_id
}

output "network_id" {
  description = "Network ID"
  value       = yandex_vpc_network.devops_network.id
}

output "subnet_id" {
  description = "Subnet ID"
  value       = yandex_vpc_subnet.devops_subnet.id
}