from pydantic_ai import Agent
from pydantic_ai import RunContext
from typing import Dict, Any, List, Optional, Union
from pydantic_ai.models.openai import OpenAIModel
import os
from pydantic import BaseModel, Field

model = OpenAIModel(
    'deepseek-chat',
    base_url='https://api.deepseek.com',
    api_key=os.getenv('DEEPSEEK_API_KEY'),
)

class FinalResults(BaseModel):
    summary: str = Field(description='Summary returned to the customer')
    table: Union[dict, None] = Field(description='Table data in JSON if needed')


summary_agent = Agent(model,
              system_prompt=(
                """
                You are an agent who can aggregate tabular and analytical information.
                Your main task is to extract the essence from a set of tables and analytics.
                All repetitions, redundancy must be removed.
                If tables are necessary to understand the information, then provide tabular information.
                Provide answer in russian language.
                """
              ),
              result_type=FinalResults)
