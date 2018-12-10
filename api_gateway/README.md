# deploy code start function
## prerequisite
- SAM is installed
- awscli credential is correctly configured
- has access to s3, cloudformation, lambda etc.

## deployment step
```
# create s3 bucket and deploy
./deploy.sh [source s3 bucket name] [stack name]

# example
./deploy.sh asap-source Binary 

```

# api demo 
- manually turn off lambda proxy integration
- use mapping_template.vtl for application/json

## resource policy
- Change resource policy on the console according to resource_policy.json or just use templates on the console.
- If your api has been deployed, don't forget to redeploy it.
- You can test the policy with your IP.


## authorizor
- config authorizor on api gateway, choose token type
- config auth in corresponding function
- test authorizor with header BEARER:andrew and other values
note:
- for china regions, be aware of the arn aws-cn in the auth.py

## validation
- config parameter, header, body check in method request

## mapping
- go to request integration

## custom domain
- create a new custom domain on the left panel
