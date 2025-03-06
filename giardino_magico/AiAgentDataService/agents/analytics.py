from pydantic_ai import Agent
from pydantic_ai import RunContext
from typing import Dict, Any, List, Optional
from pydantic_ai.models.openai import OpenAIModel
import os

model = OpenAIModel(
    'deepseek-chat',
    base_url='https://api.deepseek.com',
    api_key=os.getenv('DEEPSEEK_API_KEY'),
)

analytics_agent = Agent(model,
              system_prompt=(
                  'You are an analytics agent that can analyze tabular data (that can be represent as JSON)'
                  'You must return just string with analytics'
                  'Main goal for analytics is general recommendations that can increase revenue or decrease costs'
              ),
              result_type=str)
