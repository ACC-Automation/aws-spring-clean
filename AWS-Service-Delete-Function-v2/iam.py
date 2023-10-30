import boto3
from botocore.exceptions import ClientError

class iam:
    def __init__(self, resourceType, region, resourceName, delete_functions):
        self.resourceType = resourceType
        self.region = region
        self.resourceName = resourceName
        self.delete_functions = delete_functions
        self.iam = boto3.client('iam')
    
    def delete_action(self):
        #ec2_functions = dir(self.ec2)
        #for ec2_function in ec2_functions:
        #print(f"function name= {ec2_function}, {self.resourceType}, {self.resourceName}")
        delete_function = self.delete_functions[self.resourceType]['delete']
        status = 'false'
        print(delete_function)
        if 'delete_access_key' in delete_function:
            #print(f"function name= {ec2_function}, {self.resourceType}, {self.resourceName}")
            try:
                self.iam.delete_access_key(
                    AccessKeyId=self.resourceName
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_group' in delete_function:
            try:
                self.iam.delete_group(
                    GroupName=self.resourceName
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_server_certificate' in delete_function:
            try:
                self.iam.delete_server_certificate(
                    ServerCertificateName=self.resourceName,
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_user' in delete_function:
            try:
                self.iam.delete_user(
                    UserName=self.resourceName
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        else:
            print(f"{delete_function} not supported")
        print(f"Resource Type: {self.resourceType} of resourceName: {self.resourceName} is deleted")
        return status
