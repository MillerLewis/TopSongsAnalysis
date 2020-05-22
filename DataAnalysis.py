import pandas as pd
import properties
import numpy as np

def get_max_num_columns(file_name, delimiter=","):
    max_cols = 0
    row = 0
    with open(file_name, 'r') as f:
        for line in f.readlines():
            split_line = line.split(delimiter)
            col_count = len(split_line)
            max_cols = col_count if col_count > max_cols else max_cols
            row += 1
    return max_cols


column_names = ["date"] + ["artist{}".format(i) for i in range(get_max_num_columns(properties.FILE_NAME) - 1)]
artists_df = pd.read_csv(properties.FILE_NAME, sep=',', names=column_names, index_col=0)
print(artists_df[artists_df.iloc[:, -1].isna() == False])
# print(artists_df[artists_df.isna()[:, -1] == True])
