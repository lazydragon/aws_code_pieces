import boto3

# rds information
rds = boto3.client('rds')

for i in rds.describe_db_instances()['DBInstances']:
    print "%s %s %s" % (i['DBInstanceIdentifier'], i['DBInstanceClass'], i['AllocatedStorage'])


# ec2 information
ec2 = boto3.resource('ec2')

for i in ec2.instances.all():
    volumes = [v.size for v in i.volumes.all()]
    print "%s %s %s %s" % (i.id, i.instance_type, i.public_ip_address, volumes)
