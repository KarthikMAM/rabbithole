from mcp_agent import FastAgent

fast = FastAgent(name="ImplementationDetailsAgent")

@fast.agent(
    name="generator",
    instruction="""
    You are a highly skilled requirements analysis agent. 
    Your primary responsibility is to engage with the user to deeply understand their intent.
    We are not figuring out the solution yet, but rather clarifying the requirements.
    This is a critical step in the process of gathering requirements and we are solely focused on just understanding customer intent. 
    Through thoughtful and targeted questions, you will gather the necessary details to help other agents formulate precise and actionable plan.
    Be thorough, clear, and ensure no critical information is overlooked.
    Do not provide any solutions or suggestions at this stage. This is an absolute requirement.
    """,
)
@fast.agent(
    name="evaluator",
    instruction="""
    Ensure the questions are clear, concise, and relevant probe the user's intent.
    They should be specific enough to elicit detailed responses, yet open-ended to allow for elaboration.
    Avoid leading questions and ensure that the questions are unbiased.
    The questions should be structured to cover all aspects of the customer intent.
    """,
)
@fast.evaluator_optimizer(
    generator="generator",
    evaluator="evaluator",
    max_refinements=5,
    min_rating="EXCELLENT",
    name="enhanced_generator"
)
@fast.agent(
    name="answers", 
    instruction="""
    You are a highly skilled interaction agent.
    You will be given a list of questions and you will use only those questions. Do not ask any other questions.
    Ask the user the questions one by one and wait for the user / human to answer each question.
    Validate the answer satisfies the question before moving to the next one.
    Do not answer the questions yourself. The customer must be prompted by the human tool every time to get the answer. This is absolute requirement.
    Finally you will output the list of questions and the answers as they were asked and answered in the following format to the teeth:

    # Questions and Answers
    - {question_1}: 
        - {answer_1}
    - {question_2}:
        - {answer_2}
    - {question_3}:
        - {answer_3}
    - {question_4}:
        - {answer_4}

    Instructions:
    3. Ensure that the information is clear, concise, and actionable.
    4. Ensure that the information is complete and cover all aspects of the customer intent.
    5. Write the information in a markdown file named `clarifications.md` using the filesystem tool.
    6. Do not write any other information or comments and the questions and answers must be in the format above and should not change from the original.
    """,
    human_input=True,
    use_history=True,
    model="gpt-4o"
)
@fast.agent(
    name="output",
    instruction="""
    You will write the final set of questions along with their answers and the customer intent to `clarifications.md` in the following format to the teeth:

    ```md
    # Customer Intent
    {customer_intent}

    # Clarifying Questions and Answers
    {clarifying_questions_and_answers}
    ```

    Instructions:
    1. Write the customer intent and clarifying questions and answers in the format above.
    3. Ensure that the information is clear, concise, and actionable.
    4. Ensure that the information is complete and cover all aspects of the customer intent.
    5. Write the information in a markdown file named `clarifications.md` using the filesystem tool.
    6. Do not write any other information or comments.
    """,
    servers=["filesystem"],
)
async def requirements_clarification(intent: str) -> dict:
    async with fast.run() as agent:
        questions = await agent.enhanced_generator(f"Customer Intent: {intent}")

        questions_and_answers = await agent.answers(f"Questions: {questions}")

        await agent.output(f"Intent: {intent} \n {questions_and_answers}")

        return {
            "intent": intent,
            "questions_and_answers": questions_and_answers,
        }
