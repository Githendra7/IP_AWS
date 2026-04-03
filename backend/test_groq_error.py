import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from app.ai.agents.phase1_functional import phase1_generator

async def test():
    try:
        print("Invoking Groq...")
        res = await phase1_generator.ainvoke({
            "problem_statement": "smart calendar",
            "validation_feedback": ""
        })
        print("Success:", res)
    except Exception as e:
        print("ERROR OCCURRED:")
        print(type(e))
        print(e)
        if hasattr(e, 'response'):
            print(e.response.text)

if __name__ == "__main__":
    asyncio.run(test())
