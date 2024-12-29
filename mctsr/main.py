import argparse
from openai import OpenAI
from dotenv import load_dotenv

from mctsr.settings.constants import OPENAI_CLIENT
from mctsr.settings.constants import SEED_ANSWERS
from mctsr.utils.classes import MCTSr

load_dotenv()

def main(api_client: OpenAI = OPENAI_CLIENT, question: str = "what is the capital of France"):
    mcts = MCTSr(
        client=api_client,
        question=question,
        seed_answers=SEED_ANSWERS
    )
    best_answer = mcts.search()
    return best_answer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse arguments for MCTSr")
    parser.add_argument(
        "--question", 
        type=str, 
        help="question to be answered by LLM via MCTSr", 
        required=True
    )
    args = parser.parse_args()

    main(question=args.question)