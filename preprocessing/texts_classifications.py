import json
from collections import Counter

def classify_texts(input_file: str, output_file: str):
    """
    Classify texts based on category patterns.
    """
    with open(input_file, 'r') as f:
        items = json.load(f)
    
    classifications = {
        'ethical': [],
        'unethical': [],
        'ambiguous': []
    }
    
    for item in items:
        category = item.get('category', 'ambiguous')
        classifications[category].append(item)
    
    # Count classifications
    counts = {k: len(v) for k, v in classifications.items()}
    
    result = {
        'counts': counts,
        'classifications': classifications
    }
    
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Classification complete: {counts}")

if __name__ == "__main__":
    classify_texts('experiment/study7_items.json', 'text_classifications.json')
