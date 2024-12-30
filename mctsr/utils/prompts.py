

DRAFT_ANSWER_CRITIQUE_PROMPT = """

    #### QUESTION & DRAFT ANSWER ####

    Question: {question}

    Draft Answer: {draft_answer}

    #### INSTRUCTIONS ####

    Critique the Draft Answer to the Question. Carefully assess if the Draft Answer is correct or not and why.
    Consider multiple ways of verifying if the Draft Answer is correct.

    DO: Point out EVERY flaw and hold the draft answer to a very high standard.
    DO: Provide specific recommendations to improve the answer.
    DO: Think step by step.

    DO NOT provide a revised answer.

"""

IMPROVED_ANSWER_PROMPT = """

    #### QUESTION, DRAFT ANSWER & CRITIQUE ####

    Question: {question}

    Draft Answer: {draft_answer}

    Critique: {critique}

    #### INSTRUCTIONS ####
    
    Improve the draft answer based on the critique following this format:
    Reasoning Process: <step-by-step reasoning process>.
    Verification: <verification of the facts>.
    Final Answer: <the improved and verified answer>.

"""

ANSWER_CRITIQUE_PROMPT = """

    #### QUESTION & DRAFT ANSWER ####
    
    Question: {question}

    Draft Answer: {draft_answer}

    #### INSTRUCTIONS ####

    As an expert on this topic, please provide a detailed critique. Provide ONLY a critique of
    the answer to the question, not a suggested answer. Rate the answer on a scale of 0 to 100.

    The response should be in the following format:
    Critique: <detailed critique>
    Rating: <0 to 100 rating>

"""
