import asyncio

from mcp.types import BlobResourceContents, EmbeddedResource, TextContent
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent(name="TaskManagementAgent")

@fast.agent(
    name="task_manager",
    instruction="""
    You can find the tasks in the files/tasks folder using the filesystem tool.
    A task management agent that can create, update, assign and delete tasks using the memory tool.
    Whenever you make a change you check if the person is right for the job and if they will have bandwidth etc.
    If the customer asks to generically assign a task to someone, you will use the memory tool to find out who is the best person to assign each task to.
    Save task assignments in memory.
    """,
    servers=["memory", "filesystem"],
)
async def task_management():
    async with fast.run() as agent:
        await agent()

if __name__ == "__main__":
    asyncio.run(
        task_management()
    )