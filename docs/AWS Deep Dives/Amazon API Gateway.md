---
weight: 4
---

# Amazon API Gateway‬

‭Amazon API Gateway is a fully managed service that allows you to publish, maintain, monitor, and secure your RESTful APIs. It serves as the entry point for your back-end services that are powered by AWS Lambda, Amazon EC2, Amazon ECS, AWS Elastic Beanstalk, or any web application. 

The following diagram illustrates how a request flows through API Gateway when an API is called.

![image-20250114232708396](/Users/jvanoli/Library/Application Support/typora-user-images/image-20250114232708396.png)

1. `Method Request`

    * This section is where client requests are validated. Here, you can set up the authorization type (`AWS_IAM`, `NONE`, Lambda authorizer, Cognito authorizer) to control API access, enable the usage of API keys, or set up a request body validator using a Lambda function.
    * You can also declare in the Method Request any input body, query string parameters, and HTTP headers that your API can accept.

2. `Integration Request`

    * The Integration Request section contains settings about how API Gateway communicates with the backend of your choosing (Lambda function, HTTP endpoint, Mock, AWS Service, VPC Link) and the integration type (proxy or non-proxy) API Gateway uses.
    * For non-proxy integration, you have the option the use mapping templates to model the structure of the request data that gets forwarded to the backend.

3. `Integration Response`
    * This section only applies to a non-proxy integration. The Integration response intercepts the result returned from the backend before it’s returned to the client.
    * You must configure at least one integration response. The default response is Passthrough, which instructs API Gateway to return the response as-is. You may also transform the response to another format (base64 or text).
    * Similarly to the Integration request, you have the option to transform the response data before it is returned to the client.

4. Method Response
    * Like Method Request, the Method Response is where you can define which HTTP headers the method can return.



## REST API vs. HTTP API vs. Websocket API

When you create an API, you get to choose between a REST API, HTTP API, and a WebSocket API endpoint.

* REST API
    * For standard use cases, the REST API is what you’ll want to use.
    * This gives you complete control over the request and response along with other API management capabilities like caching, creating API keys, and usage plans.
* HTTP API
    * Cheaper than REST API
    * Designed for simple applications
    * Lacks other API Gateway features
* WebSocket API
    * Typically used for real-time applications (e.g., chat applications, market trading applications)

**References:**

- https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html
- https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-basic-concept.html


## Proxy vs. Non-proxy integration‬
‭In a‬‭ **Proxy integration**, client’s request is transmitted‬‭ as is to the backend, including any headers or query‬ parameters. No modification is done to the request data. As for the response, your backend is responsible for‬ returning the response’s status code, headers, and the payload to the client.‬

In a‬‭ **Non-Proxy integration‬‭**,‬‭ API Gateway has control‬‭ over how client data is formatted before it’s passed down‬ to your integration backend or before it’s returned to the client. For example, instead of feeding the entire‬ request data to your backend, you can filter it first using mapping templates at the‬‭ `Integration` Request‬‭ level ‬to get only the portion that care for. The Non-Proxy integration is a bit more complex to implement and requires you to have knowledge of the Apached Velocity Template Language (VTL), which is the engine that API Gateway uses for mapping templates.

**Reference:**
- https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-integration-types.html

## Stage variables‭
A Stage variable is a key-pair value that you can associate with a deployment stage of a REST API. You can‬ think of them as environment variables where you store different parameters or configuration values that your‬ API can access at runtime.‬

Doing canary releases within the same REST API stage is a great application of stage variables. Canary is a‬ deployment approach in which traﬃc is split into two parts, one of which carries a larger portion of the traﬃc‬ and is routed to the production version, while the smaller portion points to the environment to which the new‬ version is deployed. It can be a 90/10 split, 70/30 split, or even a 50/50 split. It all depends on how aggressive‬ you want your deployment to be. This kind of setup allows developers to expose new features or bug fixes to a‬ subset of users and receive feedback from them without having to shut down or make direct changes to the‬ production version.‬

‭Consider a REST API stage with a Lambda function as the backend. Assume you're about to release a new‬ version of your API and want to test it with a subset of your users while continuing to serve the majority of‬ traﬃc with the old version. You can shift all traﬃc to the new version once you’re satisfied with it.‬‭ As shown in‬ the diagram below, the goal is to have a single API endpoint that dynamically interacts with two distinct‬ versions of the Lambda function.‬

