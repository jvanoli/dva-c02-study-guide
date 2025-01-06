# AWS Identity Access Management (IAM)

IAM is the primary tool for controlling and managing access to an AWS account. It sits at the core of AWS
security; everything you do with AWS, whether it's creating a Lambda function, uploading a file to an S3 bucket,
or something mundane as viewing EC2 instances on the Console, is governed by IAM. It allows you to specify
who, which AWS resources, as well as what actions they can and cannot do. These are also known as
authentication and authorization.

IAM Identities
IAM identities handle the authentication aspect of your AWS account. It pertains to any user, application, or
group that belongs to your organization.

![image-20250106213326444](./assets/image-20250106213326444.png)

An IAM identity can be an IAM User , IAM role , or IAM Group .

