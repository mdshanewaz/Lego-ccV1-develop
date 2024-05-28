// Declare the data source for AZ
data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  total_az             = length(data.aws_availability_zones.available.names)
  total_public_subnet  = length(var.VPC.CIDR_PUBLIC)
}

// VPC
resource "aws_vpc" "ccv1-dev-122022" {
  cidr_block            = var.VPC.VPC_CIDR
  instance_tenancy      = "default"
  enable_dns_hostnames  = "true"

  tags = {
    Name = "${terraform.workspace}-ccv1-dev-122022"
  }
}

// VPC is attached to an internet gateway
resource "aws_internet_gateway" "gw-ccv1-dev-122022" {
  vpc_id = aws_vpc.ccv1-dev-122022.id

  tags = {
    Name = "${terraform.workspace}-igw-ccv1-dev-122022"
  }
}

// Configuring public subnet per availability zone
resource "aws_subnet" "public-ccv1-dev-122022" {
  vpc_id                  = aws_vpc.ccv1-dev-122022.id
  cidr_block              = var.VPC.CIDR_PUBLIC[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index % local.total_az]
  count                   = local.total_public_subnet
  map_public_ip_on_launch = "true"
  
  tags = {
    Name = "public-ccv1-dev-122022-${count.index + 1}"
  }
}

// Route Table for Public subnet through internet gateway
resource "aws_route_table" "ccv1-dev-122022" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${terraform.workspace}-public-route-table"
  }
}

resource "aws_route" "public" {
  route_table_id          = aws_route_table.public.id
  destination_cidr_block  = "0.0.0.0/0"
  gateway_id              = aws_internet_gateway.gw-ccv1-dev-122022.id
}

// route table associations for public subnets
resource "aws_route_table_association" "public-ccv1-dev-122022" {
  count          = length(var.VPC.CIDR_PUBLIC)
  subnet_id      = aws_subnet.public-ccv1-dev-122022.*.id[count.index]
  route_table_id = aws_route_table.ccv1-dev-122022.id
}

////////////////////////////////////////////////////////////////////////
# unresolved following
# For private subnet,we need to attach NAT gateway to connect to the outside world
# Not sure if we need the following section 
# because we donot need private subnets

# // NAT 
# resource "aws_nat_gateway" "nat-ccv1-dev-122022" {
#   allocation_id = aws_eip.nat_eip_ccv1_dev_122022.id
#   subnet_id     = aws_subnet.public-ccv1-dev-122022.0.id
#   depends_on    = [aws_internet_gateway.gw-ccv1-dev-122022]

#   tags = {
#     Name = "${terraform.workspace}-nat"
#   }
# }

# //Elastic IP for NAT 
# resource "aws_eip" "nat_eip_ccv1_dev_122022" {
#   vpc        = true
#   depends_on = [aws_internet_gateway.gw-ccv1-dev-122022]
# }
