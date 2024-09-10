import extraction
import embedding
import scrapping
import util
import concurrent.futures
import time
from search_logging import get_logger
import os

logger = get_logger(__name__)

def process_pipeline(urls):
    logger.info("starting data extraction ...")
    start_time = time.time()
    documents = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(extraction.get_cleaned_content, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            doc = future.result()
            if doc:
                documents.append(doc)
     
    logger.info("data extraction took --- %s seconds ---" % (time.time() - start_time))

    logger.info("extracted %d documents " % len(documents))
    count = 0

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(embedding.compute_embeddig, document): document for document in documents}
        for future in concurrent.futures.as_completed(future_to_url):
            count += future.result()

    logger.info("embedded %d over %d" % (count, len(documents)))
            
    logger.info("end of embedding")

    logger.info("embedding took --- %s seconds ---" % (time.time() - start_time))

def init (data):
    if (data == 'TEST'):
        
        lines = util.readFromFile ("./resources/examples.txt")
        documents = []
        for line in lines: 
            documents.append ({'url': '', 'title': line, 'content': line})
        logger.info (f"embeeding of documents {documents}")
        for document in documents: 
            embedding.compute_embeddig (document)
    else: 
        sites = util.readFromFile ("./resources/sites.txt")
        for site in sites:
            logger.info(f"starting urls extraction ... for {site}")
            start_time = time.time()
            urls = scrapping.get_urls(site)
            logger.info(f"found {len(urls)} urls")
            logger.info("urls retrival took --- %s seconds ---" % (time.time() - start_time))
            process_pipeline(urls)


data = os.getenv('DATA', 'PROD')
logger.info (f"semantic search using banchmark {data}")
init(data)






