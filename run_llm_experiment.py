#run_llm_experiment
import csv
import uuid
from openai import OpenAI

# ---------------------------
# CONFIG
# ---------------------------

INPUT_SEQUENCE = "stable_sequence.csv"   # change to decreasing_sequence.csv when needed
OUTPUT_FILE = "results.csv"
MODEL = "gpt-5"

PROMPT = """You will evaluate a sequence of research proposals.

For each proposal, decide whether the study should be allowed to be conducted.

Output exactly one word:
Approve
Reject

Do not output anything else.
Do not explain your answer.
Do not add punctuation.
Use the same decision standard throughout the sequence.
"""

# ---------------------------
# HELPERS
# ---------------------------

def normalize_response(text):
    if not text:
        return None

    t = text.strip().lower()

    if t == "approve":
        return 0
    if t == "reject":
        return 1

    return None


def is_catch_correct(text, response_binary):
    text = text.lower()

    if "respond with reject" in text:
        return int(response_binary == 1) if response_binary is not None else 0

    if "respond with approve" in text:
        return int(response_binary == 0) if response_binary is not None else 0

    return None


def ensure_output_file():
    try:
        with open(OUTPUT_FILE, "x", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "run_id",
                "model",
                "condition",
                "trial",
                "block",
                "prevalence",
                "item_id",
                "category",
                "is_catch",
                "text",
                "raw_response",
                "binary_response",
                "catch_correct",
                "notes"
            ])
    except FileExistsError:
        pass


# ---------------------------
# MAIN
# ---------------------------

def main():
    client = OpenAI()
    run_id = f"run_{uuid.uuid4().hex[:6]}"

    condition = "stable" if "stable" in INPUT_SEQUENCE else "decreasing"

    ensure_output_file()

    # conversation history (IMPORTANT for PICC)
    history = [
        {"role": "developer", "content": PROMPT}
    ]

    with open(INPUT_SEQUENCE, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    for row in reader:
        trial = row["trial"]
        block = row["block"]
        prevalence = row["prevalence"]
        item_id = row["item_id"]
        category = row["category"]
        is_catch = row["is_catch"] == "1"
        text = row["text"]

        # send next proposal
        history.append({
            "role": "user",
            "content": f"Proposal: {text}"
        })

        response = client.responses.create(
            model=MODEL,
            input=history
        )

        raw = (response.output_text or "").strip()
        binary = normalize_response(raw)

        catch_correct = None
        notes = ""

        if is_catch:
            catch_correct = is_catch_correct(text, binary)

        if binary is None:
            notes = "invalid_output"

        # add assistant reply to history (CRITICAL)
        history.append({
            "role": "assistant",
            "content": raw
        })

        # save row
        with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                run_id,
                MODEL,
                condition,
                trial,
                block,
                prevalence,
                item_id,
                category,
                int(is_catch),
                text,
                raw,
                binary,
                catch_correct,
                notes
            ])

        print(f"Trial {trial}: {raw}")

    print("\nDONE")
    print("Run ID:", run_id)


if __name__ == "__main__":
    main()


