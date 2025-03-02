variable "project_id" {
  description = "The project ID to deploy resources"
  type        = string
}
variable "region" {
  description = "The region to deploy resources"
  type        = string
  default     = "us-central1"
}
variable "bucket_storage_class" {
  description = "The storage class of the bucket"
  type        = string
  default     = "STANDARD"
}
variable "prefix" {
  description = "The prefix to add to resources"
  type        = string
}

variable "bucket_artifacts_name" {
  description = "The name of the artifacts bucket"
  type        = string
}
variable "environment" {
  description = "The environment to deploy resources"
  type        = string
}

variable "force_destroy" {
  description = "Whether to force destroy the bucket"
  type        = bool
  default     = true
}
