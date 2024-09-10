# Basic Semantic Search Platform

This project is a basic semantic search platform that allows users to search for content indexed with semantic embeddings. The platform uses Docker to set up and run a full environment including Solr, Flask, and a data extraction pipeline.

## Prerequisites

- [Docker](https://www.docker.com/) installed on your system.

## Getting Started

To build and run the application:

docker-compose up --build

After running the command, give it a few moments for the following services to start:

- Solr instance
- Flask server
- Initialization script execution

Once everything is ready, open your browser and navigate to:

http://localhost:3000

You can enter your search query in the UI.

## Search Queries

Example query:
Try searching for "unspoken language" on the UI, or use the following curl command on the command line:

curl "http://localhost:5001/search?query=Unspoken+language"

## Environment Configuration
In the docker-compose.yml file, you can set the DATA environment variable to choose which benchmark to use for the search platform:

Available Modes:

TEST (default):

Reads some example titles from a file and indexes them. Best used for the first launch to test basic functionality.

PROD:

- Reads sitemap files from a resource file.
- Launches a pipeline that:
- Extracts URLs from the sitemap.
- Downloads content from each URL.
- Creates a document for each URL.
- Indexes each document using a transformer library and Solr.

This mode is suitable for larger datasets and production use cases.