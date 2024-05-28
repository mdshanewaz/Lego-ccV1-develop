output "ecs_output" {
  value = {
    ecs_service = aws_ecs_service.ccv1-dev-122022.*
  }
}
