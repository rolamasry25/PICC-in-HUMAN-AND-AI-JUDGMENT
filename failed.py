import pandas as pd

runs = pd.read_csv("runs.csv")

# runs that contain either failed_catch or too_many_fast_rts
def is_failed(flags):
    if pd.isna(flags):
        return False
    return ("failed_catch" in flags) or ("too_many_fast_rts" in flags)

runs["failed"] = runs["qualityFlags"].apply(is_failed)

total = len(runs)
failed = runs["failed"].sum()
clean = total - failed

print("Total runs:", total)
print("Failed runs:", failed)
print("Clean runs:", clean)
