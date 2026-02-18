import pandas as pd



def preprocess(df, region_df):
    #Filtering only Summer Olympics Records
    df = df[df['Season'] == 'Summer']
    #Adding 'region' col to main df: LEFT JOIN
    df = pd.merge(df, region_df, how='left', on='NOC')
    #Removing duplicates
    df.drop_duplicates(inplace=True)
    #Hot one encoding 'medal' col and merging with og df
    medals = pd.get_dummies(df['Medal'], dtype=int)
    df = pd.concat([df, medals], axis=1)
    return df