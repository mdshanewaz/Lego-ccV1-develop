output "alb_output" {
  value = {
    alb_target = aws_lb_target_group.ccv1-dev-122022.arn
  }
}