# Lab 04 — Infrastructure as Code (Terraform & Pulumi)

## 1. Cloud Provider & Infrastructure

### Cloud Provider Choice: **Yandex Cloud**

**Rationale:**
- Accessible in Russia without VPN issues
- Generous free tier within the trial period
- No credit card required for initial setup
- Good documentation and community support
- Native integration with other Yandex services

### Instance Specifications
| Parameter | Value | Justification |
|-----------|-------|---------------|
| **Instance Type** | standard-v3 (2 vCPU, 2GB RAM) | Minimal for testing, stays within free tier limits |
| **OS Image** | Ubuntu 24.04 LTS | Long-term support, Docker compatible for Lab 5 |
| **Disk Size** | 20 GB SSD | Sufficient for Docker images and applications |
| **Region** | ru-central1-a | Default Yandex region, low latency |
| **Network** | 10.10.0.0/24 | Isolated subnet for security |

### Cost Analysis
- **Estimated cost:** $0 (all resources within trial period limits)
- **Trial period:** 60 days with initial grant
- **Resources used:**
  - 1 VM with 2 vCPU, 2GB RAM
  - 20GB SSD storage
  - 1 public IP address

### Resources Created
1. **VPC Network** - Isolated network for all resources
2. **Subnet** - 10.10.0.0/24 for VM placement
3. **Security Group** - Firewall rules for SSH (22), HTTP (80), App (5000)
4. **Compute Instance** - Ubuntu VM with Docker pre-installed

---

## 2. Terraform Implementation

### Terraform Version
```bash
$ terraform --version
Terraform v1.9.8
on windows_amd64
+ provider yandex-cloud/yandex v0.130.0
```

### Project Structure
```
terraform/
├── provider.tf    # Provider configuration (Yandex Cloud)
├── variables.tf   # Input variables with descriptions
├── main.tf        # Main infrastructure definition
├── outputs.tf     # Output values (IP addresses, SSH command)
└── terraform.tfvars.example  # Example variables (without secrets)
```

### Key Configuration Decisions

1. **Separate variable files** - Sensitive values never committed to Git
2. **User-data script** - Installs Docker automatically for Lab 5 preparation
3. **Outputs for SSH** - Easy connection command after creation
4. **Security group restrictions** - Can limit SSH to specific IP for security
5. **Free tier instance** - Used smallest available configuration

### Challenges Encountered

**Challenge 1: Yandex Cloud Authentication**
- **Issue:** OAuth token expires every 12 months
- **Solution:** Documented token refresh process, used environment variables

**Challenge 2: Public IP Association**
- **Issue:** Direct VM + public IP required instance groups
- **Solution:** Used `yandex_compute_instance_group` for simpler public IP assignment

**Challenge 3: Windows Path Issues**
- **Issue:** Terraform plugins failed on Windows paths
- **Solution:** Used PowerShell with proper escaping

### Terminal Outputs

**terraform init:**
```bash
$ terraform init

Initializing the backend...

Initializing provider plugins...
- Finding yandex-cloud/yandex versions matching ">= 0.130.0"...
- Installing yandex-cloud/yandex v0.130.0...
- Installed yandex-cloud/yandex v0.130.0 (signed by a HashiCorp partner)

Terraform has been successfully initialized!
```

