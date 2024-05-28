# we need two security groups
# (1) for ALB(Allow HTTP AND HTTPS)
# ASG(Allow HTTP and SSH)  <<- not sure why we need it

//////////////////////////////////////////////////////
# security groups related to alb
//////////////////////////////////////////////////////
// security group for ALB
resource "aws_security_group" "alb-ccv1-mango" {
  name        = "ccv1-dev-122022"
  description = "Allow HTTP and HTTPS traffic"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${terraform.workspace}-alb-ccv1-mango"
  }
}

# security group rule for ingress aws_security_group/alb-ccv1-dev-122022
resource "aws_security_group_rule" "ingress-ccv1-dev-122022" {
  type              = "ingress"
  count             = length(var.SECURITY_GROUPS.ALB_SG.ingress)
  description       = var.SECURITY_GROUPS.ALB_SG.ingress[count.index].description
  from_port         = var.SECURITY_GROUPS.ALB_SG.ingress[count.index].from_port
  to_port           = var.SECURITY_GROUPS.ALB_SG.ingress[count.index].to_port
  protocol          = var.SECURITY_GROUPS.ALB_SG.ingress[count.index].protocol
  cidr_blocks       = flatten([var.SECURITY_GROUPS.ALB_SG.ingress[count.index].cidr_block])

  security_group_id = aws_security_group.alb-ccv1-dev-122022.id  
}

# security group rule for egress aws_security_group/alb-ccv1-dev-122022
resource "aws_security_group_rule" "egress-ccv1-dev-122022" {
  type              = "egress"
  count             = length(var.SECURITY_GROUPS.ALB_SG.egress)
  from_port         = var.SECURITY_GROUPS.ALB_SG.egress[count.index].from_port
  to_port           = var.SECURITY_GROUPS.ALB_SG.egress[count.index].to_port
  protocol          = var.SECURITY_GROUPS.ALB_SG.egress[count.index].protocol
  cidr_blocks       = flatten([var.SECURITY_GROUPS.ALB_SG.egress[count.index].cidr_block])
  
  security_group_id = aws_security_group.alb-ccv1-dev-122022.id
}


//////////////////////////////////////////////////////
# security groups related to ecs service
# 1. ECS SERVICE
# 2. security group rule for ingress
# 3. security group rule for egress
//////////////////////////////////////////////////////

// ECS SERVICE
resource "aws_security_group" "ecs-ccv1-dev-122022" {
  name        = "ecs-ccv1-dev-122022"
  description = "Allow HTTP  traffic"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${terraform.workspace}-ecs-ccv1-dev-122022"
  }
}

// security group rule for ingress aws_security_group/ecs-ccv1-dev-122022
resource "aws_security_group_rule" "ecs-ccv1-dev-122022" {
  type                     = "ingress"
  count                    = length(var.SECURITY_GROUPS.ECS_SG.ingress)
  description              = var.SECURITY_GROUPS.ECS_SG.ingress[count.index].description
  from_port                = var.SECURITY_GROUPS.ECS_SG.ingress[count.index].from_port
  to_port                  = var.SECURITY_GROUPS.ECS_SG.ingress[count.index].to_port
  protocol                 = var.SECURITY_GROUPS.ECS_SG.ingress[count.index].protocol
  
  source_security_group_id = aws_security_group.alb-ccv1-dev-122022.id
  security_group_id        = aws_security_group.ecs-ccv1-dev-122022.id
}

# security group rule for egress aws_security_group/ecs-ccv1-dev-122022
resource "aws_security_group_rule" "ecs_egress_rules" {
  type              = "egress"
  count             = length(var.SECURITY_GROUPS.ECS_SG.egress)
  from_port         = var.SECURITY_GROUPS.ECS_SG.egress[count.index].from_port
  to_port           = var.SECURITY_GROUPS.ECS_SG.egress[count.index].to_port
  protocol          = var.SECURITY_GROUPS.ECS_SG.egress[count.index].protocol
  cidr_blocks       = flatten([var.SECURITY_GROUPS.ECS_SG.egress[count.index].cidr_block])

  security_group_id        = aws_security_group.ecs-ccv1-dev-122022.id
}

//////////////////////////////////////////////////////
# security groups for RDS database
# 1. 
# 2. security group rule for ingress
# 3. security group rule for egress
//////////////////////////////////////////////////////
resource "aws_security_group" "ccv1-mango-db" {
  description = "security-group--db-instance"

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
  }

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
  }

  name = "security-group--db-instance"

  tags = {
    Env  = "dev"
    Name = "security-group--db-instance"
  }

  vpc_id = aws_vpc.default.id
}
