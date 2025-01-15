from pydantic import BaseModel

from .core.messages.request_message import RequestMessage


class PeopleCounterParameters(BaseModel):
    inputImageURI: str
    outputImageURI: str


PeopleCounterRequestMessage = RequestMessage[PeopleCounterParameters]
