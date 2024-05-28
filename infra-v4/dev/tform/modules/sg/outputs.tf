output "sg_output" {
  value = {
    alb_sg_id = aws_security_group.alb-sg.id
    ecs_sg_id = aws_security_group.ecs-web-sg.id
  }
}