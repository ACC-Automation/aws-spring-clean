import json
import boto3
import pytz
import csv
import os
from datetime import datetime, time, date
from botocore.exceptions import ClientError
#from ec2 import ec2
from checker import checker

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
#ddb_table_name = 'AWS-Service-List'
ddb_table_name = os.environ['TABLE_NAME']
#client_cc_api = boto3.client('cloudcontrol')
delete_functions = {
    'AWS::EC2::ClientVpnEndpoint': {
        'list': 'describe_client_vpn_endpoints',
        'delete': 'delete_client_vpn_endpoint'
    },
    'AWS::EC2::ClientVpnRoute': {
        'list': 'describe_client_vpn_routes',
        'delete': 'delete_client_vpn_route'
    },
    'AWS::EC2::ClientVpnTargetNetworkAssociation': {
        'list': '',
        'delete': ''
    },
    'AWS::EC2::Instance': {
        'list': 'describe_instances',
        'delete': 'terminate_instances'
    },
    'AWS::EC2::SecurityGroup': {
        'list': 'describe_security_groups',
        'delete': 'delete_security_group'
    },
    'AWS::EC2::SecurityGroupEgress': {
        'list': '',
        'delete': ''
    },
    'AWS::EC2::SecurityGroupIngress': {
        'list': '',
        'delete': ''
    },
    'AWS::EC2::TrafficMirrorFilter': {
        'list': 'describe_traffic_mirror_filters',
        'delete': 'delete_traffic_mirror_filter'
    },
    'AWS::EC2::TrafficMirrorFilterRule': {
        'list': '',
        'delete': 'delete_traffic_mirror_filter_rule'
    },
    'AWS::EC2::TrafficMirrorSession': {
        'list': 'describe_traffic_mirror_sessions',
        'delete': 'delete_traffic_mirror_session'
    },
    'AWS::EC2::TrafficMirrorTarget': {
        'list': 'describe_traffic_mirror_targets',
        'delete': 'delete_traffic_mirror_target'
    },
    'AWS::EC2::VPCCidrBlock': {
        'list': '',
        'delete': ''
    },
    'AWS::EC2::VPNGatewayRoutePropagation': {
        'list': '',
        'delte': ''
    },
    #'AWS::AppMesh::GatewayRoute': {},
    #'AWS::AppMesh::Mesh': {},
    #'AWS::AppMesh::Route' {},
    #'AWS::AppMesh::VirtualGateway': {},
    #'AWS::AppMesh::VirtualNode': {},
    #'AWS::AppMesh::VirtualRouter': {},
    #'AWS::AppMesh::VirtualService': {},
    #'Alexa::ASK::Skill': {},
    #'AWS::AutoScalingPlans::ScalingPlan': {},
    #'AWS::Budgets::Budget': {},
    #'AWS::CertificateManager::Account': {},
    #'AWS::CertificateManager::Certificate': {},
    #'AWS::Chatbot::MicrosoftTeamsChannelConfiguration': {},
    #'AWS::Chatbot::SlackChannelConfiguration': {},
    #'AWS::CleanRooms::AnalysisTemplate': {},
    #'AWS::CleanRooms::Collaboration': {},
    #'AWS::CleanRooms::ConfiguredTable': {},
    #'AWS::CleanRooms::ConfiguredTableAssociation': {},
    #'AWS::CleanRooms::Membership': {}.
    #'AWS::Synthetics::Canary': {},
    #'AWS::Synthetics::Group': {},
    #'AWS::CodeDeploy::DeploymentGroup': {},
    #'AWS::CodeBuild::Project': {},
    #'AWS::CodeBuild::ReportGroup': {},
    #'AWS::CodeBuild::SourceCredential': {},
    #'AWS::CodePipeline::Pipeline': {},
    #'AWS::CodePipeline::Webhook': {},
    #'AWS::CodeCommit::Repository': {},
    #'AWS::DLM::LifecyclePolicy': {},
    #'AWS::DataPipeline::Pipeline': {},
    #'AWS::DAX::Cluster': {},
    #'AWS::DAX::ParameterGroup': {},
    #'AWS::DAX::SubnetGroup': {},
    #'AWS::DirectoryService::MicrosoftAD': {},
    #'AWS::DMS::Certificate': {},
    #'AWS::DMS::Endpoint': {},
    #'AWS::DMS::EventSubscription': {},
    #'AWS::DMS::ReplicationInstance': {},
    #'AWS::DMS::ReplicationSubnetGroup': {},
    #'AWS::DMS::ReplicationTask': {},
    #'AWS::DocDB::DBCluster': {},
    #'AWS::DocDB::DBClusterParameterGroup': {},
    #'AWS::DocDB::DBInstance': {},
    #'AWS::DocDB::DBSubnetGroup': {},
    'AWS::AutoScaling::AutoScalingGroup': {
        'list': 'describe_auto_scaling_groups',
        'delete': 'delete_auto_scaling_group'
    },
    'AWS::EFS::AccessPoint': {
        'list': 'describe_access_points',
        'delete': 'delete_access_point'
    },
    'AWS::EFS::FileSystem': {
        'list': 'describe_file_systems',
        'delete': 'delete_file_system'
    },
    'AWS::EFS::MountTarget': {
        'list': 'describe_mount_targets',
        'delete': 'delete_mount_target'
    },
    'AWS::Events::Rule': {
        'list': 'describe_rule',
        'delete': 'delete_rule'
    },
    #'AWS::Events::EventBusPolicy': {},
    'AWS::Events::EventBus': {
        'list': 'describe_event_bus',
        'delete': 'delete_event_bus'
    },
    #'AWS::Events::Endpoint': {},
    #'AWS::FinSpace::Environment': {},
    'AWS::FSx::FileSystem': {
        'list': 'describe_file_systems',
        'delete': 'delete_file_system'
    },
    'AWS::FSx::Snapshot': {
        'list': 'describe_snapshots',
        'delete': 'delete_snapshot'
    },
    'AWS::FSx::StorageVirtualMachine': {
        'list': 'describe_storage_virtual_machines',
        'delete': 'delete_storage_virtual_machine'
    },
    'AWS::FSx::Volume': {
        'list': 'describe_volumes',
        'delete': 'delete_volume'
    },
    #'AWS::GuardDuty::Filter': {},
    #'AWS::GuardDuty::IPSet': {},
    #'AWS::GuardDuty::Master': {},
    #'AWS::GuardDuty::Member': {},
    #'AWS::GuardDuty::ThreatIntelSet': {},
    'AWS::IAM::AccessKey': {
        'list': 'list_access_keys',
        'delete': 'delete_access_key'
    },
    'AWS::IAM::Group': {
        'list': 'list_groups',
        'delete': 'delete_group'
    },
    'AWS::IAM::ServerCertificate': {
        'list': 'list_server_certificates',
        'delete': 'delete_server_certificate'
    },
    'AWS::IAM::User': {
        'list': 'get_user',
        'delete': 'delete_user'
    },
    'AWS::IAM::UserToGroupAddition': {
        'list': '',
        'delete': ''
    },
    'AWS::Kinesis::StreamConsumer': {
        'list': 'list_stream_consumers',
        'delete': 'deregister_stream_consumer'
    },
    'AWS::KMS::ReplicaKey': {
        'list': '',
        'delete': ''
    },
    'AWS::MediaConvert::JobTemplate': {
        'list': '',
        'delete': ''
    },
    'AWS::MediaConvert::Preset': {
        'list': '',
        'delete': ''
    },
    'AWS::MediaConvert::Queue': {
        'list': '',
        'delete': ''
    },
    #'AWS::SecretsManager::RotationSchedule': {},
    'AWS::SecretsManager::ResourcePolicy': {
        'list': 'get_resource_policy',
        'delete': 'delete_resource_policy'
    },
    
    'AWS::CodePipeline::Pipeline': {
        'list': 'get_Pipeline',
        'delete': 'delete_pipeline'
    },
    'AWS::CodePipeline::Webhook': {
        'list': 'get_Webhook',
        'delete': 'delete_webhook'
    }
    
    #'AWS::SecretsManager::SecretTargetAttachment': {},
}

