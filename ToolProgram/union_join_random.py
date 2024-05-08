# importing necessary libraries
import pandas as pd
import random

# paths to the csv files for two databases
csv1_path = 'Database - aaa.csv'
csv2_path = 'recipe_dataset.csv'

# reading data from the csv files into pandas dataframes
df1 = pd.read_csv(csv1_path)
df2 = pd.read_csv(csv2_path)

# getting the lengths of the dataframes
len_df1, len_df2 = len(df1), len(df2)

# creating a list of indices in random order
random_order = list(range(max(len_df1, len_df2)))
random.shuffle(random_order)

# initializing an empty dataframe to store the merged data
merged_df = pd.DataFrame()

# looping through the randomly ordered indices
for index in random_order:
    # extracting a row from df1 if index is within its length, else creating an empty dataframe with df1 columns
    row_df1 = df1.iloc[[index]] if index < len_df1 else pd.DataFrame(columns=df1.columns)
    
    # extracting a row from df2 if index is within its length, else creating an empty dataframe with df2 columns
    row_df2 = df2.iloc[[index]] if index < len_df2 else pd.DataFrame(columns=df2.columns)
    
    # concatenating the rows from df1 and df2 vertically, then concatenating the result to the merged dataframe
    merged_df = pd.concat([merged_df, pd.concat([row_df1, row_df2])], axis=0)

# resetting the index of the merged dataframe and dropping the old index
merged_df.reset_index(drop=True, inplace=True)

# displaying the merged dataframe
print(merged_df)

# writing the merged dataframe to a csv file without index and using utf-8 encoding with a bom
merged_df.to_csv('merged_file.csv', index=False, encoding='utf-8_sig')