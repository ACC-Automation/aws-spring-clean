import boto3
from botocore.exceptions import ClientError

class ec2:
    def __init__(self, resourceType, region, resourceName, delete_functions):
        self.resourceType = resourceType
        self.region = region
        self.resourceName = resourceName
        self.delete_functions = delete_functions
        self.ec2 = boto3.client('ec2')
    
    def delete_action(self):
        #ec2_functions = dir(self.ec2)
        #for ec2_function in ec2_functions:
        #print(f"function name= {ec2_function}, {self.resourceType}, {self.resourceName}")
        delete_function = self.delete_functions[self.resourceType]['delete']
        status = 'false'
        print(delete_function)
        if 'terminate_instances' in delete_function:
            #print(f"function name= {ec2_function}, {self.resourceType}, {self.resourceName}")
            try:
                self.ec2.terminate_instances(
                    InstanceIds=[
                        self.resourceName
                    ]
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_security_group' in delete_function:
            try:
                self.ec2.delete_security_group(
                    GroupId=self.resourceName
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_client_vpn_endpoint' in delete_function:
            try:
                self.ec2.delete_client_vpn_endpoint(
                    ClientVpnEndpointId=self.resourceName,
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_client_vpn_route' in delete_function:
            try:
                response = self.ec2.describe_client_vpn_routes(
                    ClientVpnEndpointId=self.resourceName
                )
                cidr_block = response['Routes'][0]['DestinationCidr']
                self.ec2.delete_client_vpn_route(
                    ClientVpnEndpointId=self.resourceName,
                    #TargetVpcSubnetId='string',
                    DestinationCidrBlock=cidr_block
                    #DryRun=True|False
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_traffic_mirror_filter' in delete_function:
            try:
                self.ec2.delete_traffic_mirror_filter(
                    TrafficMirrorFilterId=self.resourceName,
                    DryRun=True|False
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_traffic_mirror_filter_rule' in delete_function:
            try:
                self.ec2.delete_traffic_mirror_filter_rule(
                    TrafficMirrorFilterRuleId=self.resourceName
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_traffic_mirror_filter_rule' in delete_function:
            try:
                self.ec2.delete_traffic_mirror_session(
                    TrafficMirrorSessionId=self.resourceName
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_traffic_mirror_target' in delete_function:
            try:
                self.ec2.delete_traffic_mirror_target(
                    TrafficMirrorTargetId=self.resourceName
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        #elif 'delete_traffic_mirror_target' in delete_function:
        #    
        #    status = 'true'
        else:
            print(f"{delete_function} not supported")
        print(f"Resource Type: {self.resourceType} of resourceName: {self.resourceName} is deleted")
        return status
