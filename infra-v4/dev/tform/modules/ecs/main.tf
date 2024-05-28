# define ecs cluster
resource "aws_ecs_cluster" "ccv1-dev-122022" {
    name = var.ECS.CLUSTER_NAME
    setting {
        name  = "containerInsights"
        value = "enabled"
    }

    lifecycle {
        create_before_destroy = true
    }

}

# define ecs task definition
resource "aws_ecs_task_definition" "ccv1-dev-122022" {
    family                      = var.ECS.TASK_DEFINITION_FAMILY_NAME
    requires_compatibilities    = ["FARGATE"]
    network_mode                = "awsvpc"
    cpu                         = var.ECS.CPU
    memory                      = var.ECS.MEMORY
    execution_role_arn          = var.ECS.EXECUTION_ROLE_ARN

    container_definitions = jsonencode([
        {
            name      = var.ECS.CONTAINER_NAME
            image     = var.ECS.IMAGE
            cpu       = var.ECS.CONTAINER_CPU
            memory    = var.ECS.CONTAINER_MEMORY
            essential = true
            portMappings = [
                { 
                    containerPort   = var.ECS.CONTAINERPORT 
                    hostPort        = 5000
                }
            ]
            logConfiguration: {
                logDriver: "awslogs",
                options: {
                    awslogs-group:              "/ecs/testdemo",
                    awslogs-region:             "us-east-1",
                    awslogs-stream-prefix:      "ecs"
                }
            }

        }
    ])
}

# define ecs service
resource "aws_ecs_service" "ccv1-dev-122022" {
    name            = var.ECS.SERVICE.NAME
    cluster         = aws_ecs_cluster.ecs.id
    task_definition = aws_ecs_task_definition.ccv1-dev-122022.arn
    desired_count   = var.ECS.SERVICE.DESIRED_COUNT
    launch_type     = "FARGATE"
    
    network_configuration {
        subnets          =  [for subnet in var.subnet_public : subnet.id]
        assign_public_ip =  true
        security_groups  =  [var.ecs_sg]
    }

    load_balancer {
        target_group_arn = var.alb_target
        container_name   = var.ECS.CONTAINER_NAME 
        container_port   = var.ECS.CONTAINERPORT
    }

}
