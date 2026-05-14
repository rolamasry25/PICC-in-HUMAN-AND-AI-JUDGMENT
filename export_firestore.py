import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

credentials.Certificate("firebase_key.json") #privet info
firebase_admin.initialize_app(cred)

db = firestore.client()

runs_ref = db.collection("runs")
docs = runs_ref.stream()

runs_rows = []
trials_rows = []

for d in docs:
    run = d.to_dict() or {}
    run_id = run.get("run_id", d.id)

    # ---- run level ----
    runs_rows.append({
        "run_id": run_id,
        "condition": run.get("condition"),
        "response_format": run.get("response_format"),
        "duration_ms": run.get("duration_ms"),
        "qualityFlags": ",".join(run.get("qualityFlags", []))
    })

    # ---- trial level ----
    for t in run.get("trials", []):
        row = dict(t)
        row["run_id"] = run_id
        trials_rows.append(row)

runs_df = pd.DataFrame(runs_rows)
trials_df = pd.DataFrame(trials_rows)

runs_df.to_csv("runs.csv", index=False, encoding="utf-8-sig")
trials_df.to_csv("trials.csv", index=False, encoding="utf-8-sig")

print("Export finished.")
print("Created files: runs.csv and trials.csv")
