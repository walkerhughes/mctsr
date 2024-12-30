import re
from openai import OpenAI
from mctsr.settings.constants import OPENAI_MODEL
from mctsr.utils.prompts import ANSWER_CRITIQUE_PROMPT
from mctsr.utils.prompts import DRAFT_ANSWER_CRITIQUE_PROMPT
from mctsr.utils.prompts import IMPROVED_ANSWER_PROMPT


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
    prompt = DRAFT_ANSWER_CRITIQUE_PROMPT.format(question=question, draft_answer=draft_answer)
    return chat_completion_request_openai(client=client, model=model, prompt=prompt)


def get_improved_answer(client: OpenAI, model: str = OPENAI_MODEL, question="", draft_answer="", critique=""):
    prompt = IMPROVED_ANSWER_PROMPT.format(question=question, draft_answer=draft_answer, critique=critique)
    return chat_completion_request_openai(client=client, model=model, prompt=prompt)


def get_answer_rating(client: OpenAI, model: str = OPENAI_MODEL, question="", draft_answer=""):
    prompt = ANSWER_CRITIQUE_PROMPT.format(question=question, draft_answer=draft_answer)
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
