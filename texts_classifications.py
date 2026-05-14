import pandas as pd

pd.read_csv("study7.csv")

df = df.drop_duplicates(subset='item').reset_index(drop=True)

def classify(mean):
    if mean <= 4:
        return "unethical"
    elif mean <= 6:
        return "ambiguous"
    else:
        return "ethical"

df['category'] = df['norm_mean'].apply(classify)

# CHECK COUNTS
print(df['category'].value_counts())

# SELECT 15 CONSTANT ITEMS (5 per category)
constant_set = (
    df.groupby('category', group_keys=False)
      .apply(lambda g: g.nsmallest(5, 'norm_sd'))
      .reset_index(drop=True)
)

df['tag'] = df['item'].apply(lambda x: 'constant' if x in constant_set['item'].values else None)

df.to_csv("dataset_tagged_corrected.csv", index=False)

