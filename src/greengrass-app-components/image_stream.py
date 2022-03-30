# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import stream_manager
from stream_manager.util import Util


class ImageStream:
    """Uploads images to S3 via the Greengrass Stream Mamanger"""

    def __init__(self, stream_name: str, bucket_name: str):
        self._client = stream_manager.StreamManagerClient()
        self._stream_name = stream_name
        self._bucket = bucket_name

        if not stream_name in self._client.list_streams():
            options = stream_manager.MessageStreamDefinition(
                name=stream_name,
                strategy_on_full=stream_manager.StrategyOnFull.OverwriteOldestData,
                export_definition=stream_manager.ExportDefinition(
                    s3_task_executor=[
                        stream_manager.S3ExportTaskExecutorConfig(
                            identifier=f"s3{stream_name}"
                        )
                    ]
                ),
            )
            self._client.create_message_stream(options)
            print(f"Created new message stream {stream_name}")
        else:
            print(f"Using existing message stream {stream_name}")

    def upload(self, destination_path: str, local_path: str) -> None:

        export_task = stream_manager.S3ExportTaskDefinition(
            input_url=f"file://{local_path}", bucket=self._bucket, key=destination_path
        )
        try:
            data = Util.validate_and_serialize_to_json_bytes(export_task)
            self._client.append_message(self._stream_name, data)
            print(f"Image uploaded to bucket {destination_path}")
        except Exception as ex:
            print(ex)
            raise
