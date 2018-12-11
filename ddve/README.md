# pre requisit
- ddve image created
- ddve image uploaded to a s3 bucket

# setup steps
1. create role
```
aws iam create-role --role-name vmimport --assume-role-policy-document file://trust-policy.json
```

2. use cli to convert ddve image to a snapshot
aws ec2 import-snapshot --disk-container file://DDimport.json

3. check import progress
aws ec2 ^Cscribe-import-snapshot-tasks --import-task-ids import-snap-<snapshotid>

4. 
