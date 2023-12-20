#!/bin/bash


SRC_FILE="bashcrc.txt"
DEST_FILE="bashcrc"

if [ ! -f "$SRC_FILE" ] || [ ! -f "$DEST_FILE" ]; then
    echo "Error: Required file(s) missing."
    exit 1
fi

extract_value() {
    grep "$1=" "$SRC_FILE" | cut -d '=' -f2
}

update_file() {
    local key=$1
    local value
    value=$(extract_value "$key")
    sed -i "s|^export $key=.*$|export $key=$value|" "$DEST_FILE"
}

VARS=("ARTIFACTORY_API_KEY" "ARTIFACTORY_USER" "ANDROID_HOME" "JAVA_HOME" "IVI_ADB_SERIAL")

for var in "${VARS[@]}"; do
    update_file "$var"
done

echo "Update complete."

