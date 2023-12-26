import boto3
from botocore.exceptions import ClientError

class glue:
    def __init__(self, resourceType, region, resourceName, delete_functions):
        self.resourceType = resourceType
        self.region = region
        self.resourceName = resourceName
        self.delete_functions = delete_functions
        self.glue_client = boto3.client('glue')
    
    def delete_action(self):
        print(f"deleting glue table: {self.resourceName}")
        try:
            response = self.glue_client.delete_job(
                    JobName=self.resourceName
                    )
            print(f"Resource Type: {self.resourceType} of resourceName: {self.resourceName} is deleted")
            return 'true'
        except Exception as e:
            print(f"error while deleing resource: {e}")
            return 'false'