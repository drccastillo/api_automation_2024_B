#!/bin/bash

# Todoist API Key
API_KEY="67a7cb818f2e4434218bfd0122c4d08b2ec7edb7"

# Todoist API Base URL
BASE_URL="https://api.todoist.com/rest/v2/"

# Common headers for requests
COMMON_HEADERS=(
    "-H" "Authorization: Bearer $API_KEY"
    "-H" "Content-Type: application/json"
)

OUTPUT_FILE_All_PROJECTS_NT="outputs/negative_cases/todoist_get_projects_nt.txt"
OUTPUT_FILE_ADD_PROJECT_NT="outputs/negative_cases/todoist_post_project_nt.txt"
OUTPUT_FILE_UPDATE_PROJECT_NT="outputs/negative_cases/todoist_put_project_nt.txt"
OUTPUT_FILE_DELETE_PROJECT_NT="outputs/negative_cases/todoist_delete_project_nt.txt"

# Function to get all projects
get_projects() {
    # Negative Test Scenarios:
    # 1. Invalid Authorization Token
    curl -v -i -X GET -H "Authorization: Bearer INVALID_TOKEN" "${BASE_URL}projects"

    # 2. Incorrect URL
    curl -v -i -X GET "${BASE_URL}incorrect_url"

    # 3. Incorrect HTTP Method
    curl -v -i -X POST "${COMMON_HEADERS[@]}" "${BASE_URL}projects"

    # 4. Omission of Required Headers
    curl -v -i -X GET "${BASE_URL}projects"
}

# Function to create a new project
create_project() {
    local content="$1"

    # Negative Test Scenarios:
    # 1. Empty Project Name
    curl -v -i -X POST "${COMMON_HEADERS[@]}" -d "{}" "${BASE_URL}projects"

    # 2. Invalid Authorization Token
    curl -v -i -X POST -H "Authorization: Bearer INVALID_TOKEN" -d "{\"name\":\"$content\"}" "${BASE_URL}projects"

    # 3. Incorrect HTTP Method
    curl -v -i -X GET "${COMMON_HEADERS[@]}" -d "{\"name\":\"$content\"}" "${BASE_URL}projects"

    # 4. Incorrect JSON Input Data
    curl -v -i -X POST "${COMMON_HEADERS[@]}" -d "Invalid_JSON_Data" "${BASE_URL}projects"

    # Positive Test Scenarios:
    curl -v -i -X POST "${COMMON_HEADERS[@]}" -d "{\"name\":\"$content\"}" "${BASE_URL}projects"

}

# Function to update an existing project
update_project() {
    local project_id="$1"
    local content="$2"

    # Negative Test Scenarios:
    # 1. Incorrect Project ID
    curl -v -i -X POST "${COMMON_HEADERS[@]}" -d "{\"name\":\"$content\"}" "${BASE_URL}projects/INVALID_PROJECT_ID"

    # 2. Empty Project Name
    curl -v -i -X POST "${COMMON_HEADERS[@]}" -d "{}" "${BASE_URL}projects/$project_id"

    # 3. Invalid Authorization Token
    curl -v -i -X POST -H "Authorization: Bearer INVALID_TOKEN" -d "{\"name\":\"$content\"}" "${BASE_URL}projects/$project_id"

    # Positive Test Scenarios:
    curl -v -i -X POST "${COMMON_HEADERS[@]}" -d "{\"name\":\"$content\"}" "${BASE_URL}projects/$project_id"

}

# Function to delete a project
delete_project() {
    local project_id="$1"
    # Negative Test Scenarios:
    # 1. Incorrect Project ID
    curl -v -i -X DELETE "${COMMON_HEADERS[@]}" "${BASE_URL}projects/INVALID_PROJECT_ID"

    # 2. Invalid Authorization Token
    curl -v -i -X DELETE -H "Authorization: Bearer INVALID_TOKEN" "${BASE_URL}projects/$project_id"

    # 3. Incorrect HTTP Method
    curl -v -i -X POST "${COMMON_HEADERS[@]}" "${BASE_URL}projects/$project_id"

    # Positive Test Scenarios:
    curl -v -i -X DELETE "${COMMON_HEADERS[@]}" "${BASE_URL}projects/$project_id"
}

# Example usage
get_projects --output "$OUTPUT_FILE_All_PROJECTS_NT" 2>&1| tee "$OUTPUT_FILE_All_PROJECTS_NT"
create_project "New Project $RANDOM" --output "$OUTPUT_FILE_ADD_PROJECT_NT" 2>&1| tee "$OUTPUT_FILE_ADD_PROJECT_NT"
update_project "$(grep '"id":' "$OUTPUT_FILE_ADD_PROJECT_NT" | awk -F'"' '{print $4}'| tail -n 1)" "Updated Project Name $RANDOM" --output "$OUTPUT_FILE_UPDATE_PROJECT_NT" 2>&1| tee "$OUTPUT_FILE_UPDATE_PROJECT_NT"
delete_project "$(grep '"id":' "$OUTPUT_FILE_UPDATE_PROJECT_NT" | awk -F'"' '{print $4}'| tail -n 1)" --output "$OUTPUT_FILE_DELETE_PROJECT_NT" 2>&1| tee "$OUTPUT_FILE_DELETE_PROJECT_NT"
