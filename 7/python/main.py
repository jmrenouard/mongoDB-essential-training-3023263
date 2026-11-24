import os
from pymongo import MongoClient
from dotenv import load_dotenv


def run_sample():
    """Load credentials from environment/.env, insert a sample doc, and query it back."""
    load_dotenv()
    client = MongoClient(
        'mongodb://localhost:27017/admin?retryWrites=true&w=majority',
        username=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

    db = client['sample_data']
    collection = db['testpython']

    doc = {"author": "Naomi", "message": "hello world!"}

    doc_id = collection.insert_one(doc).inserted_id
    print(doc_id)

    found = collection.find_one()
    print(found)
    return doc_id, found


if __name__ == "__main__":
    run_sample()
