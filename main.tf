terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = "1c6508e264c30fcc6249f937d2d4eb2cacd6ebbf25b1b7cd300b777cb2339195"
}

resource "digitalocean_droplet" "server" {
  image     = "debian-11-x64"
  name      = "dhdb-museum-collections"
  region    = "sfo3"
  size      = "s-8vcpu-16gb"
  ssh_keys  = ["50:ba:8f:a6:1a:e5:82:f8:57:5b:a0:c5:6e:00:f6:99"]
  user_data = file("provision.sh")

  connection {
    host        = self.ipv4_address
    user        = "root"
    type        = "ssh"
    timeout     = "2m"
    private_key = file("~/.ssh/id_rsa")
  }

  provisioner "file" {
    source      = "~/.dolt"
    destination = "/root"
  }
}

output "server_ip" {
  value = resource.digitalocean_droplet.server.ipv4_address
}

