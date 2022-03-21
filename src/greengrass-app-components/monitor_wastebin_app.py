# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os
import random
import sys
import time
from datetime import datetime

from image_stream import ImageStream
from mqtt_publisher import MqttPublisher
from sensors import Sensors


def monitor_waste_bin():
    current_weight = previous_weight = 0.0
    waste_image_timestamp = 0
    while True:
        try:
            current_weight = sensors.readWeightSensor()
            print(
                f"current_weight={current_weight} - previous weight={previous_weight} - calculatred weight:{sensors.calculateThreshold(previous_weight)}"
            )
            if current_weight >= sensors.calculateThreshold(previous_weight):
                # Take waste photo
                waste_image_timestamp = sensors.trigger_camera(
                    sensors._shutter_speed_in_micro_secs, sensors._clip_duration_in_msec
                )
                event = sensors.build_waste_weight_stats(
                    current_weight, waste_image_timestamp
                )

                # Push waste image first to cloud in readiness for waste sorting analysis
                destination_path = sensors.getUniqImageKey(waste_image_timestamp)
                uploader.upload(destination_path, sensors._local_image_full_path)
                print(f"Published Image to: {destination_path}")

                # Publish waste weight data to IoT core
                publisher.publish(event)
                print(f"Published weight data : {event}")

            previous_weight = current_weight

            time.sleep(2)

        except Exception as ex:
            # Catch I/O exception to ignore and continue
            print(ex)
            continue


def main() -> None:
    try:
        monitor_waste_bin()
    except Exception as ex:
        print(ex)
        raise


if __name__ == "__main__":
    try:

        # Initilize Sensors
        temp_local_image_path = "/tmp/garbage_bin"
        cloud_bucket_name = os.getenv('TRASH_BUCKET')  # TODO: hardcoded bucket name, has to be dynamic, SSM store maybe?
        image_name = "waste_image.jpg"
        location = "Greenhill"
        post_code = "HA11AA"

        sensors = Sensors(
            location, post_code, cloud_bucket_name, temp_local_image_path, image_name
        )

        # Initilize Stream manager client
        local_stream_name = "ab3-image-upload"
        uploader = ImageStream(local_stream_name, cloud_bucket_name)

        # Initilize MQTT client
        mqtt_topic = "smart/trash_bin"
        publisher = MqttPublisher(mqtt_topic)

        # Start sensor reading app
        main()
    except Exception as ex:
        print(ex)
        raise
