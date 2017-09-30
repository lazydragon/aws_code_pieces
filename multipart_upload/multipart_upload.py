import boto3
from boto3.s3.transfer import TransferConfig
from botocore.config import Config

# open logging to check the detailed upload process
#import logging
#logging.basicConfig(level=logging.DEBUG)

# The transfer threshold for multipart 
MB = 1024 ** 2
multipart_threshold = 8 * MB 
# The max number of threads that will be making request to perform a transfer
max_concurrency = 10 
# The partition size of each multipart chunk
multipart_chunksize = 5 * MB
# Whether use threads
use_threads = True
# Max retry times
retries = 100


# target bucket and key name
region = 'ap-northeast-1'
bucket = 'multipart--upload-andrew-test'
key = 'test/file'
# to upload file name
to_upload = 'bigfile'



# Get the service client
s3 = boto3.client('s3', region, config=Config(retries={'max_attempts': retries}))

# Group things into config
config = TransferConfig(multipart_threshold=multipart_threshold,
                        max_concurrency=max_concurrency,
                        multipart_chunksize=multipart_chunksize,
                        use_threads=use_threads)

# Upload tmp.txt to bucket-name at key-name
s3.upload_file(to_upload, bucket, key, Config=config)