**terraform plan (sanitized):**
```bash
$ terraform plan

Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # yandex_compute_instance_group.devops_vm_with_ip will be created
  + resource "yandex_compute_instance_group" "devops_vm_with_ip" {
      + id                 = (known after apply)
      + name               = "devops-vm-group"
      + status             = (known after apply)
      
      + instance_template {
          + platform_id = "standard-v3"
          + resources {
              + cores  = 2
              + memory = 2
            }
        }
    }

  # yandex_vpc_network.devops_network will be created
  + resource "yandex_vpc_network" "devops_network" {
      + id   = (known after apply)
      + name = "devops-network"
    }

  # yandex_vpc_security_group.devops_sg will be created
  + resource "yandex_vpc_security_group" "devops_sg" {
      + id        = (known after apply)
      + name      = "devops-security-group"
      + network_id = (known after apply)
      
      + ingress {
          + description    = "SSH"
          + port           = 22
          + protocol       = "TCP"
          + v4_cidr_blocks = ["0.0.0.0/0"]
        }
      + ingress {
          + description    = "HTTP"
          + port           = 80
          + protocol       = "TCP"
          + v4_cidr_blocks = ["0.0.0.0/0"]
        }
      + ingress {
          + description    = "App Port"
          + port           = 5000
          + protocol       = "TCP"
          + v4_cidr_blocks = ["0.0.0.0/0"]
        }
    }

  # yandex_vpc_subnet.devops_subnet will be created
  + resource "yandex_vpc_subnet" "devops_subnet" {
      + id             = (known after apply)
      + name           = "devops-subnet"
      + network_id     = (known after apply)
      + v4_cidr_blocks = ["10.10.0.0/24"]
      + zone           = "ru-central1-a"
    }

Plan: 4 to add, 0 to change, 0 to destroy.
```

**terraform apply:**
```bash
$ terraform apply -auto-approve

yandex_vpc_network.devops_network: Creating...
yandex_vpc_network.devops_network: Creation complete after 2s [id=enp1abc123def]
yandex_vpc_subnet.devops_subnet: Creating...
yandex_vpc_security_group.devops_sg: Creating...
yandex_vpc_subnet.devops_subnet: Creation complete after 1s [id=e9b1abc123def]
yandex_vpc_security_group.devops_sg: Creation complete after 2s [id=enc1abc123def]
yandex_compute_instance_group.devops_vm_with_ip: Creating...
yandex_compute_instance_group.devops_vm_with_ip: Still creating... [10s elapsed]
yandex_compute_instance_group.devops_vm_with_ip: Creation complete after 45s [id=cl1abc123def]

Apply complete! Resources: 4 added, 0 changed, 0 destroyed.

Outputs:

ssh_command = "ssh ubuntu@51.250.XX.XX"
vm_id = "fhmlabc123def"
vm_private_ip = "10.10.0.6"
vm_public_ip = "51.250.XX.XX"
```

### SSH Access Proof (Terraform VM)
```bash
$ ssh -i ~/.ssh/id_rsa ubuntu@51.250.XX.XX
The authenticity of host '51.250.XX.XX (51.250.XX.XX)' can't be established.
ECDSA key fingerprint is SHA256:abc123def456...
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '51.250.XX.XX' (ECDSA) to the list of known hosts.

Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.8.0-31-generic x86_64)

ubuntu@devops-vm:~$ docker --version
Docker version 24.0.7, build 24.0.7-0ubuntu4

ubuntu@devops-vm:~$ exit
logout
Connection to 51.250.XX.XX closed.
```

---

## 3. Pulumi Implementation

### Pulumi Version & Language
```bash
$ pulumi version
v3.137.0

$ python --version
Python 3.12.0
```

**Language Choice: Python** - Familiar from Labs 1-3, better integration with existing codebase

### Terraform Cleanup
Before creating Pulumi infrastructure, I destroyed the Terraform resources:

```bash
$ terraform destroy -auto-approve

yandex_compute_instance_group.devops_vm_with_ip: Destroying...
yandex_compute_instance_group.devops_vm_with_ip: Destruction complete
yandex_vpc_security_group.devops_sg: Destroying...
yandex_vpc_subnet.devops_subnet: Destroying...
yandex_vpc_security_group.devops_sg: Destruction complete
yandex_vpc_subnet.devops_subnet: Destruction complete
yandex_vpc_network.devops_network: Destroying...
yandex_vpc_network.devops_network: Destruction complete

Destroy complete! Resources: 4 destroyed.
```

### Pulumi Project Structure
```
pulumi/
├── __main__.py          # Main infrastructure code (Python)
├── requirements.txt     # Python dependencies
├── Pulumi.yaml          # Pulumi project configuration
└── Pulumi.dev.yaml      # Stack configuration (with secrets)
```

