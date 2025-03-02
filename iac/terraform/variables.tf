variable "project_id" {
  description = "The project ID to deploy resources"
  type        = string
}

variable "region" {
  description = "The region to deploy resources"
  type        = string
  default     = "us-central1"
}


variable "storage_class" {
  description = "The storage class of the bucket"
  type        = string
  default     = "STANDARD"
}
