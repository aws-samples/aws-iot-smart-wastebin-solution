# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import QOS, PublishToIoTCoreRequest


class MqttPublisher:
    def __init__(self, topic: str, timeout: int = 10):
        self._client = awsiot.greengrasscoreipc.connect()
        self._topic = topic
        self._timeout = timeout

    def publish(self, message: object) -> None:
        request = PublishToIoTCoreRequest(
            topic_name=self._topic,
            qos=QOS.AT_LEAST_ONCE,
            payload=json.dumps(message).encode(),
        )

        operation = self._client.new_publish_to_iot_core()
        operation.activate(request)
        try:
            result = operation.get_response().result(timeout=self._timeout)
            print(f"Successfully published message to IoT core: {result}")
        except Exception as ex:
            print(ex)
