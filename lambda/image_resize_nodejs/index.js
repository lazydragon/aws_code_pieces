'use strict';

const AWS = require('aws-sdk');
const S3 = new AWS.S3({
  signatureVersion: 'v4',
});
const Sharp = require('sharp');

const width = 20;
const height = 20; 

exports.handler = function(event, context, callback) {
  const bucket = event.Records[0].s3.bucket.name; 
  const key = event.Records[0].s3.object.key; 
  const dest_key = "small/" + key.split("/").pop();

  S3.getObject({Bucket: bucket, Key: key}).promise()
    .then(data => Sharp(data.Body)
      .resize(width, height)
      .toFormat('png')
      .toBuffer()
    )
    .then(buffer => S3.putObject({
        Body: buffer,
        Bucket: bucket,
        ContentType: 'image/png',
        Key: dest_key,
      }).promise()
    )
}
