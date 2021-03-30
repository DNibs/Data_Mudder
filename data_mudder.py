# This script takes a clean dataset and "muddies" it
# It will randomly remove ~10% of the data
# It then targets one attribute and randomly removes ~60% of the data
# It then splits the data into two sets and slightly alters the attribute names on the second set
import pandas as pd
import random
import numpy as np
import string


# Global variables
PERCENT_DROPPED_VALUES = 0.02


if __name__ == '__main__':
    print('It\'s about to get disguisting!')

    # File IO
    db_filename = input('Please enter the filename you want to make dirty: \n')
    try:
        df = pd.read_csv(db_filename)
        print('Read CSV file')
    except:
        print('Not read as csv file')
        try:
            df = pd.read_excel(db_filename)
            print('Read excel file')
        except:

            print('Not read as excel file - possibly because pandas cannot read xlsx files anymore')
            print('Unable to read file.')

    # Randomly delete about 10% of the data across every attribute
    for col in df.columns:
        for row in range(0, len(df.index)):
            if random.random() < PERCENT_DROPPED_VALUES:
                df.loc[row, col] = np.nan

    # Randomly choose one attribute and delete about 60% of all values in that attribute
    col_for_deletion = random.choice(df.columns)
    for row in range(0, len(df.index)):
        if random.random() < 0.6:
            df.loc[row, col_for_deletion] = np.nan

    # Split dataset into two dataframes
    df1 = df.sample(frac=0.5)
    df2 = df.drop(df1.index)

    # Slightly mess up column names in 2nd dataframe
    for col in df2.columns:
        df2.rename(columns={col: random.choice(string.ascii_letters)+col+random.choice(string.ascii_letters)},
                   inplace=True)

    # Write to output csv files
    df1.to_csv('dirty1_'+db_filename, index=False)
    df2.to_csv('dirty2_'+db_filename, index=False)

    print('Complete! Enjoy your dirty data!')
