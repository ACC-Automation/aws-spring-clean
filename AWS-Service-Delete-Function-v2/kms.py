import boto3
from botocore.exceptions import ClientError

class kms:
    def __init__(self, resourceType, region, resourceName, delete_functions):
        self.resourceType = resourceType
        self.region = region
        self.resourceName = resourceName
        self.delete_functions = delete_functions
        self.kms = boto3.client('kms')
    
    def delete_action(self):
        print("kms function is working")
        delete_function = self.delete_functions[self.resourceType]['delete']
        status = 'false'
        print(delete_function)
        print("kms function working")
        
        if 'delete_Alias' in delete_function:
            # print(f"function name= {ec2_function}, {self.resourceType}, {self.resourceName}")
            try:
                self.kms.delete_alias(
                    AliasName=self.resourceName
                    )
                    
                status = 'true'
                print("delete_Alias worked properly")
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        
        elif 'delete_kms_key' in delete_function:
            #print(f"function name= {ec2_function}, {self.resourceType}, {self.resourceName}")
            try:
                self.kms.disable_key(
                    KeyId=self.resourceName
                    )
                    
                status = 'true'
                print("delete_kms_key worked properly")
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        else:
            print(f"{delete_function} not supported")
        print(f"Resource Type: {self.resourceType} of resourceName: {self.resourceName} is deleted")
        return status
