variable "region" {
  description = "AWS Region"
  default     = "us-east-2"
  type        = string
}

variable "app_name" {
  description = "generate users lambda"
  type        = string
  default     = "generate-users"

}

variable "timeout" {

  description = "timeout for lambda function in seconds"
  default     = 300
  type        = number
}

variable "memory_size" {
  description = "momory size for lambda function in MB"
  default     = 512
  type        = number
}