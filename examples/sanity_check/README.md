# Sanity check

For formatted data files, please extract `baselines_data.zip` from our Figshare to `baselines/sanity_check/data`

You may replicate our conda environment using our `environment.yml`.
```
conda env create -f environment.yml
```

However, sometimes `pytorch_geometric` may result in installation errors, so you
can try installing manually as well.
Main dependences are
- `numpy`
- `torch`
- `wandb`
- `pytorch_lightning`
- `pytorch_geometric`.

This code was tested using PyTorch 2.3.1 and CUDA 12.1.

