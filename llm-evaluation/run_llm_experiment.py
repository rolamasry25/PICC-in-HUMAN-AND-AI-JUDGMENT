import anthropic
import json
from typing import Optional

# Initialize the Anthropic client
client = anthropic.Anthropic()

def load_items(filepath: str) -> list[dict]:
    """Load experimental items from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def classify_item(text: str, model: str = "claude-3-5-sonnet-20241022") -> dict:
    """
    Classify a single item using Claude API.
    Returns the classification and confidence.
    """
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Classify the following experimental procedure as either "ethical" or "unethical". 
                
Procedure: {text}

Respond with a JSON object containing:
- "classification": "ethical" or "unethical"
- "confidence": a number between 0 and 1
- "reasoning": brief explanation

Return ONLY valid JSON, no other text."""
            }
        ]
    )
    
    try:
        result = json.loads(message.content[0].text)
        return result
    except json.JSONDecodeError:
        return {
            "classification": "ambiguous",
            "confidence": 0.0,
            "reasoning": "Could not parse response"
        }

def run_experiment(input_file: str, output_file: str, sample_size: Optional[int] = None):
    """
    Run the LLM evaluation experiment on all items.
    """
    items = load_items(input_file)
    
    if sample_size:
        items = items[:sample_size]
    
    results = []
    
    for idx, item in enumerate(items, 1):
        print(f"Processing item {idx}/{len(items)}...")
        classification = classify_item(item['text'])
        
        result = {
            "id": item['id'],
            "text": item['text'],
            "human_category": item['category'],
            "llm_classification": classification['classification'],
            "confidence": classification['confidence'],
            "reasoning": classification['reasoning']
        }
        results.append(result)
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    run_experiment(
        input_file="experiment/study7_items.json",
        output_file="llm_classifications.json"
    )
