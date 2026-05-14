import json

# Count repetitions in data
def count_repetitions(data: list) -> dict:
    """Count how many times each item appears."""
    counts = {}
    for item in data:
        item_id = item.get('id')
        counts[item_id] = counts.get(item_id, 0) + 1
    return counts

if __name__ == "__main__":
    # Example usage
    with open('responses.json', 'r') as f:
        data = json.load(f)
    
    repetitions = count_repetitions(data)
    print(repetitions)
