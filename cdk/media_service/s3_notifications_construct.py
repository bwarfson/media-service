from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_notifications as s3n
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class S3NotificationsConstruct(Construct):

    def __init__(self, scope: Construct, id_: str, bucket: s3.Bucket, queue: sqs.Queue) -> None:
        super().__init__(scope, id_)
        self.id_ = id_
        self.bucket = bucket
        self.queue = queue

        s3_event_role = iam.Role(self, 'S3EventRole', assumed_by=iam.ServicePrincipal('s3.amazonaws.com'))

        self.queue.grant_send_messages(s3_event_role)

        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.SqsDestination(self.queue),
        )
