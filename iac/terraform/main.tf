############################################
# Google Cloud Storage Bucket
############################################
resource "google_storage_bucket" "artifacts" {
  name          = "${var.prefix}-${var.bucket_artifacts_name}"
  location      = var.region
  storage_class = var.bucket_storage_class
  force_destroy = var.force_destroy
}

############################################
# Google Cloud Composer Environment
############################################
resource "google_composer_environment" "this" {
  name   = "${var.prefix}-${var.workflow_name}"
  region = var.region

  storage_config {
    bucket = google_storage_bucket.artifacts.name
  }

  config {
    recovery_config {
      scheduled_snapshots_config {
        enabled = false
      }
    }

    node_config {
      service_account = var.sa_admin
    }

    software_config {
      image_version = "composer-3-airflow-2.10.2-build.9"

      airflow_config_overrides = {}
      env_variables            = {}
      pypi_packages            = {}
    }
  }
}
