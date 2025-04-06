import asyncio
from agents.executive_summary import executive_summary
from agents.implementation_details import implementation_details
from agents.project_plan import project_plan
from agents.requirements_generation import requirements_generation
from agents.requirements_clarification import requirements_clarification
from agents.task_assignment import task_assignment
from agents.task_writer import task_writer

async def main():
    # Simulate a conversation with the customer
    clarifications = await requirements_clarification("I want create a basic hello world script.")

    await requirements_generation(clarifications["intent"], clarifications["questions_and_answers"])

    await executive_summary()

    await implementation_details()

    await task_writer()

    await task_assignment()

asyncio.run(main())
