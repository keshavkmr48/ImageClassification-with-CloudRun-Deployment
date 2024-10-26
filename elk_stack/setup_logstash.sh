#!/bin/bash

# Ensure Logstash is pulled and run using Docker

# Set variables
LOGSTASH_VERSION="7.17.0"
CONTAINER_NAME="logstash"
NETWORK_NAME="elk"

# Pull the Logstash image if not already pulled
docker pull docker.elastic.co/logstash/logstash:$LOGSTASH_VERSION

# Create Logstash configuration
LOGSTASH_CONFIG=$(cat <<EOF
input {
  beats {
    port => 5044
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "logstash-%{+YYYY.MM.dd}"
  }
}
EOF
)

# Write Logstash config to file
echo "$LOGSTASH_CONFIG" > logstash.conf

# Run Logstash
docker run -d --name $CONTAINER_NAME \
  --net $NETWORK_NAME \
  -p 5044:5044 \
  -v $(pwd)/logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro \
  docker.elastic.co/logstash/logstash:$LOGSTASH_VERSION

echo "Logstash setup complete!"
