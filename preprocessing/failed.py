import json

# Log failed items
failed_items = []

def log_failed_item(item_id: int, reason: str):
    """Log a failed item processing."""
    failed_items.append({
        "id": item_id,
        "reason": reason
    })

def save_failed_items(output_file: str):
    """Save failed items to file."""
    with open(output_file, 'w') as f:
        json.dump(failed_items, f, indent=2)
