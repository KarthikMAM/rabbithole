import asyncio
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent(name="RequirementsGenerationAgent")

@fast.agent(
    name="requirements_generation_generator",
    instruction="""
    You are a highly skilled requirements generation agent.
    You are given a customer intent and the clarifying question and answer pairs that have been asked so far.
    Your task is to generate a set of requirements based on the customer intent and the clarifying questions.
    You should ensure that the requirements are clear, concise, and actionable.
    You should also ensure that the requirements are complete and cover all aspects of the customer intent.
    """,
)
@fast.agent(name="requirements_generation_evaluator")
@fast.evaluator_optimizer(
    generator="requirements_generation_generator",
    evaluator="requirements_generation_evaluator",
    max_refinements=5,
    min_rating="EXCELLENT",
    name="requirements_generation_enhanced_generator",
)
@fast.agent(
    name="requirements_generation_output",
    instruction="""
    You will write the final set of requirements and the customer intent to `requirements.md` in the following format to the teeth:

    ```md
    # Customer Intent
    {customer_intent}

    # Clarifying Questions and Answers
    {clarifying_questions_and_answers}

    # Requirements
    {requirements}
    ```

    Instructions:
    1. Write the customer intent and clarifying questions and answers in the format above.
    2. Write the requirements in the format above.
    3. Ensure that the requirements are clear, concise, and actionable.
    4. Ensure that the requirements are complete and cover all aspects of the customer intent.
    5. Write the requirements in a markdown file named `requirements.md` using the filesystem tool.
    """,
    servers=["filesystem"],
)
async def requirements_generation(intent: str, clarifications: str):
    async with fast.run() as agent:
        customer_intent = f"""
        Customer Intent: {intent}

        Clarifying Questions and Answers:
        - {clarifications}
        """
        
        await agent.requirements_generation_output(await agent.requirements_generation_enhanced_generator(customer_intent))

if __name__ == "__main__":
    asyncio.run(requirements_generation(
        intent="The customer wants to build a new e-commerce website.",
        clarifications="What features do you want? - I want a shopping cart and payment gateway."
    ))