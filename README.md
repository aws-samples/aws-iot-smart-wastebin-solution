<h1 align="center">
AWS IoT Smart Wastebin solution
<br>
   <a href="https://github.com/aws-samples/aws-iot-smart-wastebin-solution/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/aws-samples/aws-iot-smart-wastebin-solution?display_name=tag"></a>
   <a href="https://github.com/aws-samples/aws-iot-smart-wastebin-solution/actions"><img alt="GitHub Workflow Status" src="https://github.com/aws-samples/aws-iot-smart-wastebin-solution/workflows/Unit%20Tests/badge.svg"></a>
</h1>

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
3. An S3 bucket to upload all the artifacts from the cloned repository under src/greengrass-app-component directory
4. Upload all the artifacts to AWS S3 Bucket
    1. On AWS Console, choose "**S3**" service
    2. Choose your bucket created as mentioned step 3
    3. Press "**Create folder**" button
    4. Enter "**greengrass-app-component**" in folder name field and press "**Create folder**" button
    5. Choose the "**greengrass-app-component**" folder and press "**Upload**" button
    6. Press "**Add files**" button on upload screen and choose all the files from greengrass-app-component
    7. Finally, press "**Upload**" button
    8. Please make sure that all the artifacts are under "**s3://<your bucket name>/greengrass-app-component**". This is very important to ensure that path is correct for successful deployment on edge gateway


#### Deployment
The application is deployed as an [AWS CloudFormation](https://aws.amazon.com/cloudformation) template.

> **Note**
You are responsible for the cost of the AWS services used while running this sample deployment. There is no additional
cost for using this sample. For full details, see the pricing pages for each AWS service that you use in this sample. Prices are subject to change.

1. Deploy the latest CloudFormation template by following the link below for your preferred AWS region:

| Region                                | Launch Template                                                                                                                                                                                                                                                                                        |
|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **US East (N. Virginia)** (us-east-1) | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=iot-smart-wastebin&templateURL=https://s3.amazonaws.com/solution-builders-us-east-1/aws-iot-smart-wastebin-solution/latest/main.template)           |
| **US West (Oregon)** (us-west-2)      | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=iot-smart-wastebin&templateURL=https://s3.amazonaws.com/solution-builders-us-west-2/aws-iot-smart-wastebin-solution/latest/main.template)           |
| **EU (Ireland)** (eu-west-1)          | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=iot-smart-wastebin&templateURL=https://s3.amazonaws.com/solution-builders-eu-west-1/aws-iot-smart-wastebin-solution/latest/main.template)           |
| **EU (Frankfurt)** (eu-central-1)     | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=iot-smart-wastebin&templateURL=https://s3.amazonaws.com/solution-builders-eu-central-1/aws-iot-smart-wastebin-solution/latest/main.template)     |
| **AP (Sydney)** (ap-southeast-2)      | [![Launch CloudFormation Stack](docs/deploy-to-aws.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=iot-smart-wastebin&templateURL=https://s3.amazonaws.com/solution-builders-ap-southeast-2/aws-iot-smart-wastebin-solution/latest/main.template) |

2. If prompted, login using your AWS account credentials.
1. You should see a screen titled "*Create Stack*" at the "*Specify template*" step. The fields specifying the CloudFormation
   template are pre-populated. Choose the *Next* button at the bottom of the page.
1. On the "*Specify stack details*" screen you can customize the following parameters of the CloudFormation stack:

| Parameter label     | Default            | Description                                                                                                                                            |
|---------------------|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Stack Name          | aws-iot-smart-wastebin-solution | This is AWS CloudFormation name once deployed.                                                                                                         |
| ArtefactsBucketName | `required`         | Provide S3 bucket name where you uploaded the artifacts in step 4 of pre-requisite section                                                             |
| Project Name         | smart-bin-demo-app | smart bin app project name                                                                                                                             |
| Environment Type    | Dev                | The type of environment with which to tag your infrastructure. Valid values are DEV (development), TEST (test), or PROD (production) |
| IoT Core Role Alias | GreengrassTokenExchangeAlias             | Create an AWS IoT Core role alias. The alias must contain 1-128 characters and must include only alphanumeric characters and the =, @, and - symbols. |

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

## Test the solution
Once the resources are set up on AWS cloud, please deploy AWS greengrass and application on your IoT gateway i.e. Raspberry PI for testing E2E solution. Please refer the steps [Deploy AWS IoT Greengrass on IoT Gateway](docs/AWS_IoT_Greengrass_Setup.pdf)

## Local Development
See the [Local Development](docs/LOCAL_DEVELOPMENT.md) guide to get a copy of the project up and running on your local machine for development and testing purposes.

### Clean up

To avoid incurring future charges, please clean up the resources created.

To make cloud formation stack delete successfully, please carry out below steps first. Otherwise, stack deletion might fail.
1.	Please delete all the contents from the S3 bucket that was created by cloud formation script to upload sensor readings
2.	On AWS IoT Core Console, choose Things option under Manage section. Then press DemoWasteBin thing link.
3.	Choose "**Certificates**" tab. Then choose each certificate and press "**detach**" button.
4.	Follow step 3 by choosing "**Certificates**" option under "**Secure**" section
5.	Finally "**Deactivate**" and "**Delete**" all certificates one by one selecting Deactivate and Delete option from "**Actions**" drop down under "**Secure**" section.

To remove the stack:

1. Open the AWS CloudFormation Console.
2. Choose the **aws-iot-smart-wastebin-solution** project, press "*Delete Stack*" button.
3. Your stack might take some time to be deleted. You can track its progress in the "Events" tab.
4. When it is done, the status changes from "DELETE_IN_PROGRESS" to "DELETE_COMPLETE". It then disappears from the list.


## Security
See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License
This library is licensed under the MIT-0 License. See the LICENSE file.
