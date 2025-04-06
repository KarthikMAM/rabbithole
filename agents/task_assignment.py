import asyncio

from mcp.types import BlobResourceContents, EmbeddedResource, TextContent
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent(name="TaskAssignmentAgent")

@fast.agent(
    name="task_assignment_generator",
    instruction="""
    You are an expert in project management and task assignment.
    You will be going through an list of tasks under files/tasks and assigning them to the best person in the team.
    You will be using the filesystem tool to read the tasks and the memory tool to find out who is the best person to assign each task to.
    You will be using the memory tool to find out who is the best person to assign each task to and also to check if the person is free at the moment.
    """,
    servers=["filesystem", "memory"],
)
@fast.agent(name="task_assignment_evaluator")
@fast.evaluator_optimizer(
    generator="task_assignment_generator",
    evaluator="task_assignment_evaluator",
    max_refinements=2,
    min_rating="FAIR",
    name="task_assignment_enhanced_generator",
)
@fast.agent(
    name="task_assignment_output",
    instruction="""
    You will write the output of the accepted assignments to a file named `task_assignments.md` using the filesystem tool without any modifications.
    """,
    servers=["filesystem"],
)
async def task_assignment():
    async with fast.run() as agent:
        intent = f"""
        You will go through all the files in the files/tasks folder using the filesystem tool and then use the memory tool to find out who is the best person to assign each task to.
        """
        result = await agent.task_assignment_enhanced_generator(intent)

        await agent.task_assignment_output(result)

if __name__ == "__main__":
    asyncio.run(
        task_assignment()
    )