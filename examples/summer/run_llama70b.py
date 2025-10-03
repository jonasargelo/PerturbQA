"""
Script to run Llama 3-70B over 4 GPUs

Requirements: You *must* be authenticated to huggingface + have permission to access Llama 3

Please see: https://huggingface.co/meta-llama/Meta-Llama-3-70B

Sample input and output at inputs/sample.json, outputs/sample.json
"""

import os
import json
from datetime import datetime

from lmdeploy import pipeline, GenerationConfig, TurbomindEngineConfig


batch_size = 128

engine_config = TurbomindEngineConfig(
    tp=4,
    max_batch_size=batch_size,
    quant_policy=8
)
pipe = pipeline(
    "meta-llama/Meta-Llama-3-70B",
    backend_config=engine_config
)

gen_config = GenerationConfig(top_p=0.9,
                              temperature=0.6,
                              max_new_tokens=2048)

paths = [
    "inputs/diff_exp/AARS2_AAK1_example.json",
]

for fp_prompts in paths:
    with open(fp_prompts) as f:
        prompts = json.load(f)

    save_batch_size = 1024
    prompts_batched = [prompts[i:i+batch_size] for i in range(0, len(prompts), batch_size)]
    outputs = []
    output_paths = []
    total = 0
    idx = 0
    for batch in prompts_batched:
        outputs.extend([x.text for x in pipe(batch, gen_config=gen_config)])
        total += 1
        if len(outputs) >= save_batch_size:
            print(f"{datetime.now().strftime('%H:%M:%S')} {total*batch_size} / {len(prompts)}")
            fp_out = fp_prompts.replace(".json", f"-{idx}.json")
            fp_out = fp_out.replace("inputs/", "outputs/")
            with open(fp_out, "w+") as f:
                json.dump(outputs, f)
            output_paths.append(fp_out)
            outputs = []
            idx += 1

    fp_out = fp_prompts.replace(".json", f"-{idx}.json")
    fp_out = fp_out.replace("inputs/", "outputs/")
    with open(fp_out, "w+") as f:
        json.dump(outputs, f)
    output_paths.append(fp_out)

    all_outputs = []
    for fp_out in output_paths:
        with open(fp_out) as f:
            all_outputs.extend(json.load(f))

    fp_out = os.path.join("outputs/diff_exp", "llama-3-70b.json")
    with open(fp_out, "w+") as f:
        json.dump(all_outputs, f)

    for fp_out in output_paths:
        os.system(f"rm {fp_out}")