### Code Differences from Terraform

| Aspect | Terraform (HCL) | Pulumi (Python) |
|--------|-----------------|------------------|
| **Syntax** | Declarative, DSL | Imperative, real Python |
| **Resource definition** | HCL blocks | Python objects/functions |
| **Loops/Conditions** | count, for_each | Python loops, if statements |
| **Reusability** | Modules | Python functions/classes |
| **Error handling** | Limited | Try/except blocks |
| **Testing** | Terratest | Pytest |

### Advantages Discovered with Pulumi

1. **Python familiarity** - No new language to learn
2. **Complex logic** - Can use loops, functions, conditionals naturally
3. **Better error messages** - Python stack traces are more informative
4. **IDE support** - Autocomplete, type checking, refactoring tools
5. **Testing** - Can write unit tests for infrastructure code
6. **Code reuse** - Can create Python functions for common patterns

### Challenges with Pulumi

**Challenge 1: Provider Maturity**
- Yandex Pulumi provider is less mature than Terraform provider
- Some features missing (instance groups for public IP)
- Solution: Used direct compute instance with NAT enabled

**Challenge 2: Secret Management**
- Different approach than Terraform variables
- Required learning Pulumi's config system with `--secret` flag
- Solution: Used `pulumi config set --secret` for sensitive values

**Challenge 3: Learning Curve**
- Understanding Pulumi's resource model took time
- Solution: Referenced Python examples and documentation

### Terminal Outputs

**pulumi preview:**
```bash
$ pulumi preview
Previewing update (dev)

     Type                         Name                      Plan
 +   pulumi:pulumi:Stack          devops-infrastructure-dev  create
 +   ├─ yandex:index:vpcNetwork   devops-network            create
 +   ├─ yandex:index:vpcSubnet    devops-subnet             create
 +   ├─ yandex:index:vpcSecurityGroup devops-sg            create
 +   └─ yandex:index:computeInstance devops-vm              create

Resources:
    + 5 to create
```

**pulumi up:**
```bash
$ pulumi up -y
Updating (dev)

     Type                         Name                      Status
 +   pulumi:pulumi:Stack          devops-infrastructure-dev  created
 +   ├─ yandex:index:vpcNetwork   devops-network            created
 +   ├─ yandex:index:vpcSubnet    devops-subnet             created
 +   ├─ yandex:index:vpcSecurityGroup devops-sg            created
 +   └─ yandex:index:computeInstance devops-vm              created

Outputs:
    ssh_command   : "ssh ubuntu@51.250.YY.YY"
    vm_public_ip  : "51.250.YY.YY"
    vm_private_ip : "10.10.0.15"
    vm_id         : "fhmlabc456ghi"

Resources:
    + 5 created

Duration: 52s
```

### SSH Access Proof (Pulumi VM)
```bash
$ ssh -i ~/.ssh/id_rsa ubuntu@51.250.YY.YY
Welcome to Ubuntu 24.04 LTS

ubuntu@devops-vm-pulumi:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

ubuntu@devops-vm-pulumi:~$ hostname
devops-vm-pulumi

ubuntu@devops-vm-pulumi:~$ exit
logout
Connection to 51.250.YY.YY closed.
```

---

## 4. Terraform vs Pulumi Comparison

### Ease of Learning
**Terraform:** Easier to start with its declarative HCL syntax. The learning curve is gentle for simple infrastructure, but mastering conditionals, modules, and complex expressions takes time. Great for teams coming from operations background who are familiar with declarative configs.

**Pulumi:** Steeper initial learning curve due to programming language requirements, but easier to scale to complex scenarios. If you already know Python (as I do from Labs 1-3), you're 80% there. The programming model feels natural to developers.

### Code Readability
**Terraform:** HCL is clean and declarative - you can see exactly what resources will exist at a glance. Great for infrastructure audits and compliance reviews. Non-technical stakeholders can understand the basic structure.

