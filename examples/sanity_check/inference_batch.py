"""
Wrapper around inference script
"""

import os
import sys
import yaml


def main():
    # config file with model parameters
    if len(sys.argv) > 1:
        fp_configs = sys.argv[1]
    else:
        fp_configs = "data/inference.yaml"
    with open(fp_configs) as f:
        configs = yaml.safe_load(f)
    # pass

    for config in configs:
        if os.path.exists(config["results_file"]):
            continue
        cmd = f"python inference.py --gpu -1 --num_gpu 0 {chain_commands(config)}"
        print(cmd)
        os.system(cmd)


def chain_commands(config):
    args = []
    for k, v in config.items():
        args.append(f"--{k} {v}")
    return " ".join(args)


if __name__ == "__main__":
    main()

