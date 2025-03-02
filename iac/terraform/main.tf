############################################
# Google Cloud Storage Bucket
############################################
resource "google_storage_bucket" "artifacts" {
  name          = "${var.prefix}-${var.bucket_artifacts_name}"
  location      = var.region
  storage_class = var.bucket_storage_class
  force_destroy = var.force_destroy
}
