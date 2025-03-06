from pydantic_ai import Agent
from pydantic_ai import RunContext
from typing import Dict, Any, List, Optional
from pydantic_ai.models.openai import OpenAIModel
import os
import requests

model = OpenAIModel(
    'deepseek-chat',
    base_url='https://api.deepseek.com',
    api_key=os.getenv('DEEPSEEK_API_KEY'),
)

json_getter_agent = Agent(model,
              system_prompt=(
                """
                You are an Agent that should use only one tool and immideatly give response of this tool as it is
                Your main goal only choose correct tool
                If you dont have any correct tool return None
                You must return results in JSON format
                """

              ),
              result_type=Dict[str, Any])

ML_SERVICE_URL = 'http://localhost:8010'

@json_getter_agent.tool
async def generate_agents_type_report(ctx: RunContext[None]) -> Dict[str, Any]:
    """
    This tool give a report by customer type in JSON format
    """
    print('i dont know what to do')
    response = requests.get(f'{ML_SERVICE_URL}/get_agents_type_report').json()
    return {"data": response}

@json_getter_agent.tool
async def generate_agents_name_report(ctx: RunContext[None]) -> Dict[str, Any]:
    """
    This tool give a report by customer name in JSON format
    """
    print('i dont know what to do')
    response = requests.get(f'{ML_SERVICE_URL}/get_agents_name_data').json()
    return {"data": response}

@json_getter_agent.tool
async def generate_item_type_report(ctx: RunContext[None]) -> Dict[str, Any]:
    """
    This tool give a report by product type in JSON format
    """
    print('i dont know what to do')
    response = requests.get(f'{ML_SERVICE_URL}/get_item_type_data').json()
    return {"data": response}

@json_getter_agent.tool
async def generate_volumes_report(ctx: RunContext[None]) -> Dict[str, Any]:
    """
    This tool give a report by product volume in JSON format
    """
    print('i dont know what to do')
    response = requests.get(f'{ML_SERVICE_URL}/get_volumes_data').json()
    return {"data": response}

@json_getter_agent.tool
async def generate_cityname_report(ctx: RunContext[None]) -> Dict[str, Any]:
    """
    This tool give a report by city name in JSON format
    """
    print('i dont know what to do')
    response = requests.get(f'{ML_SERVICE_URL}/get_city_data').json()
    return {"data": response}


@json_getter_agent.tool
async def generate_predictions(ctx: RunContext[None]) -> Dict[str, Any]:
    """
    This tool give stock predictions in JSON format
    """
    print('try to extract from right tool')
    response = requests.get(f'{ML_SERVICE_URL}/create_stock_preds?n=30').json()
    print(f'{response[:10]=}')
    return {"data": response[:10]}



