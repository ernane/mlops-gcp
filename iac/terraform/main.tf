############################################
# Google Cloud Storage Bucket
############################################
resource "google_storage_bucket" "artifacts" {
  name          = "ml-platform-artifacts"
  location      = var.region
  storage_class = var.storage_class
}
