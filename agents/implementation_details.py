import asyncio

from mcp.types import BlobResourceContents, EmbeddedResource, TextContent
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent(name="ImplementationDetailsAgent")

@fast.agent(
    name="implementation_details_generator",
    instruction="""
    You are a domain expert in the field of Program Management and Business Analysis.
    You will be generating a detailed strategy document or low-level design document based on the requirements given to you.
    Use sequential thinking for each turn and ensure that you are not missing any key points.

    Instructions:
    1. Read the requirements carefully.
    2. Identify the key points, key modules, ingridients and main ideas.
    3. Figure out the best way to implement the requirements.
    4. Create a detailed strategy document or low-level design document.
    5. Search for relevant information and best practices.
    6. Ensure that the document is well-structured and easy to understand.
    7. Use bullet points to highlight the key points.
    8. Use UML to generate diagrams where needed.
    """,
    servers=["filesystem", "sequential_thinking"],
)
@fast.agent(name="implementation_details_evaluator")
@fast.evaluator_optimizer(
    generator="implementation_details_generator",
    evaluator="implementation_details_evaluator",
    max_refinements=2,
    min_rating="GOOD",
    name="implementation_details_enhanced_generator",
)
@fast.agent(
    name="implementation_details_output",
    instruction="""
    You will write the output of the accepted markdown document to a file named `implementation_details.md` using the filesystem tool without any modifications.
    """,
    servers=["filesystem"],
)
async def implementation_details():
    async with fast.run() as agent:
        intent = f"""
        You will go through all the files in the files/ folder using the filesystem tool to come up with a detailed document to implement the user requirements.
        """
        result = await agent.implementation_details_enhanced_generator(intent)

        await agent.implementation_details_output(result)

if __name__ == "__main__":
    # Example usage
    document = "Prepare chicken 65 with medium spice level and use 4-5 servings prepared with minimal oil in air fryer."
    asyncio.run(implementation_details(document))