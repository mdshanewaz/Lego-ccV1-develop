# Create ALB
resource "aws_alb" "ccv1-dev-122022" {
  name               = var.ALB.LOAD_BALANCER.NAME
  internal           = var.ALB.LOAD_BALANCER.INTERNAL
  load_balancer_type = var.ALB.LOAD_BALANCER.LOAD_BALANCER_TYPE
  security_groups    = [var.alb_sg]
  subnets            = [for subnet in var.subnet_public : subnet.id]

  tags = {
    Name = "${terraform.workspace}-ccv1-dev-122022"
  }
}

# Create Target Group
resource "aws_alb_target_group" "ccv1-dev-122022" {
  name        = var.ALB.TARGET_GROUP.NAME_TARGET
  port        = var.ALB.TARGET_GROUP.PORT_TARGET
  protocol    = var.ALB.TARGET_GROUP.PROTOCOL_TARGET
  target_type = var.ALB.TARGET_GROUP.TARGET_TYPE
  vpc_id      = var.vpc_id
}

# HTTP LISTENER FOR ALB
resource "aws_alb_listener" "ccv1-dev-122022" {
  count             = length(var.ALB.HTTP_LISTENERS)
  load_balancer_arn = aws_lb.ccv1-dev-122022.arn
  port              = var.ALB.HTTP_LISTENERS[count.index]["PORT"]
  protocol          = var.ALB.HTTP_LISTENERS[count.index]["PROTOCOL"]

  # dynamic "default_action" {
  #   for_each = [var.ALB.HTTP_LISTENERS[count.index]]
  #   content {
  #     type             = lookup(default_action.value, "ACTION_TYPE", "forward")
  #     target_group_arn = aws_lb_target_group.ccv1-dev-122022.arn
  #     dynamic "redirect" {
  #       for_each = length(keys(lookup(default_action.value, "REDIRECT", {}))) == 0 ? [] : [lookup(default_action.value, "REDIRECT", {})]
  #       content {
  #         port        = lookup(redirect.value, "PORT", null)
  #         protocol    = lookup(redirect.value, "PROTOCOL", null)
  #         status_code = redirect.value.STATUS_CODE
  #       }
  #     }
  #     dynamic "fixed_response" {
  #       for_each = length(keys(lookup(default_action.value, "FIXED_RESPONSE", {}))) == 0 ? [] : [lookup(default_action.value, "FIXED_RESPONSE", {})]
  #       content {
  #         content_type = fixed_response.value.CONTENT_TYPE
  #         message_body = lookup(fixed_response.value, "MESSAGE_BODY", null)
  #         status_code  = lookup(fixed_response.value, "STATUS_CODE", null)
  #       }
  #     }
  #   }
  # }

  default_action {
    target_group_arn  = aws_alb_target_group.ccv1-dev-122022.id
    type              = "forward"
  }


}
