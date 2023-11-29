from aws_cdk import CfnOutput, RemovalPolicy
from aws_cdk import aws_dynamodb as dynamodb
from constructs import Construct

import cdk.media_service.constants as constants


class ApiDbConstruct(Construct):

    def __init__(self, scope: Construct, id_: str) -> None:
        super().__init__(scope, id_)

        self.db: dynamodb.Table = self._build_db(id_)
        self.idempotency_db: dynamodb.Table = self._build_idempotency_table(id_)

    def _build_idempotency_table(self, id_: str) -> dynamodb.Table:
        table_id = f'{id_}{constants.IDEMPOTENCY_TABLE_NAME}'
        table = dynamodb.Table(
            self,
            table_id,
            table_name=table_id,
            partition_key=dynamodb.Attribute(name='id', type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
            time_to_live_attribute='expiration',
            point_in_time_recovery=True,
        )
        CfnOutput(self, id=constants.IDEMPOTENCY_TABLE_NAME_OUTPUT,
                  value=table.table_name).override_logical_id(constants.IDEMPOTENCY_TABLE_NAME_OUTPUT)
        return table

    def _build_db(self, id_prefix: str) -> dynamodb.Table:
        table_id = f'{id_prefix}{constants.TABLE_NAME}'
        table = dynamodb.Table(
            self,
            table_id,
            table_name=table_id,
            partition_key=dynamodb.Attribute(
                name='PK',
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='SK',
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        table.add_global_secondary_index(
            index_name='GSI1',
            partition_key=dynamodb.Attribute(
                name='GSI1PK',
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='GSI1SK',
                type=dynamodb.AttributeType.STRING
            )
        )

        table.add_global_secondary_index(
            index_name='GSI2',
            partition_key=dynamodb.Attribute(
                name='GSI2PK',
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='GSI2SK',
                type=dynamodb.AttributeType.STRING
            )
        )

        CfnOutput(self, id=constants.TABLE_NAME_OUTPUT, value=table.table_name).override_logical_id(constants.TABLE_NAME_OUTPUT)
        return table
