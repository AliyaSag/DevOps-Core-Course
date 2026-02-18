"""Pulumi program to create infrastructure identical to Terraform version."""
import pulumi
import pulumi_yandex as yandex

# Get configuration
config = pulumi.Config()
yandex_token = config.require_secret("yandexToken")
cloud_id = config.require("cloudId")
folder_id = config.require("folderId")
zone = config.get("zone", "ru-central1-a")
vm_name = config.get("vmName", "devops-vm-pulumi")
ssh_public_key = config.require_secret("sshPublicKey")
allowed_ssh_ip = config.get("allowedSshIp", "0.0.0.0/0")

# Create network
network = yandex.vpc.Network(
    "devops-network",
    name="devops-network-pulumi",
    opts=pulumi.ResourceOptions(protect=False)
)

# Create subnet
subnet = yandex.vpc.Subnet(
    "devops-subnet",
    name="devops-subnet-pulumi",
    zone=zone,
    network_id=network.id,
    v4_cidr_blocks=["10.10.0.0/24"]
)

# Create security group
security_group = yandex.vpc.SecurityGroup(
    "devops-sg",
    name="devops-security-group-pulumi",
    description="Security group for DevOps VM",
    network_id=network.id,
    
    ingress=[
        # SSH access
        yandex.vpc.SecurityGroupIngressArgs(
            protocol="TCP",
            description="SSH",
            v4_cidr_blocks=[allowed_ssh_ip],
            port=22,
        ),
        # HTTP access
        yandex.vpc.SecurityGroupIngressArgs(
            protocol="TCP",
            description="HTTP",
            v4_cidr_blocks=["0.0.0.0/0"],
            port=80,
        ),
        # Application port
        yandex.vpc.SecurityGroupIngressArgs(
            protocol="TCP",
            description="App Port",
            v4_cidr_blocks=["0.0.0.0/0"],
            port=5000,
        ),
    ],
    
    egress=[yandex.vpc.SecurityGroupEgressArgs(
        protocol="ANY",
        description="Outbound",
        v4_cidr_blocks=["0.0.0.0/0"],
        from_port=0,
        to_port=65535,
    )]
)

# Create VM instance with public IP
vm = yandex.compute.Instance(
    "devops-vm",
    name=vm_name,
    zone=zone,
    platform_id="standard-v3",
    
    resources=yandex.compute.InstanceResourcesArgs(
        cores=2,
        memory=2,
    ),
    
    boot_disk=yandex.compute.InstanceBootDiskArgs(
        initialize_params=yandex.compute.InstanceBootDiskInitializeParamsArgs(
            image_id="fd8idfirhnddklq0u5nk",  # Ubuntu 24.04 LTS
            size=20,
        ),
    ),
    
    network_interfaces=[yandex.compute.InstanceNetworkInterfaceArgs(
        subnet_id=subnet.id,
        nat=True,  # Enable public IP
        security_group_ids=[security_group.id],
    )],
    
    metadata={
        "ssh-keys": f"ubuntu:{ssh_public_key}",
        "user-data": """#cloud-config
package_update: true
packages:
  - docker.io
  - python3-pip
runcmd:
  - systemctl enable docker
  - systemctl start docker
  - usermod -aG docker ubuntu
"""
    }
)

# Export important values
pulumi.export("vm_public_ip", vm.network_interfaces[0].nat_ip_address)
pulumi.export("vm_private_ip", vm.network_interfaces[0].ip_address)
pulumi.export("ssh_command", vm.network_interfaces[0].nat_ip_address.apply(
    lambda ip: f"ssh ubuntu@{ip}"
))
pulumi.export("vm_id", vm.id)
pulumi.export("network_id", network.id)
pulumi.export("subnet_id", subnet.id)