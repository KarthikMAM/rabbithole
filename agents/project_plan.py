import asyncio

from mcp.types import BlobResourceContents, EmbeddedResource, TextContent
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent(name="ProjectPlanAgent")

@fast.agent(
    name="project_plan_generator",
    instruction="""
    You are a highly skilled person familiar with the AGILE world. 
    You will be generating a detailed list of tasks and subtasks for a project based on the provided requirements and implementation details.
    You have access to the filesystem tool to read the document and generate a markdown file.

    Instructions:
    1. Read the requirements and implementation details from the provided document carefully.
    2. Generate a detailed list of tasks and subtasks for the project.
    3. Ensure that the tasks are clear, actionable, and well-defined.
    4. Use markdown formatting for the output.
    5. Ensure that tasks have clear boundaries and are not too vague or overlap with eachother.
    6. Each task must be idependetly completelable by a single person.
    7. For each task list the following sections description, acceptance criteria, dependencies, priority, estimated time, skills needed.
    """,
    servers=["filesystem"],
)
@fast.agent(name="project_plan_evaluator")
@fast.evaluator_optimizer(
    generator="project_plan_generator",
    evaluator="project_plan_evaluator",
    max_refinements=5,
    min_rating="EXCELLENT",
    name="project_plan_enhanced_generator",
)
@fast.agent(
    name="project_plan_output",
    instruction="""
    You will write the output of the accepted markdown document to a file named `project_plan.md` using the filesystem tool without any modifications.
    """,
    servers=["filesystem"],
)
async def project_plan():
    async with fast.run() as agent:
        intent = f"""
        You will go through all the files in the `files` folder using the filesystem tool's allowed directories to come up with a detailed project plan.
        """
        result = await agent.project_plan_enhanced_generator(intent)

        await agent.project_plan_output(result)

if __name__ == "__main__":
    asyncio.run(
        project_plan()
    )