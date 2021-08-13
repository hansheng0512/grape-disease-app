from pydantic import BaseModel


class Base64str(BaseModel):
    base64str: str


class ResponseDataModel(BaseModel):
    filename: str
    content_type: str
    likely_class: str