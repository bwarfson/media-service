from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt


class CreateOrderRequest(BaseModel):
    customer_name: Annotated[str, Field(min_length=1, max_length=20)]
    order_item_count: PositiveInt

class PresignedUrlRequest(BaseModel):
    file_names: List[str]
    expiration: int = 3600

class CreateMediaRequest(BaseModel):
    media_name: Annotated[str, Field(min_length=1, max_length=20)]
    media_item_count: PositiveInt
    user_email: Annotated[str, Field(min_length=1, max_length=20)]
    user_id: Annotated[str, Field(min_length=1, max_length=20)]
    presigned_url_request: PresignedUrlRequest
