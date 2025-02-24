# Summarize, retrievE, answeR (SUMMER)

This directory contains the prompts and scripts required to reproduce SUMMER, as
well as the LLM baselines.

The two files `run_llama8b.py` and `run_llama70b.py` provide examples of running
inference on Llama3 8B and 70B using the [LMDeploy](https://github.com/InternLM/lmdeploy) framework.
Since the only code requirement is `lmdeploy`, we recommend installing this package
in a clean environment following their official instructions.

Templates for SUMMER and our LLM ablations are provided at:
- SUMMER final QA prompts `prompts/summer_qa.py`
- SUMMER summarization prompts `prompts/summarize.py`
- SUMMER gene set enrichment prompts `prompts/enrich.py`
- LLM (No CoT) `prompts/llm-no_cot.py`
- LLM (No Retrieval) `prompts/llm-no_retrieve.py`

Other relevant files:
- retrieving relevant experimental outcomes based on knowledge graphs `prompts/retrieve.py`

Example prompts and outputs are provided in `prompts/sample.json` and
`outputs/sample.json`. The format is a simple Python list of strings, dumped
into JSON.

Note that you must first [obtain access to
Llama3](https://huggingface.co/docs/transformers/main/en/model_doc/llama3)
before you will be able to
download their model weights. Once you do, you should set your environment
variables as follows, to ensure that you are authenticated each time.

```
export HF_TOKEN=your_token
export HF_HOME=path_to_your_cache
```

