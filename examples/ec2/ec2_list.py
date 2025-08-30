#!/usr/bin/env python3
"""
AWS EC2 Instance Lister

This script uses Boto3 to list all EC2 instances in your AWS account.
It displays key information about each instance including instance ID, 
type, state, and name tag.

Prerequisites:
- AWS credentials configured (via AWS CLI, environment variables, or IAM role)
- boto3 library installed
"""

import boto3
import sys
from botocore.exceptions import ClientError, NoCredentialsError


def get_ec2_instances(region='us-east-1'):
    """
    Retrieve all EC2 instances from the specified region.
    
    Args:
        region (str): AWS region to query (default: us-east-1)
    
    Returns:
        list: List of EC2 instance dictionaries
    """
    try:
        # Create EC2 client
        ec2_client = boto3.client('ec2', region_name=region)
        
        # Describe all instances
        response = ec2_client.describe_instances()
        
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance)
        
        return instances
    
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
        print("You can configure credentials using:")
        print("1. AWS CLI: aws configure")
        print("2. Environment variables: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        print("3. IAM role (if running on EC2)")
        sys.exit(1)
    
    except ClientError as e:
        print(f"AWS Error: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def get_instance_name(instance):
    """
    Extract the Name tag from an EC2 instance.
    
    Args:
        instance (dict): EC2 instance dictionary
    
    Returns:
        str: Instance name or 'No Name' if not found
    """
    if 'Tags' in instance:
        for tag in instance['Tags']:
            if tag['Key'] == 'Name':
                return tag['Value']
    return 'No Name'


def display_instances(instances, region):
    """
    Display EC2 instances in a formatted table.
    
    Args:
        instances (list): List of EC2 instance dictionaries
        region (str): AWS region name
    """
    if not instances:
        print(f"No EC2 instances found in region: {region}")
        return
    
    print(f"\nEC2 Instances in region: {region}")
    print("=" * 80)
    print(f"{'Instance ID':<20} {'Name':<25} {'Type':<15} {'State':<15} {'AZ':<15}")
    print("-" * 80)
    
    for instance in instances:
        instance_id = instance['InstanceId']
        instance_name = get_instance_name(instance)
        instance_type = instance['InstanceType']
        state = instance['State']['Name']
        availability_zone = instance['Placement']['AvailabilityZone']
        
        print(f"{instance_id:<20} {instance_name:<25} {instance_type:<15} {state:<15} {availability_zone:<15}")
    
    print(f"\nTotal instances: {len(instances)}")


def main():
    """
    Main function to execute the EC2 listing application.
    """
    print("AWS EC2 Instance Lister")
    print("=====================")
    
    # You can modify this to use a different region or get it from command line arguments
    region = 'us-east-1'
    
    # Allow region to be specified as command line argument
    if len(sys.argv) > 1:
        region = sys.argv[1]
        print(f"Using region: {region}")
    else:
        print(f"Using default region: {region}")
        print("To specify a different region, run: python ec2_list.py <region-name>")
    
    try:
        # Get all EC2 instances
        instances = get_ec2_instances(region)
        
        # Display the instances
        display_instances(instances, region)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
