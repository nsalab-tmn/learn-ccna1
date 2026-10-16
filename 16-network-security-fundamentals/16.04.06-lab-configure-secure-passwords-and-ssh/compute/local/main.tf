# Spins one learn-netsim node on the shared learn-labs Docker network and hands its
# SSH address to the grader via tf-dynamic-params.json (written by learn-lab-deploy
# from these outputs). Mirrors the learn-lab-template sshd reference lab.

terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}

# The lab topology (also uploaded into the container below): device ids drive the
# per-device SSH ports (ssh_base_port + id), exported in outputs.tf.
locals {
  topology      = yamldecode(file("${path.module}/topology.yaml"))
  device_ids    = { for i, d in local.topology.devices : d.name => try(d.id, i) }
  ssh_base_port = 2200
}

# Reads DOCKER_HOST from the environment — the scoped socket-proxy wired by learn-infra.
provider "docker" {}

# The shared lab network created by learn-infra (name pinned as a cross-repo contract).
data "docker_network" "labs" {
  name = "learn-labs"
}

# Per-lab SSH password; surfaced to the learner + grader via tf-dynamic-params.json.
resource "random_password" "ssh" {
  length  = 16
  special = false
}

resource "docker_image" "netsim" {
  name = var.netsim_image
  # Keep an image pulled by the local daemon if present (offline/e2e); the
  # socket-proxy also allows a pull on first use.
  keep_locally = true
}

resource "docker_container" "lab" {
  name  = "lab-${var.instance_id}"
  image = docker_image.netsim.image_id

  # The device boots at its factory hostname so `hostname RTA` is a graded student
  # action. The web canvas (:7681) draws the lab topology and opens an in-page
  # console into the same daemon the grader reaches over SSH.
  env = [
    "NETSIM_SSH_USER=admin",
    "NETSIM_SSH_PASSWORD=${random_password.ssh.result}",
    "NETSIM_SSH_BASE_PORT=${local.ssh_base_port}",
    "NETSIM_ENABLE_WEB=1",
    "NETSIM_TOPOLOGY=/app/topology.yaml",
  ]

  # The lab topology the canvas draws. It sits in this directory because
  # learn-lab-deploy stages only compute/local.
  upload {
    file    = "/app/topology.yaml"
    content = file("${path.module}/topology.yaml")
  }

  networks_advanced {
    name = data.docker_network.labs.name
  }

  labels {
    label = "learn.instance_id"
    value = var.instance_id
  }
  labels {
    label = "learn.material_id"
    value = var.tp_name
  }
}
