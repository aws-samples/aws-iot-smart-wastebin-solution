# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os
from invoke import run
import sys
import time
from datetime import datetime

from hx711_i2c import HX711_I2C


def get_image_full_path(path: str, name: str) -> None:
    return os.path.join(path, name)


class Sensors:
    def __init__(
        self,
        location: str,
        post_code: str,
        bucket: str,
        local_garbage_path: str,
        image_name: str = "waste_image.jpg",
    ):

        # Initilize veriables
        self._sensor_deployed_location = location
        self._sensor_deployed_post_code = post_code
        self._local_path = local_garbage_path
        self._image_name = image_name
        self._bucket = bucket
        self._local_image_full_path = get_image_full_path(
            local_garbage_path, image_name
        )

        # Camera initialization
        self._clip_duration_in_msec = 1000
        self._shutter_speed_in_micro_secs = 20000

        # Load cell sensor initlization
        self._IIC_MODE = 0x01  # default use IIC1
        self._IIC_ADDRESS = 0x64  # default i2c device address
        """
           # The first  parameter is to select iic0 or iic1
           # The second parameter is the iic device address
        """
        self._hx711 = HX711_I2C(self._IIC_MODE, self._IIC_ADDRESS)
        self._hx711.begin()
        print("start\r\n")
        # Manually set the calibration values
        self._hx711.setCalibration(2210.0)
        # peel
        self._hx711.peel()

    def getUniqImageKey(self, waste_image_timestamp: float) -> None:

        key = f"waste_image_{waste_image_timestamp}.jpg"
        destination_path = os.path.join(
            self._sensor_deployed_location, self._sensor_deployed_post_code, key
        )

        return destination_path

    def build_waste_weight_stats(
        self, weight: float, waste_image_timestamp: float
    ) -> None:

        # weight=random.randint(1,10)
        uniq_key = f"waste_image_{waste_image_timestamp}.jpg"

        destination_path = os.path.join(
            self._sensor_deployed_location, self._sensor_deployed_post_code, uniq_key
        )
        s3_uri = f"s3://{self._bucket}/{destination_path}"

        # print(f'publish_waste_weight_stats:{s3_uri}')
        timestamp = time.time()

        event = {
            "timestamp": timestamp,
            "sensor_id": os.getenv("AWS_IOT_THING_NAME"),
            "thingname": os.getenv("AWS_IOT_THING_NAME"),
            "sensorvalue": weight,
            "s3_image_uri": s3_uri,
            "location": self._sensor_deployed_location,
            "postcode": self._sensor_deployed_post_code,
            "latitude": 51.579677,
            "longitude": -0.335836,
            "country": "United Kingdom",
            "city": "London",
        }

        return event

    def calculateThreshold(self, previous_weight: float = 0.0) -> None:
        threshold = 50.0
        return previous_weight + threshold

    def readWeightSensor(self) -> None:
        current_weight = previous_weight = 0.0
        waste_image_timestamp = 0
        done = False
        # Ignore noise until weight is stable. Below loop should be replaced by queue
        while not done:
            current_weight = self._hx711.readWeight(10)
            # print('weight is {:.1f} g, previous weight {:.1f} g'.format(round(current_weight,0),round(previous_weight,0)))
            if round(current_weight, 0) != round(previous_weight, 0):
                previous_weight = current_weight
            else:
                done = True

        print("######### final stable weight from sensor is %.1f g" % current_weight)
        return current_weight if current_weight > 0.0 else 0.0
        # except Exception as ex:
        #     #Catch I/O exception to ignore and conitue
        #     print(ex)
        #     return 0

    def trigger_camera(self, shutter_speed: int, clip_duration: int) -> None:
        filename = f"{self._local_path}/{self._image_name}"
        cmd = f"libcamera-jpeg --width 800 --height 600 --nopreview -o {filename} -t {clip_duration} --shutter {shutter_speed}"
        run(cmd,hide=True)

        # return latest camera image timestamp
        statinfo = os.stat(filename)
        return statinfo.st_mtime
