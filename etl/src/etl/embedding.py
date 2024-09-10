import pysolr
import json
import os
from search_logging import get_logger
from sentence_transformers import SentenceTransformer

solr_url = data = os.getenv('SOLR_URL', 'http://solr:8983/solr/demo')
solr = pysolr.Solr(solr_url)

logger = get_logger(__name__)

model_name='bert-base-nli-mean-tokens'
model=SentenceTransformer(model_name)


def updateSchema () : 

   
    try: 

        field_type_payload = {
            "add-field-type": {
                "name": "knn_vector",
                "class": "solr.DenseVectorField",
                'vectorDimension' : "768",
                'similarityFunction' : "cosine",
                'knnAlgorithm': "hnsw",
                'hnswMaxConnections': "10",
                'hnswBeamWidth':"40"
            }
        }

        solr._send_request('POST', '/schema', json.dumps(field_type_payload))
    
        field_payload = {
            "add-field": {
                "name": "bert_vector",
                "type": "knn_vector",
                "stored": True,
                "indexed": True
            }
        }

    
        solr._send_request('POST', '/schema', json.dumps(field_payload))

    except Exception as error:
        logger.warning("field is already added") 

def compute_embeddig(document): 
    try:
        title = document["title"]
        content = document["content"]
        url = document['url']
        
        sentences = content.split('. ')  
        embedding = model.encode(sentences)
        logger.info(f"Indexing url: {url}")
        solr.add({'url': url, 'title': title, 'bert_vector':{'set':[float(w) for w in embedding[0]]}})

        # Commit the changes
        solr.commit()

        return 1

    except Exception as error:
      logger.error(f"error occured when embedding document {document}: {error}")
      return 0


updateSchema()



