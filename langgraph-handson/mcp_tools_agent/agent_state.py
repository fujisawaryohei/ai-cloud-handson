import operator
from typing import Annotated, List

from langchain_core.messages import AnyMessage
from pydantic import BaseModel


class AgentState(BaseModel):
    messages: Annotated[List[AnyMessage], operator.add]
