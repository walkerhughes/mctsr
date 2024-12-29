# Monte Carlo Tree Self-Refine Implementation
Monte Carlo Tree Self-Refine implementation for enhanced LLM accuracy in Q&amp;A tasks based on [MCTSr](https://arxiv.org/pdf/2406.07394) paper, Trelis Research implementation, &amp; TextGrad.


### Environment Set-up
This project uses python 3.10.9. You'll need `poetry` installed for dependency and package management and should create a virtual environment. The below commands will create your environment and install the required dependencies.

1. `$ pyenv virtualenv 3.10.9 mctsr`
2. `$ pyenv shell mctsr`
3. `$ poetry install`


### Answering Questions via Monte Carlo Tree Self-Refine
To run the `main.py` script from the command line to answer a question with the `MCTSr` class, use the below command:
```bash
╰─$ python mctsr/main.py --question "what is the capital of france"
```
Output will appear in the terminal:
```bash
Iteration 1/2
Selected Node: I'm not sure

---Critique 0---
The draft answer, "I'm not sure," has several significant flaws that undermine its effectiveness and quality.

1. **Accuracy**: The capital of France is well-known and easily verifiable information. The answer fails to provide the correct information, which can be immediately identified by anyone with basic knowledge...

...

Number of node visits: 1
Node Value           : 0.85
Number of node visits: 1
Node Value           : 0.85
Number of node visits: 2
Node Value           : 1.7

...

**Final Answer:** The capital of France is Paris. Renowned for its rich history and immense cultural influence, Paris is home to iconic landmarks such as the Eiffel Tower and the Louvre Museum. This vibrant city is a global center for art, fashion, and gastronomy, drawing millions of visitors each year.
```
