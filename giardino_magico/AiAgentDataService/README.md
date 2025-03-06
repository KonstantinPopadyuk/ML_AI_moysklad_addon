# AI Agent Data Service

A distributed AI agent system built with pydantic AI for processing and analyzing structured data.

## Overview

The system consists of multiple specialized AI agents that work together to:
1. Decompose complex questions into structured sub-questions
2. Retrieve relevant data from various sources
3. Analyze tabular data and generate insights
4. Summarize findings into actionable recommendations

## Architecture

### Core Components

- **Decomposition Agent**: Breaks down user questions into structured sub-questions
- **JSON Getter Agent**: Retrieves relevant tabular data in JSON format
- **Analytics Agent**: Analyzes tabular data and provides insights
- **Summary Agent**: Synthesizes results into final recommendations

### Data Flow

1. User question → Decomposition Agent
2. Sub-questions → JSON Getter Agent
3. Tabular data → Analytics Agent
4. Insights → Summary Agent
5. Final response → User

## Installation

The service will:
1. Listen for incoming messages via Kafka
2. Process questions through the agent pipeline
3. Return structured responses

## API Response Format

## Dependencies

- pydantic-ai
- aiokafka
- python-dotenv
- asyncio

## License

MIT License
