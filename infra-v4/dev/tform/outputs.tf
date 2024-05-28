output "output_root_data" {
  value = {
    vpc_id            = module.vpc.vpc_output.vpc_id
    public_subnet     = module.vpc.vpc_output.public_subnets.*
    vpc_azs_available = module.vpc.vpc_output.vpc_azs_available
    alb_target        = module.alb.alb_output.alb_target
    ecs_service       = module.ecs.ecs_output.ecs_service.*
  }
}