# First we combine the train.json and train_others.json into one dataset
import pandas as pd
import json

if __name__ == '__main__':
    df_train = pd.read_json("../../Assets/datasets/spider_data/train_spider.json")
    df_train_others = pd.read_json("../../Assets/datasets/spider_data/train_others.json")
    df_concatenated = pd.concat([df_train, df_train_others])


    # TODO: Dataset handeln
