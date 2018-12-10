import boto3

from type_info import types

rds = boto3.client('rds')
cloudwatch = boto3.client('cloudwatch')

def main():
    # go through all rds instances
    for i in rds.describe_db_instances()['DBInstances']:
        name = i['DBInstanceIdentifier']
        class_type = i['DBInstanceClass']
        disk = i['AllocatedStorage']

        max_connection = types[class_type] * 1024 * 1024 * 1024 / 12582880

        print "%s %s %s %s" % (name, class_type, disk, max_connection)

        # set alarm for connections
        put_alarm(alarm_name='db_connection_alarm_%s' % name,
                  origin='DatabaseConnections', rds_name=name,
                  expression='origin/%s*100' % max_connection)
        # set alarm for disk space
        put_alarm(alarm_name='db_space_alarm_%s' % name,
                  origin='FreeStorageSpace', rds_name=name,
                  expression='origin/%s*100' % disk,
                  threshold=25,
                  comparison='LessThanThreshold')


def put_alarm(alarm_name, origin, rds_name, expression,
              evaluation_periods=10, threshold=75, comparison='GreaterThanThreshold',
              sns='arn:aws-cn:sns:cn-north-1:074481125102:rds_performance'):
    response = cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        # alarm actions, you can config SNS topic here to send SMS or email
        AlarmActions=[
            sns
        ],
        EvaluationPeriods=evaluation_periods,
        Threshold=threshold,
        ComparisonOperator=comparison,
        Metrics=[
            {
                'Id': 'origin',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/RDS',
                        'MetricName': origin,
                        'Dimensions': [
                            {
                                'Name': 'DBInstanceIdentifier',
                                'Value': rds_name 
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Average',
                },
                'ReturnData': False
            },
            {
                'Id':'consumption',
                'Expression': expression,
                'ReturnData': True
            }
        ]
    ) 
    print response
    return response

if __name__ == "__main__":
    main()
