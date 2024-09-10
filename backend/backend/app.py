import os
from backend.document import Document
import pysolr
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from flask_cors import CORS


solr_url = data = os.getenv('SOLR_URL', 'http://solr:8983/solr/demo')
solr = pysolr.Solr(solr_url)

app = Flask(__name__)
CORS(app)
model = SentenceTransformer('bert-base-nli-mean-tokens')

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'message': 'Not found', 'error': error}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error', 'error': error}), 500

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    embedding = model.encode([query])
    solr_response=solr.search(fl=['id','title','score'],
                  q="{!knn f=bert_vector topK=10}"+str([float(w) for w in embedding[0]]),
                  rows = 30)
    

    documents = []
    for document in solr_response:
        doc = Document(
            url=document.get('url'),
            title=document.get('title'),
            score=document.get('score')
        )
        documents.append(doc.to_dict())


    return jsonify({"documents": documents})

@app.route('/health', methods=['GET'])
def health():
    name = request.args.get('name')
    return f"Hello {name}"

if __name__ == '__main__':
    app.run(debug=True)