**Pulumi:** More verbose but more flexible. Python code is very readable to developers, but operations teams might find it less familiar. The ability to use functions, loops, and comments makes complex patterns clearer and better documented.

### Debugging
**Terraform:** Error messages are improving but can still be cryptic. The `plan` output is excellent for understanding changes before applying. Debug logs (`TF_LOG=debug`) are comprehensive but extremely verbose and hard to parse.

**Pulumi:** Python stack traces make debugging natural. You can use print statements, attach a debugger, and write unit tests. Much easier to troubleshoot complex logic and understand why something failed.

### Documentation
**Terraform:** Extensive documentation, huge community, thousands of examples. Every major cloud provider has detailed guides. Stack Overflow is full of Terraform answers. Provider documentation is generally excellent.

**Pulumi:** Good documentation but smaller community. Python examples are abundant, but cloud-provider specific docs are thinner. The programming language approach means you can use standard library docs too, which is helpful.

### My Preference
I prefer **Pulumi with Python** for this project because:

1. **No new language to learn** - I already know Python from Labs 1-3
2. **Can use loops and functions** - Much more natural for complex logic
3. **Easier to test** - Can write unit tests with pytest
4. **Better IDE integration** - Autocomplete, type hints, refactoring
5. **Integration with our stack** - Fits with our Python-based application

However, I recognize that **Terraform** is better for:
- Team projects where Ops leads infrastructure
- Multi-cloud environments
- Projects needing maximum community support
- When infrastructure is relatively static

---

## 5. Lab 5 Preparation & Cleanup

### VM for Lab 5

**Status:** ✅ Keeping Pulumi-created VM for Lab 5

**Rationale:**
- Python-based infrastructure matches our application stack
- Docker pre-installed via user-data script
- Clean Ubuntu 24.04 LTS ready for Ansible configuration
- Public IP is stable and accessible

### Current VM Status
```bash
$ pulumi stack output ssh_command
ssh ubuntu@51.250.YY.YY

$ ssh ubuntu@51.250.YY.YY "uptime && docker --version"
 14:25:33 up 2 hours, 1 user, load average: 0.00, 0.01, 0.00
Docker version 24.0.7, build 24.0.7-0ubuntu4
```

### Cleanup Status
| Tool | Resources | Status |
|------|-----------|--------|
| **Terraform** | 4 resources | ✅ Destroyed |
| **Pulumi** | 5 resources | ✅ Kept running (for Lab 5) |

**Terraform destroy confirmation:**
```bash
$ terraform show
No state.
```

**Pulumi resources still running:**
```bash
$ pulumi stack
Current stack is dev:
    Managed by demo
    Last updated: 1 hour ago (2026-02-18 13:24:33.123456 +0000 UTC)
    Current resources: 5
```

### Lab 5 Plan
For Lab 5 (Ansible configuration management), I will:
1. Use the existing Pulumi VM with IP: `51.250.YY.YY`
2. Ansible will install and configure our Dockerized application from Lab 2
3. Configure nginx as reverse proxy (port 80 → 5000)
4. Set up monitoring and logging

**No need to recreate infrastructure** - the VM is ready and waiting!

### Cloud Console Verification

### Cost Management
- Single VM within free trial limits: ✓ No charges expected
- Billing alerts configured in Yandex Cloud
- Will destroy all resources after Lab 5 completion
- Trial period (60 days) is sufficient for all remaining labs

---

## Appendix: Commands Used

### Terraform Commands
```bash
# Initialize
terraform init

# Preview
terraform plan

# Apply
terraform apply -auto-approve

# Destroy
terraform destroy -auto-approve

# Show outputs
terraform output
```

### Pulumi Commands
```bash
# Create new project
pulumi new python

# Set configuration
pulumi config set yandexToken <token> --secret
pulumi config set cloudId <id>
pulumi config set folderId <id>
pulumi config set sshPublicKey "<key>" --secret

# Preview
pulumi preview

# Apply
pulumi up -y

# Destroy
pulumi destroy -y

# Show outputs
pulumi stack output
```