![image-20250114235406422](/Users/jvanoli/Library/Application Support/typora-user-images/image-20250114235406422.png)

This is where stage variables come into play. In the example, we have a Lambda function with two aliases (prod and beta). Rather than writing the actual aliases in your integration backend's settings, we can use the stage variable ver as a placeholder. You can then switch between different values of ver in the Canary setting of the API Stage and control the amount of traﬃc that goes to different aliases.

**References:**

- https://docs.aws.amazon.com/apigateway/latest/developerguide/stage-variables.html
- https://docs.aws.amazon.com/apigateway/latest/developerguide/canary-release.html


## Mapping Templates

Mapping templates allow you to modify any request data before it is forwarded to your integration backend. Conversely, it can be used for transforming the response data before it is returned to the client. Let’s further understand how this works with an example.

Say you’ve built an API for a music application that returns various details about an artist. To keep it simple, consider the following JSON data:‭

```json
{
    "id": 1234,
    "artist": "Queen",
    "popularity": 90,
    "genres": [
        "Progressive rock",
        "Pop rock",
        "Glam rock"
    ]
}
```

If a user wants to obtain the popularity score or the genre of a certain artist, there’s no way for him/her to retrieve the information that he/she only cares for. To solve this, you can use mapping templates to modify the response before it is sent back to the user. Assuming that your API has a resource path named `/{id}` , a child resource path called `/genres` can be created under it. In the integration response settings, add a mapping template to construct the new response.

After redeploying the API, users can now send `GET` requests to the `/{id}/genres` resource. In our example, the response would simply be:

```json
{
    "genre": [
        "Progressive rock",
        "Pop rock",
        "Glam rock"
    ]
}
```

Mapping templates are written in the Velocity Template Language or VTL — a Java-based template engine developed by Apache. If you aren’t familiar with it, getting comfortable with mapping templates may take you some time. Don’t worry, as knowledge of VTL is not required in the CDA exam; you must only understand what a mapping template is and what it is used for at a high level.

Keep in mind that mapping templates **only work for non-proxy integrations** . This is because in proxy integrations, API Gateway simply passes the data it receives to both ends and is unaware of how the request/response is modeled.

You can also use mapping templates to modernize legacy applications. If you have a legacy application that‭ you want to expose, say a SOAP web service that processes XML data, you can have clients send‬ JSON-formatted requests and then have Amazon API Gateway transform that JSON data to XML using‭ mapping templates. As for the integration backend, you can use a Lambda function as middleware to transmit‬ the XML as a payload to the SOAP web service.‬

## Invalidating Cache‬
Caching often leads to data inconsistency, which is a problem commonly faced. When content is cached, API‬ Gateway does not update the cache entries until the Time-To-Live (TTL) expires. As a result, any changes made‬ to the database will not immediately reflect on the client-side, leading to a disparity between the actual content‬ and what is displayed on the application. However, you can take steps to mitigate this issue by sending an‬ invalidation request to your API endpoint. This will prompt API Gateway to refresh its cache instead of waiting‬ for the TTL to expire.‬

To invalidate a cache entry, simply include the‬‭ `Cache-Control‬‭` header in a request with a‬‭ `max-age‬‭` of `0`, as‬‭ shown in the example below that uses the Fetch API in Javascript.

```javascript
fetch('https://aaaa4vb5wf.execute-api.us-east-1.amazonaws.com/v1', {
    method:	'GET',
    headers : {
      'Cache-Control': 'max-age=0'
    }
  });
```

**Reference:**

- https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html#invalidate-method-caching



## Cross-Origin Resource Sharing (CORS)

CORS a security mechanism that most web browsers such as Google Chrome or Mozilla Firefox enforce to relax the restrictions of the same-origin policy. The same-origin policy is a browser security feature that limits scripts loaded from an origin to only interact with resources from the same origin. While the intention is good, sometimes it can be too restrictive. Businesses today usually rely on third-party APIs to quickly add features to their applications. This would not be possible with the Same-Origin Policy in place. To solve this problem, engineers came up with the idea of Cross-origin resource sharing to loosen up the Same-Origin Policy restrictions.

![image-20250115002053902](/Users/jvanoli/Library/Application Support/typora-user-images/image-20250115002053902.png)

