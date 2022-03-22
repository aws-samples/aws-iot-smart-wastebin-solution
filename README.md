## AWS IoT Smart Wastebin solution

[![Unit Tests](https://github.com/aws-samples/aws-iot-smart-wastebin-solution/workflows/Unit%20Tests/badge.svg)](https://github.com/aws-samples/aws-iot-smart-wastebin-solution/actions)

This post provides an example of how to build a connected Trash Can IoT solution for local councils.
As the IoT use cases involve complex ecosystem of technologies right from sensor, device management
all the way through to analytics layer, the serverless architecture is a great way to start small, validate and
deploy at scale.
Hence, this post walks you through AWS serverless key architecture components around device
provisioning, ingesting trash images and waste weight data through AWS IoT Core into AWS IoT
Analytics, analyze trash image using Amazon Rekognition to enrich waste data and finally store into
Amazon S3 storage for building waste heat map using Amazon QuickSight

### Architecture

Target architecture:

<p align="center">
  <img src="docs/smart-wastebin-iot-architecture.png" alt="AWS Architecture Diagram" />
</p>

### Usage

#### Prerequisites
To deploy the solution, 

1. you need an AWS account. If you don’t already have an AWS account, create one at <https://aws.amazon.com> by following the on-screen instructions. Your access to the AWS account must have IAM permissions to launch AWS CloudFormation templates that create IAM roles.
2. clone the repository
3. An S3 bucket to upload all the artifacts from the cloned respository under src/greengrass-app-component directory
4. Upload all the artifacts to AWS S3 Bucket
    1. On AWS Console, choose "**S3**" service
    2. Choose your bucket created as mentioned step 3
    3. Press "**Create folder**" button
    4. Enter "**greengrass-app-component**" in folder name field and press "**Create folder**" button
    5. Choose the "**greengrass-app-component**" folder and press "**Upload**" button
    6. Press "**Add files**" button on upload screen and choose all the files from greengrass-app-component
    7. Finally press "**Upload**" button
    8. Please make sure that all the artifacts are under "**s3://<your bucket name>/greengrass-app-component**". This is very important to ensure that path is correct for successful deployment on edge gateway


#### Deployment
The application is deployed as an [AWS CloudFormation](https://aws.amazon.com/cloudformation) template.

> **Note**
You are responsible for the cost of the AWS services used while running this sample deployment. There is no additional
cost for using this sample. For full details, see the pricing pages for each AWS service that you use in this sample. Prices are subject to change.

1. Deploy the latest CloudFormation template by following the link below for your preferred AWS region:

| Region                                | Launch Template                                            |
|---------------------------------------|------------------------------------------------------------|
| **US East (N. Virginia)** (us-east-1) | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)]() |
| **US West (Oregon)** (us-west-2)      | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)]() |
| **EU (Ireland)** (eu-west-1)          | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)]() |
| **EU (London)** (eu-west-2)           | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)]() |
| **EU (Frankfurt)** (eu-central-1)     | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)]() |
| **AP (Sydney)** (ap-southeast-2)      | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)]() |

2. If prompted, login using your AWS account credentials.
1. You should see a screen titled "*Create Stack*" at the "*Specify template*" step. The fields specifying the CloudFormation
   template are pre-populated. Choose the *Next* button at the bottom of the page.
1. On the "*Specify stack details*" screen you can customize the following parameters of the CloudFormation stack:

| Parameter label | Default           | Description                                                                     |
|-----------------|-------------------|---------------------------------------------------------------------------------|
| Stack Name       | smart-bin-demo-app  |  This is AWS CloudFormation name once deployed.
| ArtefactsBucketName |       | Provide S3 bucket name where you uploaded the artifacts in step 4 of pre-requisite section |
| ProjectName  | smart-bin-demo-app | smart bin app project name                               |
| ResourcePrefix        | demo | The AWS resources are prefixed based on the value of this parameter. You must change this value when launching more than once within the same account.              |

When completed, choose *Next*
1. [Configure stack options](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-add-tags.html) if desired, then choose *Next*.
1. On the review you screen, you must check the boxes for:
    * "*I acknowledge that AWS CloudFormation might create IAM resources*"
    * "*I acknowledge that AWS CloudFormation might create IAM resources with custom names*"
    * "*I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND*"

   These are required to allow CloudFormation to create a Role to grant access to the resources needed by the stack and name the resources in a dynamic way.
1. Choose *Create Stack*
1. Wait for the CloudFormation stack to launch. Completion is indicated when the "Stack status" is "*CREATE_COMPLETE*".
    * You can monitor the stack creation progress in the "Events" tab.

## Local Development
See the [Local Development](docs/LOCAL_DEVELOPMENT.md) guide to get a copy of the project up and running on your local machine for development and testing purposes.

### Clean up

To avoid incurring future charges, please clean up the resources created.

To make cloud formation stack delete successfully, please carry out below steps first. Otherwise stack deletion might fail. 
1.	Please delete all the contents from the S3 bucket that was created by cloud formation script to upload sensor readings
2.	On AWS IoT Core Console, choose Things option under Manage section. Then press DemoWasteBin thing link. 
3.	Choose "**Certificates**" tab. Then choose each certificate and press "**detach**" button.
4.	Follow step 3 by choosing "**Certificates**" option under "**Secure**" section
5.	Finally "**Revoke**" and "**Delete**" all certificates one by one selecting Revoke and Delete option from "**Actions**" drop down under "**Secure**" section.

To remove the stack:

1. Open the AWS CloudFormation Console.
2. Choose the **smart-bin-demo-app** project, press "*Delete Stack*" button.
3. Your stack might take some time to be deleted. You can track its progress in the "Events" tab.
4. When it is done, the status changes from "DELETE_IN_PROGRESS" to "DELETE_COMPLETE". It then disappears from the list.


## Security
See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License
This library is licensed under the MIT-0 License. See the LICENSE file.
