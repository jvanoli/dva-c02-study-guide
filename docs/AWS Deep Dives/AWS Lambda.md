# AWS Lambda

AWS Lambda lets you run codes without managing servers. You don’t need to worry about tasks such as scaling, patching, and other management operations that are typically done on EC2 instances or on-premises servers. You can allot the maximum memory available for a Lambda function, as well as the function's execution duration, before timing out. The memory, which scales proportionally to the CPU power, can range from 128 MB to 10,240 MB in 1-MB increments. The default timeout is three seconds, with a maximum value of 900 seconds (15 minutes).

A Lambda function can be invoked in different ways. You can invoke a function directly on the AWS Lambda console, via the `Invoke` API/CLI command, or through a Function URL . You can set up certain AWS Services to invoke a Lambda function as well. For example, you can create a Lambda function that responds to Amazon S3 events (e.g. *processing files as they are uploaded to an S3 bucket*) or set up an Amazon EventBridge rule that triggers a Lambda function every week to perform batch processing. Lambda functions are also commonly used as a backend for APIs that do not require constant load, such as handling login requests or on-the-fly image processing.

![image-20250107204723652](./assets/image-20250107204723652.png)

## Synchronous vs. Asynchronous Invocations

There are two invocation types in AWS Lambda.

The first type is called Synchronous invocation, which is the default. Synchronous invocation is pretty straightforward. When a function is invoked synchronously, AWS Lambda waits until the function is done processing, then returns the result. Let’s see how this works through the following example:

![image-20250107205228755](./assets/image-20250107205228755.png)

The image above illustrates a Lambda function-backed API that is managed by API Gateway. When API Gateway receives a GET request from the /getOrder resource, it invokes the getOrder function. The function receives an event containing the payload, processes it, and then returns the result. 

Considerations when using synchronous invocation:

* If you’re planning to integrate AWS Lambda with API Gateway, take note that API Gateway’s integration timeout is 29 seconds. If a function takes longer than that to complete, the connection will time out, and the request will fail. Hence, use synchronous invocations for applications that don’t take too long to complete (e.g., authorizing requests, and interacting with databases). 
* Synchronously-invoked functions can accept a payload of up to 6 MB.
* You might need to implement a retry logic in your code to handle intermittent errors.

To call a Lambda function synchronously via API/CLI, set RequestResponse as the value for the invocation-type parameter when calling the Invoke command, as shown below:

```shell
aws lambda invoke \
	--function-name testFunction \
	--invocation-type RequestResponse \
	--cli-binary-format raw-in-base64-out \
	--payload '{ "input" : "input_value" }' response.json
```

Alternatively, you may just omit the invocation-type parameter as AWS Lambda invokes functions synchronously by default.

Services that invoke Lambda functions synchronously: ( services irrelevant to the exam are excluded ):
* Amazon API Gateway
* Application Load Balancer
* Amazon Cognito
* Amazon Data Firehose
* Amazon CloudFront (Lambda@Edge)

An Asynchronous invocation is typically used when a client does not need to wait for immediate results from a function. Some examples of these are long-latency processes that run in the background, such as batch operations, video encoding, and order processing.

When a function is invoked asynchronously, AWS Lambda stores the event in an internal queue that it manages. Let’s understand asynchronous invocation through the example below:

![image-20250107205409596](./assets/image-20250107205409596.png)

A PUT request is made to the /putOrder resource. Like the previous example, the request goes through API Gateway, which produces an event. This time, instead of API Gateway directly invoking the function, AWS Lambda queues the event. If the event is successfully queued, AWS Lambda returns an empty payload with `HTTP 202 status code`. The 202 status code is just a confirmation that the event is queued; it’s not indicative of a successful invocation. The client will not be required to wait for the Lambda function to complete. So, to improve user experience, you can create a worker that tracks order completion and sends notifications once the order is successfully processed.

To call a Lambda function asynchronously via the Invoke command, simply set Event as the value for the invocation-type parameter, as shown below:

```shell
aws lambda invoke \
	--function-name testFunction \
	--invocation-type Event \
	--cli-binary-format raw-in-base64-out \
	--payload '{ "input" : "input_value" }' response.json
```

Considerations when using asynchronous invocation:

* Asynchronously-invoked functions can only accept a payload of up to 256 KB.
* The Lambda service implements a retry logic for asynchronously-invoked functions
* Good for applications that run in the background (batch processing, video encoding)

Services that invoke Lambda functions asynchronously: (services irrelevant to the exam are excluded):

* Amazon API Gateway (by specifying Event in the X-Amz-Invocation-Type request header of a non-proxy integration API)
* Amazon S3
* Amazon CloudWatch Logs
* Amazon EventBridge
* AWS CodeCommit
* AWS CloudFormation
* AWS Config

### Handling failed asynchronous invocations
AWS Lambda has a built-in retry mechanism for asynchronous invocations. If the function returns an error,
Lambda will attempt to retry the request two more times, with a longer wait interval between each attempt.

![image-20250107205639032](./assets/image-20250107205639032.png)

The request is discarded after AWS Lambda has exhausted all remaining retries. To avoid losing events, you may redirect failed request attempts to an SQS dead-letter queue so that you can debug the error later and have another function retry it.

**References:**

- https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html
- https://aws.amazon.com/blogs/architecture/understanding-the-different-ways-to-invoke-lambda-functions/

## Event source mappings
Stream or queue-based resources such as DynamoDB streams, SQS queues, and Kinesis Data Streams streams do not invoke Lambda functions directly. Typically, we read records from these resources using pollers. A poller is an application that periodically checks a queue, pulls records from it (sometimes in batches), and sends them to a downstream service that will process them.

![image-20250107205752280](./assets/image-20250107205752280.png)

An event source mapping is a sort of polling agent that Lambda manages. Event source mappings take away the overhead of writing pollers from scratch to retrieve messages from queues/streams. This allows you to focus on building the domain logic of your application.

Event source mapping invokes a function synchronously if one of the following conditions is met:

1. The batch size is reached - The minimum batch size can be set to 1, but the default and maximum batch sizes vary on the AWS service that invokes your function.
2. The maximum batching window is reached - The batching window is the amount of time Lambda waits to gather and batch records. The default batch window for Amazon Kinesis, Amazon DynamoDB, and Amazon SQS is 0. This means that a Lambda function will receive batches as quickly as possible. You can tweak the value of the batch window based on the nature of your application.
3. The total payload is 6 MB - Because event source mappings invoke functions synchronously, the total payload (event data) that a function can receive is also limited to 6MB (the limit for synchronous invocations). This means that if the maximum record size in a queue is 100KB, then the maximum batch size you can set is 60.

