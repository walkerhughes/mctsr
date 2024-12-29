import re
from openai import OpenAI
from mctsr.settings.constants import OPENAI_MODEL



def chat_completion_request_openai(client: OpenAI, model: str = OPENAI_MODEL, prompt: str = ""):
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1.0,
        max_tokens=1500
    )
    if response.choices:
        return response.choices[0].message.content
    return None


def get_draft_answer_critique(client: OpenAI, model: str = OPENAI_MODEL, question = "", draft_answer = ""):
    prompt = (
        f"Question: {question}"
        f"Draft Answer: {draft_answer}"
        "Please critique the draft answer."
        "Carefully assess if the answer is correct of not and why."
        "Consider multiple ways of verifying if the answer is correct."
        "DO: Point out EVERY flaw and hold the draft answer to a very high standard."
        "DO: Provide specific recommendations to improve the answer."
        "DO: Think step by step."
        "DO NOT provide a revised answer"
    )
    return chat_completion_request_openai(client=client, model=model, prompt=prompt)


def get_improved_answer(client: OpenAI, model: str = OPENAI_MODEL, question="", draft_answer="", critique=""):
    prompt = (
        f"Question: {question}"
        f"Draft Answer: {draft_answer}"
        f"Critique: {critique}"
        "Please improve the draft answer based on the critique following this format:"
        "Reasoning Process: <step-by-ste- reasoning process>\n"
        "Verification: <verification of the facts>\n"
        "Final Answer: <the improved and verified answer>\n"
    )
    return chat_completion_request_openai(client=client, model=model, prompt=prompt)


def get_answer_rating(client: OpenAI, model: str = OPENAI_MODEL, question="", answer=""):
    prompt = (
        f"Question: {question}"
        f"Answer: {answer}"
        "As an expert on this topic, please provide a detailed critique "
        "Provide ONLY a critique, not a suggested answer."
        "Then, rate the answer on a scale of 0 to 100."
        "The response should be in the following format:"
        "Critique: <detailed critique>\n"
        "Rating: <0 to 100 rating>\n"
    )
    response = chat_completion_request_openai(client=client, model=model, prompt=prompt)

    try: 
        match = re.search(r"Rating:\s+(\d+)", response)
        if match:
            rating = int(match.group(1))
            if rating > 95:
                rating = 95.0
            rating /= 100.0
        else:
            raise ValueError("Rating not found in response.")
    except Exception as e:
        print(f"Error extracting rating: {e}")
        print(f"Rating response was: {response}")
        rating = 0.0
    return rating