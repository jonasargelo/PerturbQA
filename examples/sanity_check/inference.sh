#!/bin/sh

# main script for training

######### training params
CUDA=-1
NUM_GPU=0

######### data params

# NOTE: name of YAML file and run save folder
# see ./config for more options
TAG="mlp"
#TAG="kg_tf"
#TAG="kg_gnn"
#TAG="kg_tf_path"
CONFIG="config/${TAG}.yaml"


python inference.py \
    --config_file $CONFIG \
    --gpu $CUDA \
    --num_gpu $NUM_GPU \
    --results_file "results/results_tf.pkl" \
    --checkpoint_path $CKPT_MLP_ASY \
    --num_transformer_layers 1 \
    --embed_dim 1024 \
    --ffn_embed_dim 1024 \
    ## GNN params
    #--checkpoint_path $CKPT_GNN \
    #--num_transformer_layers 4 \
    #--embed_dim 512 \
    #--ffn_embed_dim 1024 \
    #--num_neighbors 20 \
    ## TF params
    #--checkpoint_path $CKPT_TF \
    #--num_transformer_layers 4 \
    #--embed_dim 256 \
    #--ffn_embed_dim 1024 \
    #--num_neighbors 10 \
    ## MLP params
    ## PATH params
    #--checkpoint_path $CKPT_PATH_MAX \
    #--num_transformer_layers 4 \
    #--embed_dim 256 \
    #--ffn_embed_dim 1024 \
    #--path_cache "data/paths.pkl" \


