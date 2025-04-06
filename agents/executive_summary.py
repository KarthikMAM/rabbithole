import asyncio

from mcp.types import BlobResourceContents, EmbeddedResource, TextContent
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent(name="ExecutiveSummaryAgent")


@fast.agent(
    name="executive_summary_generator",
    instruction="""
    You are a highly skilled Program Manager and Business Analyst. 
    You will be generating an executive summary by summarizing the document provided to you.

    Instructions:
    1. Read the document carefully.
    2. Identify the key points and main ideas.
    3. Summarize the document in a clear and concise manner.
    4. Use bullet points to highlight the key points.
    5. Ensure that the summary is easy to understand and free of jargon.
    6. Write the summary in a markdown file named `executive_summary.md` using the filesystem tool.
    """,
)
@fast.agent(name="executive_summary_evaluator")
@fast.evaluator_optimizer(
    generator="executive_summary_generator",
    evaluator="executive_summary_evaluator",
    max_refinements=5,
    min_rating="EXCELLENT",
    name="executive_summary_enhanced_generator",
)
@fast.agent(
    name="executive_summary_output",
    instruction="""
    You will write the output of the accepted markdown document to a file named `executive_summary.md` using the filesystem tool without any modifications.
    """,
    servers=["filesystem"],
)
async def executive_summary():
    async with fast.run() as agent:
        intent = f"""
        Document to summarize and create an executive summary from clarifications and requirements in the files.
        """
        result = await agent.executive_summary_enhanced_generator(intent)

        await agent.executive_summary_output(result)

if __name__ == "__main__":
    asyncio.run(
        executive_summary(open("data/files/requirements.md", "r").read())
    )