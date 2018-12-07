// Load the AWS SDK
const aws = require("aws-sdk");

// Construct the AWS S3 Object -
// http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/S3.html#constructor-property
const s3 = new aws.S3({
  apiVersion: "2006-03-01"
});

// Define 2 new variables for the source and destination buckets
var srcBucket = "chris1-bucket-source";
var destBucket = "chris1-bucket-destination";

//Main function
exports.handler = (event, context, callback) => {
  var sourceObject = JSON.parse(JSON.parse(event.Records[0].body).Message)
    .Records[0].s3.object.key;

  //Copy the current object to the destination bucket
  //docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/S3.html#copyObject-property
  http: s3.copyObject(
    {
      CopySource: srcBucket + "/" + sourceObject,
      Bucket: destBucket,
      Key: sourceObject
    },
    function(copyErr, copyData) {
      if (copyErr) {
        console.log("Error: " + copyErr);
      } else {
        console.log("Copied OK");
      }
    }
  );
  callback(null, "All done!");
};
