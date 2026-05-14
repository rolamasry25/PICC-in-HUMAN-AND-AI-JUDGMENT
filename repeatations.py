import pandas as pd

runs = pd.read_csv("runs.csv")

dups = runs[runs.duplicated("run_id", keep=False)]
print(dups.sort_values("run_id"))


