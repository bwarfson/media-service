from aws_cdk import RemovalPolicy
from aws_cdk import aws_s3 as s3
from constructs import Construct

import cdk.media_service.constants as constants


class S3Construct(Construct):

    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)
        self.id_ = id_
        self.access_logs_bucket = self._build_access_logs_bucket(id_)
        self.temp_bucket = self._build_temp_bucket(id_)

    def _build_access_logs_bucket(self, id_: str) -> s3.Bucket:
        return s3.Bucket(self, id=f'{id_}{constants.ACCESS_LOGS_BUCKET_NAME}', bucket_name=f'{self.id_}{constants.ACCESS_LOGS_BUCKET_NAME}',
                         access_control=s3.BucketAccessControl.LOG_DELIVERY_WRITE, block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                         encryption=s3.BucketEncryption.S3_MANAGED, object_ownership=s3.ObjectOwnership.OBJECT_WRITER, public_read_access=False,
                         removal_policy=RemovalPolicy.RETAIN, versioned=True, enforce_ssl=True)

    def _build_temp_bucket(self, id_: str) -> s3.Bucket:
        return s3.Bucket(self, id=f'{id_}{constants.TEMP_BUCKET_NAME}', bucket_name=f'{self.id_}{constants.TEMP_BUCKET_NAME}',
                         access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL, block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                         encryption=s3.BucketEncryption.S3_MANAGED, object_ownership=s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
                         public_read_access=False, removal_policy=RemovalPolicy.RETAIN, server_access_logs_bucket=self.access_logs_bucket,
                         server_access_logs_prefix='temp-bucket/serverAccessLogging_', versioned=False, enforce_ssl=True)
