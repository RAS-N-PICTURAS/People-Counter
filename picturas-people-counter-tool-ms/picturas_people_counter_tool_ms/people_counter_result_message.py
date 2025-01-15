from typing import Any

from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .people_counter_request_message import PeopleCounterRequestMessage


class PeopleCounterResultOutput(BaseModel):
    type: str
    count: int
    processedImageURI: str


class PeopleCounterResultMessage(ResultMessage[PeopleCounterResultOutput]):

    def __init__(self, request: PeopleCounterRequestMessage, tool_result: Any, exception: Exception, *args):
        super().__init__(request, tool_result, exception, *args)
        if exception is None:
            self.output = PeopleCounterResultOutput(
                type="people_count",
                count=tool_result,  # The result from the tool will be the count of people
                processedImageURI=request.parameters.outputImageURI,
            )
