terraform {
  required_providers {
    linode = {
    source  = "linode/linode"
    }
  }
}

variable "linode_api_key" {
  type = string
}

provider "linode" {
  token = var.linode_api_key
}

variable "solve_server_port" {
  type = string
  default = "40863"
}

variable "turn_key_0_ip" {
  type = string
  default = "vault1.momandpopsflags.ca"
}

variable "turn_key_1_ip" {
  type = string
  default = "vault2.momandpopsflags.ca"
}

variable "turn_key_2_ip" {
  type = string
  default = "vault3.momandpopsflags.ca"
}

variable "root_password" {
  type = string
}

variable "authorized_keys" {
  type = list(string)
  default = [
    ""
  ]
}

resource "linode_instance" "turn_key_solve_0" {
  label = "turn-key-solve-0"
  image = "linode/debian11"
  region = "ca-central"
  type = "g6-nanode-1"
  authorized_keys = var.authorized_keys
  root_pass = var.root_password

  connection {
    type = "ssh"
    user = "root"
    private_key = file("files/keys/id_ed25519_terraform")
    host = self.ip_address
  }

  provisioner "file" {
    source = "files/solve.py"
    destination = "/root/solve.py"
  }

  provisioner "file" {
    source = "files/solve-setup.sh"
    destination = "/root/solve-setup.sh"
  }

  provisioner "file" {
    source = "files/server.py"
    destination = "/root/server.py"
  }

  provisioner "file" {
    source = "files/server-setup.sh"
    destination = "/root/server-setup.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "bash /root/solve-setup.sh 0 ${var.turn_key_0_ip} http://${var.solve_server_dns}:${var.solve_server_port}",
      "bash /root/server-setup.sh"
    ]
  }
}

resource "linode_instance" "turn_key_solve_1" {
  label = "turn-key-solve-1"
  image = "linode/debian11"
  region = "ap-south"
  type = "g6-nanode-1"
  authorized_keys = var.authorized_keys
  root_pass = var.root_password

  connection {
    type = "ssh"
    user = "root"
    private_key = file("files/keys/id_ed25519_terraform")
    host = self.ip_address
  }

  provisioner "file" {
    source = "files/solve.py"
    destination = "/root/solve.py"
  }

  provisioner "file" {
    source = "files/solve-setup.sh"
    destination = "/root/solve-setup.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "bash /root/solve-setup.sh 1 ${var.turn_key_1_ip} http://${var.solve_server_dns}:${var.solve_server_port}"
    ]
  }
}

resource "linode_instance" "turn_key_solve_2" {
  label = "turn-key-solve-2"
  image = "linode/debian11"
  region = "eu-west"
  type = "g6-nanode-1"
  authorized_keys = var.authorized_keys
  root_pass = var.root_password

  connection {
    type = "ssh"
    user = "root"
    private_key = file("files/keys/id_ed25519_terraform")
    host = self.ip_address
  }

  provisioner "file" {
    source = "files/solve.py"
    destination = "/root/solve.py"
  }

  provisioner "file" {
    source = "files/solve-setup.sh"
    destination = "/root/solve-setup.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "bash /root/solve-setup.sh 2 ${var.turn_key_2_ip} http://${var.solve_server_dns}:${var.solve_server_port}"
    ]
  }
}

output "turn_key_solve_0_ipv4" {
  value = linode_instance.turn_key_solve_0.ip_address
}

output "turn_key_solve_1_ipv4" {
  value = linode_instance.turn_key_solve_1.ip_address
}

output "turn_key_solve_2_ipv4" {
  value = linode_instance.turn_key_solve_2.ip_address
}
