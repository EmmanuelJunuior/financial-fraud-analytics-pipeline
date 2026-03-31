# variables.tf

# Google Cloud Project ID
variable "project_id" {
  description = "The GCP project ID where resources will be created"
  type        = string
}

# GCP region
variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "us-central1"
}

# Name of the BigQuery dataset
variable "bigquery_dataset" {
  description = "The name of the BigQuery dataset to store processed fraud data"
  type        = string
  default     = "fraud_analytics"
}

# Name of the storage bucket for raw data
variable "raw_data_bucket" {
  description = "GCS bucket name for storing raw input data"
  type        = string
  default     = "fraud-raw-data"
}

# Name of the storage bucket for processed/analytics data
variable "processed_data_bucket" {
  description = "GCS bucket name for storing processed/analytics data"
  type        = string
  default     = "fraud-processed-data"
}

# Airflow environment name
variable "airflow_env_name" {
  description = "Name of the Cloud Composer/Airflow environment"
  type        = string
  default     = "fraud-airflow-env"
}

# Kestra workflow directory path (optional override)
variable "kestra_workflow_path" {
  description = "Path to Kestra workflow YAML files"
  type        = string
  default     = "kestra/workflows"
}

# Docker image for custom Airflow tasks (if any)
variable "docker_image" {
  description = "Docker image for Airflow custom tasks"
  type        = string
  default     = "gcr.io/my-project/fraud-airflow:latest"
}

# Enable debug/logging for deployments
variable "enable_debug" {
  description = "Enable debug mode for Terraform deployments"
  type        = bool
  default     = false
}
