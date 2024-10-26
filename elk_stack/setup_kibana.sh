#!/bin/bash

# Ensure Kibana is pulled and run using Docker

# Set variables
KIBANA_VERSION="7.17.0"
CONTAINER_NAME="kibana"
NETWORK_NAME="elk"

# Pull the Kibana image if not already pulled
docker pull docker.elastic.co/kibana/kibana:$KIBANA_VERSION

# Run Kibana
docker run -d --name $CONTAINER_NAME \
  --net $NETWORK_NAME \
  -p 5601:5601 \
  -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" \
  docker.elastic.co/kibana/kibana:$KIBANA_VERSION

echo "Kibana setup complete! Access Kibana at http://localhost:5601"
