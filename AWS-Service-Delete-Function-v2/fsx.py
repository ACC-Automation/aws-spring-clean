import boto3
from botocore.exceptions import ClientError

class fsx:
    def __init__(self, resourceType, region, resourceName, delete_functions):
        self.resourceType = resourceType
        self.region = region
        self.resourceName = resourceName
        self.delete_functions = delete_functions
        self.fsx = boto3.client('fsx')
    
    def delete_action(self):
        #ec2_functions = dir(self.ec2)
        #for ec2_function in ec2_functions:
        #print(f"function name= {ec2_function}, {self.resourceType}, {self.resourceName}")
        delete_function = self.delete_functions[self.resourceType]['delete']
        status = 'false'
        print(delete_function)
        if 'delete_file_system' in delete_function:
            #print(f"function name= {ec2_function}, {self.resourceType}, {self.resourceName}")
            try:
                self.fsx.delete_file_system(
                    FileSystemId=self.resourceName
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_snapshot' in delete_function:
            try:
                self.fsx.delete_snapshot(
                    SnapshotId=self.resourceName
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_storage_virtual_machine' in delete_function:
            try:
                self.fsx.delete_storage_virtual_machine(
                    SnapshotId=self.resourceName,
                )
                status = 'true'
            except ClientError as e:
                status = 'false'
                print(e)
                pass
        elif 'delete_volume' in delete_function:
            try:
                self.fsx.delete_volume(
                    VolumeId=self.resourceName
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