def lambda_handler(event, context):
    table = dynamodb.Table(ddb_table_name)
    
    # Scan DynamoDB table to get items
    response = table.scan()
    items = response.get('Items', [])
    print(items)
    
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist_timezone).time()
    print(current_time_ist.hour)
    #start_time = time(18, 0)  # 18:00 IST
    #end_time = time(0, 0)  # 00:00 IST (midnight)
    curr_date = date.today()
    print(curr_date)
    #bucket_name = 'aws-security-automation'
    bucket_name = os.environ['BUCKET_NAME']
    #sns_topic_arn = 'arn:aws:sns:ap-south-1:268500393272:AWS_Resource_Status'
    sns_topic_arn = os.environ['SNS_ARN']
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    #if 18 <= current_time_ist.hour < 24 or 0 <= current_time_ist.hour < 6:
    if 18 <= current_time_ist.hour < 24:
    #if 18 <= 2 < 24:
        # Define the CSV file path
        csv_file_path = f'/tmp/{curr_date}.csv'

        # Convert JSON data to CSV
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
            csv_writer.writeheader()
            for data in items:
                #json_data = json.loads(json.dumps(data))
                print(data.values())
                csv_writer.writerow(data)
        object_key = f'scan/{curr_date}.csv'

        try:
            s3.upload_file(csv_file_path, bucket_name, object_key)
            print(f'Uploaded {object_key} to S3 bucket {bucket_name}')
        except ClientError as e:
            print(e)

        # Create a message with the S3 URL and send it to the SNS topic
        s3_url = f'https://{bucket_name}.s3.amazonaws.com/{object_key}'
        emailmsg = f'Please find the s3 link for csv file for resosurces about to be deleted for {curr_date}.\n\n' \
            f'CSV file available at: {s3_url}' \
            f'Make required changes before 12:00 am today before deletion of mentioned resources' \

        response = sns.publish(
            TopicArn=sns_topic_arn,
            Message=emailmsg,
            Subject=f'Resource Deletion Reminder for {curr_date}'
        )
    else:
        csv_file_path = f'/tmp/{curr_date}-deleted.csv'
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=['resourceType', 'awsRegion', 'resourceId', 'resourceName', 'resource_status', 'configurationItemStatus', 'time_of_crud_past_18'])
            csv_writer.writeheader()
        object_key = f'delete/{curr_date}-deleted.csv'
        s3_url = f'https://{bucket_name}.s3.amazonaws.com/{object_key}'
        for item in items:
            print(item)
            if item['time_of_crud_past_18'] == 'true':
                print(f"Skipping this item resourceType: {item['resourceType']} and resourceName: {item['resourceName']}")
                table.update_item(
                    Key={'resourceId': item['resourceId'], 'resourceType': item['resourceType']},
                    UpdateExpression="set time_of_crud_past_18= :t",
                    ExpressionAttributeValues={
                        ':t': 'false'
                    },
                    ReturnValues="ALL_NEW"
                )
                continue
            c = checker(item, delete_functions, bucket_name, sns_topic_arn, ddb_table_name)
            status = c.checker_resourcedeleted()
            if status != 'true':
                print(f"status:{status} for checker_resourcedeleted")
                status = c.status_terminate()
                print(f"status:{status} for status_terminate ref 1")
                if status == 'true':
                    print(f"status:{status} for status_terminate ref 2")
                    continue
                #else:
                #    status = c.delete_cloudcontrol_api()
                #    print(f"status:{status} for delete_cloudcontrol_api")
                #continue
            #status = c.status_terminate()
            #if status == 'true':
            #    print(f"status:{status} for status_terminate")
            #    continue
            #status = c.delete_cloudcontrol_api()
            #print(f"status:{status} for delete_cloudcontrol_api")
        #checker.send_notification()
        try:
            s3.upload_file(csv_file_path, bucket_name, object_key)
            print(f'Uploaded {object_key} to S3 bucket {bucket_name}')
        except ClientError as e:
            print(e)
        emailmsg = f'Please find the s3 link for csv file for resosurces that have been deleted for {curr_date}.\n\n' \
            f'CSV file available at: {s3_url}' \
            f'Make required changes before 12:00 am today before deletion of mentioned resources' \
        
        response = sns.publish(
            TopicArn=sns_topic_arn,
            Message=emailmsg,
            Subject=f'Resources Deleted for {curr_date}'
        )
    return {
        'statusCode': 200,
        'body': 'Resources deleted and DynamoDB entries removed successfully.'
    }

 

