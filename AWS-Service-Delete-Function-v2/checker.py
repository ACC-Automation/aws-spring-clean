import boto3
import csv
from datetime import date
from ec2 import ec2
from efs import efs
from fsx import fsx
from secretsmanager import secretsmanager
from kinesis import kinesis
from autoscaling import autoscaling
from botocore.exceptions import ClientError

class checker:
    def __init__(self, item, delete_functions, bucket_name, sns_topic_arn, ddb_table_name):
        self.item = item
        self.delete_functions = delete_functions
        self.bucket_name = bucket_name
        selfsns_topic_arn = sns_topic_arn
        self.curr_date = date.today()
        self.csv_file_path = f'/tmp/{self.curr_date}-deleted.csv'
        self.object_key = f'delete/{self.curr_date}-deleted.csv'
        self.s3_url = f'https://{self.bucket_name}.s3.amazonaws.com/{self.object_key}'
        #self.ec2 = boto3.client('ec2')
        dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
        #ddb_table_name = 'AWS-Service-List'
        self.s3 = boto3.client('s3')
        self.sns = boto3.client('sns')
        self.client_cc_api = boto3.client('cloudcontrol')
        self.table = dynamodb.Table(ddb_table_name)
        
    def checker_resourcedeleted(self):
        self.resourceId_value = self.item.get('resourceId')
        self.resourceType_value = self.item.get('resourceType')
        self.status_value = self.item.get('resource_status')
        self.resourceName_value = self.item.get('resourceName')
        self.configurationItemStatus_value = self.item.get('configurationItemStatus')
        self.awsRegion_value = self.item.get('awsRegion')
        status = 'false'
        if self.configurationItemStatus_value == 'ResourceDeleted':
            self.table.delete_item(
                Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
            )
            status = 'true'
        return status #continue
        
    def status_terminate(self):
        status = 'false'
        if self.status_value == 'Terminate':
            cf = boto3.client('cloudformation')
            try:
                type_supp = cf.describe_type(
                Type='RESOURCE',
                TypeName = self.resourceType_value
                )
            except ClientError as e:
                print(e)
                self.table.delete_item(
                    Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
                )
                with open(self.csv_file_path, 'w', newline='') as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
                    csv_writer.writeheader()
                    csv_writer.writerow(self.item)
                status = 'true'
                return status
                #continue
            if type_supp['ProvisioningType'] != 'FULLY_MUTABLE' and type_supp['ProvisioningType'] != 'IMMUTABLE':
                print(f"{self.resourceType_value} and {type_supp['ProvisioningType']}")
                #for self.resourceType_value in delete_functions.keys():
                if self.delete_functions[self.resourceType_value]:
                    elements = self.resourceType_value.split("::")
                    if len(elements) >= 3:
                        service_to_find = elements[1].lower()
                    else:
                        service_to_find = "unknown"
                        print("Input string does not have at least 3 elements")
                    
                    print(service_to_find)
                        
                    if service_to_find == 'ec2':
                        print(self.resourceType_value)
                        e = ec2(self.resourceType_value, self.awsRegion_value, self.resourceName_value, self.delete_functions)
                        status = e.delete_action()
                        print(status)
                        if status == 'true':
                            self.table.delete_item(
                                Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
                            )
                            with open(self.csv_file_path, 'w', newline='') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
                                csv_writer.writeheader()
                                csv_writer.writerow(self.item)
                        return status #continue
                    elif service_to_find == 'autoscaling':
                        print(self.resourceType_value)
                        a = autoscaling(self.resourceType_value, self.awsRegion_value, self.resourceName_value, self.delete_functions)
                        status = a.delete_action()
                        if status == 'true':
                            self.table.delete_item(
                                Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
                            )
                            with open(self.csv_file_path, 'w', newline='') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
                                csv_writer.writeheader()
                                csv_writer.writerow(self.item)
                        return status #continue
                    elif service_to_find == 'efs':
                        print(self.resourceType_value)
                        e = efs(self.resourceType_value, self.awsRegion_value, self.resourceName_value, self.delete_functions)
                        status = e.delete_action()
                        if status == 'true':
                            self.table.delete_item(
                                Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
                            )
                            with open(self.csv_file_path, 'w', newline='') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
                                csv_writer.writeheader()
                                csv_writer.writerow(self.item)
                        return status #continue
                    elif service_to_find == 'fsx':
                        print(self.resourceType_value)
                        f = fsx(self.resourceType_value, self.awsRegion_value, self.resourceName_value, self.delete_functions)
                        status = f.delete_action()
                        if status == 'true':
                            self.table.delete_item(
                                Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
                            )
                            with open(self.csv_file_path, 'w', newline='') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
                                csv_writer.writeheader()
                                csv_writer.writerow(self.item)
                        return status #continue
                    elif service_to_find == 'iam':
                        print(self.resourceType_value)
                        i = iam(self.resourceType_value, self.awsRegion_value, self.resourceName_value, self.delete_functions)
                        status = i.delete_action()
                        if status == 'true':
                            self.table.delete_item(
                                Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
                            )
                            with open(self.csv_file_path, 'w', newline='') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
                                csv_writer.writeheader()
                                csv_writer.writerow(self.item)
                        return status #continue
                    elif service_to_find == 'kinesis':
                        print(self.resourceType_value)
                        k = kinesis(self.resourceType_value, self.awsRegion_value, self.resourceName_value, self.delete_functions)
                        status = k.delete_action()
                        if status == 'true':
                            self.table.delete_item(
                                Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
                            )
                            with open(self.csv_file_path, 'w', newline='') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
                                csv_writer.writeheader()
                                csv_writer.writerow(self.item)
                        return status #continue
                    elif service_to_find == 'kms':
                        if status == 'true':
                            self.table.delete_item(
                                Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
                            )
                            with open(self.csv_file_path, 'w', newline='') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
                                csv_writer.writeheader()
                                csv_writer.writerow(self.item)
                        return status #continue
                    elif service_to_find == 'secretsmanager':
                        print(self.resourceType_value)
                        s = secretsmanager(self.resourceType_value, self.awsRegion_value, self.resourceName_value, sedelete_functions)
                        status = s.delete_action()
                        if status == 'true':
                            self.table.delete_item(
                                Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
                            )
                            with open(self.csv_file_path, 'w', newline='') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
                                csv_writer.writeheader()
                                csv_writer.writerow(self.item)
                        return status #continue
                    elif service_to_find == 'mediaconvert':
                        if status == 'true':
                            self.table.delete_item(
                                Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
                            )
                            with open(self.csv_file_path, 'w', newline='') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
                                csv_writer.writeheader()
                                csv_writer.writerow(self.item)
                        return status #continue
                    else:
                        status = 'true'
                        print(f"Resource type: {self.resourceType_value}, currently not supported. Ref 1")
                        return status #continue
            else:
                print(f"Resource type: {self.resourceType_value} and status: {self.status_value}, supported in delete_cloudcontrol_api. Ref 2")
                status = self.delete_cloudcontrol_api()
                print(f"status:{status} for delete_cloudcontrol_api ref ")
                return status #continue
        else:
            #status = 'true'
            print(f"Resource type: {self.resourceType_value} and status: {self.status_value}. Retain Resource")
            return status #continue
        # Convert JSON data to CSV
        
    
    def delete_cloudcontrol_api(self):
        status = 'false'
        try:
            if self.status_value == 'Terminate':
                response = self.client_cc_api.delete_resource(
                    TypeName=self.resourceType_value,
                    #TypeVersionId='string',
                    #RoleArn='string',
                    #ClientToken='string',
                    Identifier=self.resourceName_value
                )
                print(response)
                    #if response['ProgressEvent']['OperationStatus'] == 'SUCCESS':
                        # Remove the DynamoDB entry
                    #    table.delete_item(
                    #        Key={'resourceId': resourceId_value, 'resourceType': resourceType_value}
                    #    )
                self.table.delete_item(
                        Key={'resourceId': self.resourceId_value, 'resourceType': self.resourceType_value}
                )
                print(f"resources for ID {self.resourceId_value} and Type: {self.resourceType_value} deleted successfully.")
            status = 'true'
        except ClientError as e:
            print(e)
            print(f"resources for ID {self.resourceId_value} and Type: {self.resourceType_value} NOT deleted.")
            status = 'false'
            pass     
        #status = 'true'
        if status == 'true':
            with open(self.csv_file_path, 'w', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
                csv_writer.writeheader()
                csv_writer.writerow(self.item)
        return status #continue
    '''
    def send_notification(self):
        try:
            self.s3.upload_file(self.csv_file_path, self.bucket_name, self.object_key)
            print(f'Uploaded {self.object_key} to S3 bucket {self.bucket_name}')
        except ClientError as e:
            print(e)
        emailmsg = f'Please find the s3 link for csv file for resosurces that have been deleted for {self.curr_date}.\n\n' \
            f'CSV file available at: {self.s3_url}' \
            f'Make required changes before 12:00 am today before deletion of mentioned resources' \
        
        response = self.sns.publish(
            TopicArn=self.sns_topic_arn,
            Message=emailmsg,
            Subject=f'Resources Deleted for {self.curr_date}'
        )
    '''