Say you visit a website called `pet.com` using Google Chrome. Upon loading, Google Chrome will download the required assets (HTML, Javascript, images, fonts, etc.) from the website’s server to render the webpage. As you browse the website, you come across a fun feature that uses Artificial Intelligence (AI) to identify dog or cat breeds based on an image you upload. This feature is powered by a third-party API (`petbreed.com`), which is accessed via a Javascript file. Google Chrome will not immediately send a GET request to `petbreed.com` after you submit an image. Instead, it will first send a preflight OPTIONS request to confirm if `petbreed.com` does indeed allow `pet.com` to make GET requests. At the `petbreed.com` server’s end, the allowed domains and methods can be specified through the **`Access-Control-Allow-Origin`** and the **`Access-Control-Request-Method`** headers. The API developer can select which values to put in those headers. For example, `pet.com` can be defined as an `Access-Control-Allow-Origin` header value and `GET` as an `Access-Control-Request-Method` header value. This will explicitly grant `pet.com` to make `GET` requests to `petbreed.com`. Next, `petbreed.com` returns the list of allowed API methods and domains to Google Chrome. If `pet.com` is specified in the `Access-Control-Allow-Origin`, only then will Google Chrome send the actual `GET` request.

Just like `petbreed.com`, you can also configure CORS in API Gateway. Please note that CORS is disabled by default. CORS is configured at the resource method level when using non-proxy integrations. You must specify the proper access control headers in the header mappings of your API's integration response. On the other hand, if you’re using a proxy integration, you must explicitly declare the access control headers in the response returned by your backend.

**References:**

- https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html
- https://aws.amazon.com/blogs/compute/configuring-cors-on-amazon-api-gateway-apis/



## Authorizers

API Gateway lets you use Cognito User Pool or a Lambda function to authorize client requests.

How Cognito User Pool authorizer works:

![image-20250115002820198](/Users/jvanoli/Library/Application Support/typora-user-images/image-20250115002820198.png)

1. When a user logs in to the User Pool, Cognito checks if the credentials the user has submitted are valid.
2. If the login is successful, Cognito returns a JSON web token (JWT) to the client.
3. The JSON web token (JWT) is passed to a custom header which is included as part of the API request.
4. API Gateway will look for the custom header and verify its validity from Amazon Cognito.
5. Once verified, API Gateway accepts the request and performs the API call. In this case, the Lambda function, which is the backend, is invoked. If there are no issues, API Gateway returns a 200 status code along with the response from the Lambda function back to the client.

You might want to implement a Lambda Function Authorizer to enforce custom authorization logic, such as those that employ bearer token authentication strategies (OAuth) or something that uses request parameters to determine the caller's identity. Since this is a custom method, you have to write the logic that carries out the authorization process. As a result, this takes more development effort on your end compared to using the Cognito User Pool.

<u>How a Lambda function Authorizer works:</u>

![image-20250115003010860](/Users/jvanoli/Library/Application Support/typora-user-images/image-20250115003010860.png)

1. The application sends a GET method to API Gateway, along with a bearer token or request parameters.
2. API Gateway will check whether a Lambda authorizer is enabled for the method. If it is, API Gateway calls the Lambda function that authorizes the request.
3. The Lambda function authenticates the request. If the call succeeds, the Lambda function grants access by returning an output object containing at least an IAM policy and a principal identifier.
4. API Gateway evaluates the policy. If access is denied, API Gateway returns a 403 forbidden status code and If access is allowed, API Gateway performs the GET request.

**Reference:**

- https://aws.amazon.com/blogs/compute/introducing-custom-authorizers-in-amazon-api-gateway/

## Usage Plans

If you have an idea for an API that you’d like to expose or sell, perhaps you’ve built an AI service that can help out other businesses, then you might want to look at Usage Plans. Usage plans is an API Gateway feature that can help you control different levels of access to an API. For example, you can create three subscription plans for your API: basic, standard, and premium plan. A usage plan can be used to set distinct throttling and quota limitations based on a subscription, which is then enforced on specific client API keys.

Aside from that, you can sell your API as a product in the AWS SaaS Marketplace so other users or companies can see your product and subscribe to it. Your API subscribers are billed based on the number of requests made to the usage plan.

**References:**

- https://aws.amazon.com/blogs/aws/new-usage-plans-for-amazon-api-gateway/
- https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html
