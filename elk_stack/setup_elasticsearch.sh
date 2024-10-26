#!/bin/bash

# Ensure Elasticsearch is pulled and run using Docker

# Set variables
ES_VERSION="7.17.0"
CONTAINER_NAME="elasticsearch"
NETWORK_NAME="elk"

# Create a Docker network for the ELK stack if it doesn't exist
docker network ls | grep -q $NETWORK_NAME || docker network create $NETWORK_NAME

# Pull the Elasticsearch image if not already pulled
docker pull docker.elastic.co/elasticsearch/elasticsearch:$ES_VERSION

# Run Elasticsearch
docker run -d --name $CONTAINER_NAME \
  --net $NETWORK_NAME \
  -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:$ES_VERSION

# Wait for Elasticsearch to start
echo "Waiting for Elasticsearch to start..."
until curl -s http://localhost:9200 > /dev/null; do
  sleep 5
  echo "Still waiting for Elasticsearch..."
done

echo "Elasticsearch setup complete!"
