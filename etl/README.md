## ETL: Extract, Transform, and Load Pipeline
This project implements an ETL pipeline where data is retrieved and indexed using a Transformer model.

## Overview

- Data Extraction: We retrieve relevant URLs from the provided websites using sitemap XML files.
Website Configuration: The list of websites to be processed is defined in the sites.txt file, located in the resources folder.
- Parallel Processing: We utilize multiple processes for data extraction and vector embedding to speed up both phases.
  
## Possible Optimizations

- Cluster Deployment: For a production environment, a Solr cluster can further accelerate the indexing process by distributing the load across multiple nodes.
- Retry Mechanism: To enhance resilience, implementing a retry mechanism would ensure that if the process fails, it can resume from where it left off rather than starting from the beginning.

