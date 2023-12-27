import boto3
from botocore.exceptions import ClientError

class mediapackage:
    def __init__(self, resourceType, region, resourceName, delete_functions):
        self.resourceType = resourceType
        self.region = region
        self.resourceName = resourceName
        self.delete_functions = delete_functions
        self.mediapackage = boto3.client('mediapackage-vod')
    
    def delete_action(self):
        print("mediapackage function is working")
        delete_function = self.delete_functions[self.resourceType]['delete']
        status = 'false'
        print(delete_function)
        print("mediapackage function working")
        if 'delete_packaging_Configuration' in delete_function:
            try:
                self.mediapackage.delete_packaging_configuration(
                    Id=self.resourceName
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_packaging_groups' in delete_function:
            #print(f"function name= {ec2_function}, {self.resourceType}, {self.resourceName}")
            try:
                self.mediapackage.delete_packaging_group(
                    Id=self.resourceName
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
