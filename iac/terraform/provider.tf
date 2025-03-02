terraform {
  required_version = ">= 1.10.4"
}

############################################
# Provider Configuration
############################################
provider "google" {
  project = var.project_id
  region  = var.region

  default_labels = {
    environment = var.environment
  }
}
