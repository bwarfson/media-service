from typing import Any

from aws_lambda_env_modeler import get_environment_variables, init_environment_variables
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.parser.envelopes import ApiGatewayEnvelope
from aws_lambda_powertools.utilities.typing import LambdaContext

from media_service.handlers.models.dynamic_configuration import MyConfiguration
from media_service.handlers.models.env_vars import MyHandlerEnvVars
from media_service.handlers.utils.dynamic_configuration import parse_configuration
from media_service.handlers.utils.observability import logger, metrics, tracer
from media_service.handlers.utils.rest_api_resolver import ORDERS_PATH, app
from media_service.logic.create_order import create_order
from media_service.models.input import CreateOrderRequest
from media_service.models.output import CreateOrderOutput


@app.post(ORDERS_PATH)
def handle_create_media() -> dict[str, Any]:
    env_vars: MyHandlerEnvVars = get_environment_variables(model=MyHandlerEnvVars)
    logger.debug('environment variables', env_vars=env_vars.model_dump())

    my_configuration = parse_configuration(model=MyConfiguration)
    logger.debug('fetched dynamic configuration', configuration=my_configuration.model_dump())

    # we want to extract and parse the HTTP body from the api gw envelope
    create_input: CreateMediaRequest = parse(
        event=app.current_event.raw_event,
        model=CreateMediaRequest,
        envelope=ApiGatewayEnvelope,
    )
    logger.info('got create media request', media=create_input.model_dump())

    metrics.add_metric(name='ValidCreateMediaEvents', unit=MetricUnit.Count, value=1)
    response: CreateMediaOutput = create_media(
        media_request=create_input,
        table_name=env_vars.TABLE_NAME,
        context=app.lambda_context,
    )

    logger.info('finished handling create media request')
    return response.model_dump()


@init_environment_variables(model=MyHandlerEnvVars)
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@metrics.log_metrics
@tracer.capture_lambda_handler(capture_response=False)
def lambda_handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:
    return app.resolve(event, context)
