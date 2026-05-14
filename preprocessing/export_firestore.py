import json
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('path/to/serviceAccountKey.json')
db = firestore.client()

def export_firestore_data(collection_name: str, output_file: str):
    """
    Export Firestore collection to JSON file.
    """
    docs = db.collection(collection_name).stream()
    data = []
    
    for doc in docs:
        data.append(doc.to_dict())
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Exported {len(data)} documents to {output_file}")

if __name__ == "__main__":
    export_firestore_data('responses', 'firestore_export.json')
