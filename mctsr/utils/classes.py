import math
import random
import numpy as np
from openai import OpenAI

from mctsr.settings.constants import RANDOM_SEED
from mctsr.settings.constants import MAX_CHILDREN
from mctsr.settings.constants import SEED_ANSWERS
from mctsr.settings.constants import OPENAI_MODEL
from mctsr.utils.funcs import get_answer_rating
from mctsr.utils.funcs import get_draft_answer_critique
from mctsr.utils.funcs import get_improved_answer

np.random.seed(RANDOM_SEED)

class MCTSrNode:
    def __init__(self, question, answer, parent=None):
        self.question = question
        self.answer = answer
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0

    def add_child(self, child_node):
        self.children.append(child_node)

    def is_fully_expanded(self):
        return len(self.children) >= MAX_CHILDREN

    def most_visited_child(self):
        return max(self.children, key = lambda child: child.visits)

    def best_child(self, exploration_weight=math.sqrt(2)):
        choices_weights = []
        for child in self.children:
            if child.visits == 0:
                weight = np.inf
            else:
                weight = (
                    (child.value / child.visits) + 
                    exploration_weight 
                    * math.sqrt((2 * math.log(self.visits) / child.visits))
                )
            choices_weights.append(weight)
        return self.children[np.argmax(choices_weights)]
    

class MCTSr:
    def __init__(self, client: OpenAI, question: str, seed_answers: list, iterations: int = 2):
        self.client = client
        self.question = question
        self.seed_answers = seed_answers
        self.iterations = iterations
        self.root = MCTSrNode(question, random.choice(SEED_ANSWERS))

    def search(self):
        for i in range(self.iterations):
            print(f"Iteration {i + 1}/{self.iterations}")
            node = self.select(self.root)
            print(f"Selected Node: {node.answer}")
            if not node.is_fully_expanded():
                node = self.expand(node)
                print(f"Expanded node: {node.answer}")
            reward = self.simulate(node)
            print(f"Simulated Reward: {reward}")
            self.backpropagate(node, reward)
        print(f"Visits to most visited child: {self.root.most_visited_child().visits}")
        return self.root.most_visited_child().answer
    
    def select(self, node: MCTSrNode):
        """ 
        For a fully expanded Node, move to its best child using UCT criteria.
        """
        while node.is_fully_expanded() and node.children:
            node = node.best_child()
        return node
    
    def expand(self, node: MCTSrNode):
        for i in range(MAX_CHILDREN - len(node.children)):

            child_node = MCTSrNode(self.question, node.answer, parent=node)
            node.add_child(child_node)

            critique = get_draft_answer_critique(self.client, OPENAI_MODEL, self.question, child_node.answer)
            print(f"\n---Critique {i}---\n{critique}")

            improved_answer = get_improved_answer(self.client, OPENAI_MODEL, self.question, child_node.answer, critique)
            print(f"\n---Improved Answer {i}---\n{improved_answer}")

            child_node.answer = improved_answer
        return random.choice(node.children)
    
    def simulate(self, node: MCTSrNode):
        return get_answer_rating(self.client, OPENAI_MODEL, node.question, node.answer)
    
    def backpropagate(self, node: MCTSrNode, reward: float):
         """ 
         Backpropagates reward for a given answer through the tree structure,
         which is used to calculate UTC bounds for the best answer to the original question.
         """
         while node is not None: 
             node.visits += 1
             node.value += reward
             print(f"\nNumber of node visits: {node.visits}\n")
             print(f"\nNode Value           : {node.value}\n")
             node = node.parent
