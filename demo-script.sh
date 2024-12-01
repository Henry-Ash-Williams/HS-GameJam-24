#!/bin/bash 

source ".venv/bin/activate" || echo "Could not activate virtual environment" 

alien_ids=()
images=()

for i in $(seq 1 3); do
    alien=$(curl -s 127.0.0.1:5000/generate-alien)
    echo $alien | jq 
    alien_id=$(echo $alien | jq '.alien.alien_id' | sed 's/\"//g')
    image_url=$(curl -s "http://127.0.0.1:5000/generate-artwork/$alien_id" | jq -r '.image_url')
    alien_ids+=("$alien_id")  # Append the alien_id to the list
    # open $image_url
done
echo 

curl -X POST "http://127.0.0.1:5000/simulate" \
    -H "Content-Type: application/json" \
    -d "{\"alien_ids\": [\"${alien_ids[0]}\", \"${alien_ids[1]}\", \"${alien_ids[2]}\"]}"