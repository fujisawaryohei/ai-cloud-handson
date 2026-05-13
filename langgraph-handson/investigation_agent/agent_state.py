import operator
from typing import Annotated

from langchain_core.messages import AnyMessage
from pydantic import BaseModel


class AgentState(BaseModel):
    messages: Annotated[list[AnyMessage], operator.add]
