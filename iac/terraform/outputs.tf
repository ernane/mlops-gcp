output "bucket_artifacts" {
  description = "The name of the bucket to store artifacts"
  value       = google_storage_bucket.artifacts.name
}
