import asyncio

from mcp_agent.core.fastagent import FastAgent

fast = FastAgent(name="MemoryAgent")

@fast.agent(
    name="memory",
    instruction="""
    Follow these steps for each interaction:

        1. User Identification:
        - You should assume that you are interacting with default_user
        - If you have not identified default_user, proactively try to do so.

        2. Memory Retrieval:
        - Always begin your chat by saying only "Remembering..." and retrieve all relevant information from your knowledge graph
        - Always refer to your knowledge graph as your "memory"

        3. Memory
        - While conversing with the user, be attentive to any new information that falls into these categories:
            a) Basic Identity (age, gender, location, job title, education level, etc.)
            b) Behaviors (interests, habits, etc.)
            c) Preferences (communication style, preferred language, etc.)
            d) Goals (goals, targets, aspirations, etc.)
            e) Relationships (personal and professional relationships up to 3 degrees of separation)

        4. Memory Update:
        - If any new information was gathered during the interaction, update your memory as follows:
            a) Create entities for recurring organizations, people, and significant events
            b) Connect them to the current entities using relations
            b) Store facts about them as observations

    """,
    servers=["memory"],
)
async def memory():
    async with fast.run() as agent:
        # Step 1: User Identification
        await agent(f"""
        Remember that there is a team of 6 people: Alice, Bob, Charlie, David, Eve, and Frank.
                    
        Alice is a backend engineer who has consistenly proved her skills.
        Bob is a frontend engineer who is also a great designer.
        Charlie is also a frontend engineer but is not free at the moment.
        David is a data engineer.
        Eve is a product manager.
        Frank is a data scientist.
        """)

if __name__ == "__main__":
    asyncio.run(memory())