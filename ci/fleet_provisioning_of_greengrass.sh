#!/usr/bin/env bash

#Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#SPDX-License-Identifier: MIT-0

mkdir -p build/certs/
curl -o build/certs/AmazonRootCA1.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem

chmod 745 build
chmod 700 build/certs
chmod 644 build/certs/AmazonRootCA1.pem

#cp AmazonRootCA1.pem build/certs/

# Retrieve provisioning certificates from secrets manager
SECRET_ARN=$(aws cloudformation list-exports | jq -r '.Exports[] | select(.Name=="FleetProvisioningCertificateSecret") | .Value')
SECRET=$(aws secretsmanager get-secret-value --secret-id "$SECRET_ARN" | jq -r '.SecretString')
jq --arg s "$SECRET" -jn '$s | fromjson | .certificate' > build/certs/cert.pem
jq --arg s "$SECRET" -jn '$s | fromjson | .privateKey' > build/certs/privateKey.pem


# Download the greengrass runtime and plugins
GG_VERSION='2.4.0'
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-$GG_VERSION.zip > build/greengrass-nucleus.zip
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/aws-greengrass-FleetProvisioningByClaim/fleetprovisioningbyclaim-latest.jar > build/aws.greengrass.FleetProvisioningByClaim.jar

DATA_ENDPOINT=$(aws iot describe-endpoint --endpoint-type iot:Data-ATS --output text)
CREDENTIALS_ENDPOINT=$(aws iot describe-endpoint --endpoint-type iot:CredentialProvider --output text)
TEMPLATE_NAME=$(aws cloudformation list-exports | jq -r '.Exports[] | select(.Name=="FleetProvisioningTemplate") | .Value')
ROOT='/greengrass/v2'

cat >build/config.yml <<EOF
---
services:
  aws.greengrass.Nucleus:
    version: 2.4.0
    configuration:
      awsRegion: eu-west-1
  aws.greengrass.FleetProvisioningByClaim:
    configuration:
      rootPath: $ROOT/
      awsRegion: eu-west-1
      iotDataEndpoint: $DATA_ENDPOINT
      iotCredentialEndpoint: $CREDENTIALS_ENDPOINT
      iotRoleAlias: GreengrassTokenExchangeAlias
      provisioningTemplate: $TEMPLATE_NAME
      claimCertificatePath: $ROOT/certs/cert.pem
      claimCertificatePrivateKeyPath: $ROOT/certs/privateKey.pem
      rootCaPath: $ROOT/certs/AmazonRootCA1.pem
      templateParameters:
        ThingName: DemoWasteBin
        Location: London
        SerialNumber: W123
EOF

cp fleet_provision.sh build/
chmod 755 build/fleet_provision.sh
