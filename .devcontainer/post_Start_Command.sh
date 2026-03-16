#! /bin/bash

#used to Create or identify the VPC & Security Groups needed for ECS------->
export DEFAULT_VPC_ID=$(aws ec2 describe-vpcs \
    --filters "Name=isDefault, Values=true" \
    --query "Vpcs[0].VpcId" \
    --output text)

# export CRUD_SERVICE_SG=$(aws ec2 create-security-group \
#     --group-name "crud-srv-sg-2026" \
#     --description "Security Group for Cruddur Services on ECS - 2026" \
#     --vpc-id $DEFAULT_VPC_ID \
#     --query "GroupId" \
#     --output text)

# aws ec2 authorize-security-group-ingress \
# 	--group-id $CRUD_SERVICE_SG \
# 	--protocol tcp \
# 	--port 80 \
# 	--cidr 0.0.0.0/0

export CRUD_SERVICE_SG=$(aws ec2 describe-security-groups \
	--filters Name=group-name,Values=crud-srv-sg \
	--query 'SecurityGroups[*].GroupId' \
	--output text)


export DEFAULT_SUBNET_IDS=$(aws ec2 describe-subnets \
    --filters Name=vpc-id,Values=$DEFAULT_VPC_ID \
	--query 'Subnets[*].SubnetId' \
	--output json | jq -r 'join(",")')
#<-----------------------------------------------------------------------------

#Install Sessions Manager------------------------------------------------------------------------->
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
sudo dpkg -i session-manager-plugin.deb
#<--------------------------------------------------------------------------------------------

