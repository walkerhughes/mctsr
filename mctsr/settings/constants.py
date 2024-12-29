import os
from openai import OpenAI

RANDOM_SEED = 17
MAX_CHILDREN = 3

LLAMA_MODEL = "llama3-8b-8192"
OPENAI_MODEL = "gpt-4o-mini-2024-07-18"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_CLIENT = OpenAI()

SEED_ANSWERS = [
    "I don't know the answer",
    "I'm not sure",
    "I can't say on that one"
]
