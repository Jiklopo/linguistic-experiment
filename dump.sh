#!/bin/bash
now=$(date +"%+4Y_%m_%d__%H_%M_%S")
base_dir="backups"
json_file="dump.json"
dump_file="$base_dir/$now.zip"

mkdir -p "$base_dir"
venv/bin/python manage.py dumpdata --exclude=contenttypes > "$json_file"
zip -rq "$dump_file" media "$json_file"
rm "$json_file"
echo "Created backup file at $(pwd)/$dump_file"