# llm-morality

We introduce an evaluation dataset grounded in Moral Foundations Theory, which conceptualizes human morality through six core foundations. We propose a novel evaluation method that captures the full spectrum of LLMs' revealed moral preferences by answering a range of real-world moral dilemmas. Our findings reveal that state-of-the-art models have remarkably similar value preferences and demonstrate a lack of consistency.


### Dataset generation and annotation

To run dataset generation we first need to obtain API-keys for the models we evaluate. 
We run the evaluations on state-of-the-art models: GPT-3.5, GPT-4, GPT-4o, Claude-2, Claude-3-Sonnet, Claude-3.5-Sonnet, Llama-3-70b, Llama-3.1-405b, and Gemini-1.5-Flash.
The API keys can be set in file __functions.py__ .

To generate a single Moral Foundations Theory moral dilemma example, 
run the file __generate_mft_dataset.py__, where the function
__generate_single_mft_scenario__ will generate one example of a moral dilemma.
To generate a full dataset, we run __run_dataset_generation__ function which generates and performs checks on each generated example.

### Running model evaluations

The final evaluations dataset can be accessed in the final-data folder. To run evaluations for a model, 
go to __evaluate_models.py__ file and run the following specifying which model to evaluate and
type of preference (single, pair, triple or total preference) to evaluate it on.

```
file = "final-data/final_data.csv"
model = "llama3.1-405b" # other available models: "gpt-4o", "claude-2", "claude-3", "claude-3.5"
outfile = f"total_preferences_{model}"

eval = Evaluations(eval_models=[model])
eval.evals(input_filename=file, outfile=outfile, tp=True)
```

We include the final evaluation results of the models in file __llms_results.py__
