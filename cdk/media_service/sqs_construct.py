from aws_cdk import Duration
from aws_cdk import aws_sqs as sqs
from constructs import Construct

import cdk.media_service.constants as constants


class SQSConstruct(Construct):

    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)
        self.id_ = id_
        self.dead_letter_queue = self._build_dead_letter_queue(id_)
        self.queue = self._build_queue(id_)

    def _build_dead_letter_queue(self, id_: str) -> sqs.Queue:
        return sqs.Queue(
            self,
            id=f'{id_}{constants.DEAD_LETTER_QUEUE_NAME}',
            queue_name=f'{self.id_}{constants.DEAD_LETTER_QUEUE_NAME}',
            retention_period=Duration.days(constants.DLQ_RETENTION_PERIOD),
            enforce_ssl=True,
        )

    def _build_queue(self, id_: str) -> sqs.Queue:
        return sqs.Queue(
            self,
            id=f'{id_}{constants.QUEUE_NAME}',
            queue_name=f'{self.id_}{constants.QUEUE_NAME}',
            retention_period=Duration.days(constants.QUEUE_RETENTION_PERIOD),
            visibility_timeout=Duration.seconds(constants.QUEUE_VISIBILITY_TIMEOUT),
            enforce_ssl=True,
            receive_message_wait_time=Duration.seconds(constants.QUEUE_RECEIVE_MESSAGE_WAIT_TIME),
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=constants.DEAD_LETTER_QUEUE_MAX_RECEIVE_COUNT,
                queue=self.dead_letter_queue,
            ),
        )
