---
weight: 2
---

# AWS STS
AWS Security Token Service (AWS STS) is a global web service that allows you to generate temporary access for IAM users or federated users to gain access to your AWS resources. These temporary credentials are session-based, meaning they’re for short-term use only; once expired, they can no longer be used to access your AWS resources.

AWS STS can’t be accessed on the AWS console; it is only accessible through API. All STS requests go to a single endpoint at https://sts.amazonaws.com/, and logs are then recorded to AWS CloudTrail.

## STS API Operations

### `AssumeRole`
The AssumeRole API operation lets an IAM user assume an IAM role belonging to your account or to an external one (cross-account access). Once the request is successful, AWS generates and returns temporary credentials consisting of an access key ID, a secret access key, and a security token. These credentials can then be used by the IAM user to make requests to AWS services.

### `AssumeRoleWithWebIdentity`
The AssumeRoleWithWebIdentity API operation returns temporary security credentials for federated users who are authenticated through a public identity provider (e.g., Amazon Cognito, Login with Amazon, Facebook, Google, or any OpenID Connect-compatible identity provider). The temporary credentials can then be used by your application to establish a session with AWS. Just like the `AssumeRole` API, trusted entities who will be assuming the role must be specified. This time, instead of IAM users, it’ll be an identity provider.

`AssumeRoleWithWebIdentity` does not require IAM Identities credentials, making it suitable for mobile applications that require access to AWS. The `AssumeRoleWithWebIdentity` is one of the APIs that Amazon Cognito uses under the hood to facilitate the exchange of token and credentials on your behalf. Because Amazon Cognito abstracts the hassles associated with user authentication, it is recommended that you use Amazon Cognito when providing AWS access to application users. However, you may just use `AssumeRoleWithWebIdentity` as a standalone operation.

### `AssumeRoleWithSAML`
The `AssumeRoleWithSAML` API operation returns a set of temporary security credentials for federated users who are authenticated by enterprise Identity Providers compatible with SAML 2.0. The users must also use SAML 2.0 (Security Assertion Markup Language) to pass authentication and authorization information to AWS. This API operation is useful for organizations that have integrated their identity systems (such as Windows Active Directory or OpenLDAP) with software that can produce SAML assertions.

### `GetFederationToken`
The GetFederationToken API operation returns a set of temporary security credentials consisting of a security token, access key, secret key, and expiration for a federated user. This API is usually used for federating access to users authenticated by a custom identity broker and can only be called using the programmatic credentials of an IAM user (IAM Roles are not supported). Although you can use the security credentials of a root user to call `GetFederationToken`, it is not recommended for security reasons. Instead, AWS advises creating an IAM user specifically for a proxy application that does the authentication process. The default expiration period for this API is significantly longer than `AssumeRole` (12 hours instead of one hour). Since you do not need to obtain new credentials as frequently, the longer expiration period can help reduce the number of calls to AWS.

You can use the temporary credentials created by `GetFederationToken` in any AWS service except the following:

* You cannot call any IAM operations using the AWS CLI or the AWS API.
* You cannot call any STS operations except GetCallerIdentity .

### `DecodeAuthorizationMessage`
`DecodeAuthorizationMessage` decodes additional information about the authorization status of a request from an encoded message returned in response to an AWS request. For example, a user might call an API to which he or she does not have access; the request results in a Client.UnauthorizedOperation response. Some AWS operations additionally return an encoded message that can provide details about this authorization failure. The message is encoded, so that privilege details about the authorization are hidden from the user who requested the operation. To decode an authorization status message, one must be granted permission via an IAM policy to request the `DecodeAuthorizationMessage` action.

**References:**

* https://docs.aws.amazon.com/STS/latest/APIReference/API_Operations.html
* https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html