#!/bin/sh

# main script for training

######### training params
CUDA=0
NUM_GPU=1

# I can train this on CPU HAHA
CUDA=-1
NUM_GPU=0

######### data params

# NOTE: name of YAML file and run save folder
# see ./config for more options

#TAG="mlp"
#for DATASET in hepg2 jurkat
#do
#    DATA_FILE="data/20240712-nadig_${DATASET}.csv"
#    SAVE_PATH="weights_${DATASET}"
#    RUN_NAME="${DATASET}_${TAG}"
#    CONFIG="config/${TAG}.yaml"
#    for LAYERS in 0 1 2 4
#    do
#        for DIM in 256 512 1024
#        do
#            for FFN in 1024 2048
#            do
#                echo $DIM $FFN $LAYERS $CONFIG
#                python train.py \
#                    --data_file $DATA_FILE \
#                    --config_file $CONFIG \
#                    --num_layers $LAYERS \
#                    --embed_dim $DIM \
#                    --ffn_embed_dim $FFN \
#                    --save_path $SAVE_PATH \
#                    --gpu $CUDA \
#                    --num_gpu $NUM_GPU \
#                    --run_name $RUN_NAME
#            done
#        done
#    done
#
#done

TAG="mlp_pathway"
for DATASET in k562_gw_path
do
    DATA_FILE="data/20240717-replogle_${DATASET}.csv"
    SAVE_PATH="weights_${DATASET}"
    #RUN_NAME="${DATASET}_${TAG}"
    RUN_NAME="${DATASET}_mlp"
    CONFIG="config/${TAG}.yaml"
    for LAYERS in 0 1 2 4
    do
        for DIM in 256 512 1024
        do
            for FFN in 1024 2048
            do
                echo $DIM $FFN $LAYERS $CONFIG
                python train.py \
                    --data_file $DATA_FILE \
                    --config_file $CONFIG \
                    --num_layers $LAYERS \
                    --embed_dim $DIM \
                    --ffn_embed_dim $FFN \
                    --save_path $SAVE_PATH \
                    --gpu $CUDA \
                    --num_gpu $NUM_GPU \
                    --run_name $RUN_NAME
            done
        done
    done
done

