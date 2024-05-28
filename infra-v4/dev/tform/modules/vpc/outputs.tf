output "vpc_output" {
  value = {
    vpc_id            = aws_vpc.ccv1-dev-122022.id
    public_subnets    = aws_subnet.public-ccv1-dev-122022.*
    vpc_azs_available = local.total_az
  }
}
