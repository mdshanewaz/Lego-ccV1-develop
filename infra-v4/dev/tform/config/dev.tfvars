VPC = {
  VPC_CIDR     = "10.0.0.0/16"
  CIDR_PUBLIC  = ["10.0.1.0/24", "10.0.2.0/24"]
}

SECURITY_GROUPS = {
  ALB_SG = {
    ingress = [
      {
        protocol    = "tcp"
        description = "HTTP from anywhere"
        from_port   = 80
        to_port     = 80
        cidr_block  = ["0.0.0.0/0"]

      },
      {
        protocol    = "tcp"
        description = "HTTPS from anywhere"
        from_port   = 443
        to_port     = 443
        cidr_block  = ["0.0.0.0/0"]
      }
    ]
    
    egress = [
      {
        from_port  = 0
        to_port    = 0
        protocol   = "-1"
        cidr_block = ["0.0.0.0/0"]
      }
    ]
  }

  ECS_SG = {
    ingress = [
      {
        description = "Container Port access"
        from_port   = 5000  
        to_port     = 5000
        protocol    = "tcp"

      }

    ]
    egress = [
      {
        from_port  = 0
        to_port    = 0
        protocol   = "-1"
        cidr_block = ["0.0.0.0/0"]
      }
    ]

  }
}

ECS = {
    CLUSTER_NAME                = "ccv1-dev-122022"
    IMAGE                       = "700158924566.dkr.ecr.us-east-1.amazonaws.com/ccv1/dev/webapp:latest"
    CONTAINERPORT               = 5000
    TASK_DEFINITION_FAMILY_NAME = "ccv1-dev-122022"
    CPU                         = 256
    MEMORY                      = 512
    EXECUTION_ROLE_ARN          = "arn:aws:iam::700158924566:role/ecsTaskExecutionRole"
    CONTAINER_NAME              = "ccv1-dev-122022"
    CONTAINER_CPU               = 256
    CONTAINER_MEMORY            = 512

    SERVICE = {
      NAME          = "ccv1dev"
      DESIRED_COUNT = 2
    }

}

ALB = {
  TARGET_GROUP = {
    NAME_TARGET     = "ccv1-dev-122022"
    PORT_TARGET     = 5000
    PROTOCOL_TARGET = "HTTP"
    TARGET_TYPE     = "ip"
  }

  LOAD_BALANCER = {
    NAME               = "ccv1-dev-122022"
    INTERNAL           = false
    LOAD_BALANCER_TYPE = "application"
  }
  
  // HTTP LISTENERS FOR ALB
  HTTP_LISTENERS = [
    {
      PORT        = 80
      PROTOCOL    = "HTTP"
      ACTION_TYPE = "forward"
    }
  ]
}
