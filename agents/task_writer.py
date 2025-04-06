import asyncio

from mcp.types import BlobResourceContents, EmbeddedResource, TextContent
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent(name="TaskWriterAgent")

@fast.agent(
    name="task_assignment_generator",
    instruction="""
    You are a highly skilled person familiar with the AGILE world. 
    You will be going through an existing project plan under files/task_writer.md
    You have access to the filesystem tool to read the document.

    Instructions:
    1. Read the project plan carefully and identify the tasks and subtasks.
    2. For each task and sub-task create a new markdown file in the files/tasks folder.
    3. Ensure that the tasks are clear, actionable, and well-defined.
    4. Use markdown formatting for the output.
    5. Ensure that tasks have clear boundaries and are not too vague or overlap with eachother.
    6. Each task must be idependetly completelable by a single person.
    7. For each task list the following sections description, acceptance criteria, dependencies, priority, estimated time, skills needed.
    8. Give each task a unique uuid which you generate and use the same name as the file name.
    """,
    servers=["filesystem"],
)
@fast.agent(name="task_assignment_evaluator")
@fast.evaluator_optimizer(
    generator="task_assignment_generator",
    evaluator="task_assignment_evaluator",
    max_refinements=5,
    min_rating="EXCELLENT",
    name="task_assignment_enhanced_generator",
)
@fast.agent(
    name="task_assignment_output",
    instruction="""
    You will write each task to a file in the files/tasks folder using the filesystem tool without any modifications.
    Instructions:
    1. Read the output of the generator agent.
    2. For each task, create a new markdown file in the files/tasks folder.
    3. Ensure that the task is clear, actionable, and well-defined.
    4. Use markdown formatting for the output. 
    5. Commit metadata about each task to the memory.
    """,
    servers=["filesystem", "memory"],
)
async def task_writer():
    async with fast.run() as agent:
        intent = f"""
        You will go through all the files in the files/ folder using the filesystem tool to come up with a detailed task list.
        """
        result = await agent.task_assignment_enhanced_generator(intent)

        await agent.task_assignment_output(result)

if __name__ == "__main__":
    asyncio.run(
        task_writer()
    )