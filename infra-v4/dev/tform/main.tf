module "vpc" {
   source = "./modules/vpc"
   VPC    = var.VPC
}

module "sg" {
  source           = "./modules/sg"
   vpc_id          = module.vpc.vpc_output.vpc_id
   SECURITY_GROUPS = var.SECURITY_GROUPS
}

module "alb" {
  source        = "./modules/alb"
  vpc_id        = module.vpc.vpc_output.vpc_id
  subnet_public = module.vpc.vpc_output.public_subnets
  alb_sg        = module.sg.sg_output.alb_sg_id
  ALB           = var.ALB
}

module "ecs" {
  source        = "./modules/ecs"
  ECS           = var.ECS
  vpc_id        = module.vpc.vpc_output.vpc_id
  subnet_public = module.vpc.vpc_output.public_subnets
  ecs_sg        = module.sg.sg_output.ecs_sg_id
  alb_target    = module.alb.alb_output.alb_target

}
