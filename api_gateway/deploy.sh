bucket_name=$1
stack_name=$2

sam package --template-file template.yaml --s3-bucket $bucket_name --output-template-file output.yaml
sam deploy --template-file output.yaml --stack-name $stack_name --capabilities CAPABILITY_IAM
aws cloudformation describe-stacks --stack-name $stack_name
