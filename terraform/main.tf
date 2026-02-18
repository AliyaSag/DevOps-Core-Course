# Network
resource "yandex_vpc_network" "devops_network" {
  name = "devops-network"
}

resource "yandex_vpc_subnet" "devops_subnet" {
  name           = "devops-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.devops_network.id
  v4_cidr_blocks = ["10.10.0.0/24"]
}

# Security Group
resource "yandex_vpc_security_group" "devops_sg" {
  name        = "devops-security-group"
  description = "Security group for DevOps VM"
  network_id  = yandex_vpc_network.devops_network.id

  # SSH access
  ingress {
    protocol       = "TCP"
    description    = "SSH"
    v4_cidr_blocks = [var.allowed_ssh_ip]
    port           = 22
  }

  # HTTP access
  ingress {
    protocol       = "TCP"
    description    = "HTTP"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 80
  }

  # Application port (from Lab 2)
  ingress {
    protocol       = "TCP"
    description    = "App Port"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 5000
  }

  # Allow all outgoing traffic
  egress {
    protocol       = "ANY"
    description    = "Outbound"
    v4_cidr_blocks = ["0.0.0.0/0"]
    from_port      = 0
    to_port        = 65535
  }
}

# Public IP
resource "yandex_vpc_address" "devops_ip" {
  name = "devops-public-ip"

  external_ipv4_address {
    zone_id = var.zone
  }
}

# VM Instance
resource "yandex_compute_instance" "devops_vm" {
  name        = var.vm_name
  platform_id = "standard-v3"
  zone        = var.zone

  resources {
    cores  = var.vm_cores
    memory = var.vm_memory
  }

  boot_disk {
    initialize_params {
      image_id = "fd8idfirhnddklq0u5nk" # Ubuntu 24.04 LTS
      size     = var.vm_disk_size
    }
  }

  network_interface {
    subnet_id          = yandex_vpc_subnet.devops_subnet.id
    nat                = false
    ip_address         = "10.10.0.10"
    security_group_ids = [yandex_vpc_security_group.devops_sg.id]
  }

  metadata = {
    ssh-keys = "ubuntu:${var.ssh_public_key}"
    user-data = <<-EOF
      #cloud-config
      package_update: true
      packages:
        - docker.io
        - python3-pip
      runcmd:
        - systemctl enable docker
        - systemctl start docker
        - usermod -aG docker ubuntu
    EOF
  }
}

# Associate public IP with VM
resource "yandex_compute_instance_group" "devops_vm_with_ip" {
  name = "devops-vm-group"

  instance_template {
    platform_id = "standard-v3"
    
    resources {
      cores  = var.vm_cores
      memory = var.vm_memory
    }

    boot_disk {
      mode = "READ_WRITE"
      initialize_params {
        image_id = "fd8idfirhnddklq0u5nk"
        size     = var.vm_disk_size
      }
    }

    network_interface {
      network_id = yandex_vpc_network.devops_network.id
      subnet_ids = [yandex_vpc_subnet.devops_subnet.id]
      nat        = true
    }

    metadata = {
      ssh-keys = "ubuntu:${var.ssh_public_key}"
    }
  }

  scale_policy {
    fixed_scale {
      size = 1
    }
  }

  allocation_policy {
    zones = [var.zone]
  }

  deploy_policy {
    max_unavailable = 1
    max_expansion   = 0
  }
}