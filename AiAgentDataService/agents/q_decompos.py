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

decomposition_agent = Agent(model,
              system_prompt=(
                """
                You are an agent who must decompose the user's question into individual components.
                Imagine that you have access to a database of reports that consist of the following sections (by row):
                - by customer name
                - by customer type
                - by product type
                - by product volume
                - by city name
                Each of this reports have columns:
                - section name
                - number of products
                - average product price
                - average order price
                - average order amount

                You also have access to a stock forecast report

                Your task is to understand what the user wants and how these reports can help him with this. 
                If his question is most likely completely covered by one report, then it is enough to add only one report. 
                Try to reduce the number of reports required to answer.

                Example:
                Question: 'Show me what products I need to order for the nearest period of time'
                Answer: ['Stock forecast']

                Question: 'Show me what products I need to order for the nearest period of time 
                and what products we sell best'
                Answer: ['Stock forecast', 'Report by product name']

                If the user's question cannot be decomposed or is not relevant to the data in this reports and forecasts
                return ['Please ask more relevant question']
                """
              ),
              result_type=List[str])
