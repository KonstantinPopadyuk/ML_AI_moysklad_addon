from agents import json_getter_agent, decomposition_agent, analytics_agent, summary_agent
from agents import FinalResults

import asyncio
# import logfire
from dotenv import load_dotenv
load_dotenv()

from utils import *
import asyncio
import json


async def agents_run(question) -> FinalResults:
    try:
        final_answers = []
        structual_questions: List[str] = await decomposition_agent.run(question)
        structual_questions = structual_questions.data
        if structual_questions[0] == 'Please ask more relevant question':
            return FinalResults(summary='Please ask more relevant question', table=None)
        for q in structual_questions:
            data_to_analyze = await json_getter_agent.run(q)
            data_insights = await analytics_agent.run(str(data_to_analyze.data))
            final_answers.append({
                'question':q,
                'tabular_data':data_to_analyze.data,
                'data_insights':data_insights.data
                })
        all_answers = json.dumps(final_answers)
        final_answer = await summary_agent.run(all_answers)
        return final_answer.data
    except Exception as e:
        return f'Something goes wrong with AI {e}'

async def main() -> None:
    consumer = await start_consumer()
    producer = await start_producer()
    try:
        async for question in consumer:
            decoded_message = json.loads(question.value)
            ai_message_response = await agents_run(question=decoded_message['message'])
            response = {'message': ai_message_response.summary,
                        'table': ai_message_response.table, 
                        'user_id': decoded_message['user_id'], 
                        'message_id': decoded_message['message_id']}
            response = json.dumps(response).encode(encoding="utf-8")
            await producer.send('AI_agents_answers', response)

    finally:
        await consumer.stop()
        await producer.stop()

if __name__ == '__main__':
    asyncio.run(main())