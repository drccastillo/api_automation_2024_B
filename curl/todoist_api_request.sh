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

OUTPUT_FILE_All_PROJECTS="outputs/CRUD/todoist_get_projects.txt"
OUTPUT_FILE_ADD_PROJECT="outputs/CRUD/todoist_post_project.txt"
OUTPUT_FILE_UPDATE_PROJECT="outputs/CRUD/todoist_put_project.txt"
OUTPUT_FILE_DELETE_PROJECT="outputs/CRUD/todoist_delete_project.txt"


# Function to get all projects
get_projects() {
    curl -v -i -X GET "${COMMON_HEADERS[@]}" "${BASE_URL}projects"
}

# Function to create a new project
create_project() {
    local content="$1"
    curl -v -i -X POST "${COMMON_HEADERS[@]}" -d "{\"name\":\"$content\"}" "${BASE_URL}projects"
}

# Function to update an existing project
update_project() {
    local project_id="$1"
    local content="$2"
    curl -v -i -X POST "${COMMON_HEADERS[@]}" -d "{\"name\":\"$content\"}" "${BASE_URL}projects/$project_id"
}

# Function to delete a project
delete_project() {
    local project_id="$1"
    curl -v -i -X DELETE "${COMMON_HEADERS[@]}" "${BASE_URL}projects/$project_id"
}

# Example usage
get_projects --output "$OUTPUT_FILE_All_PROJECTS" 2>&1| tee "$OUTPUT_FILE_All_PROJECTS"
create_project "New Project $RANDOM" --output "$OUTPUT_FILE_ADD_PROJECT" 2>&1| tee "$OUTPUT_FILE_ADD_PROJECT"
update_project "$(grep '"id":' "$OUTPUT_FILE_ADD_PROJECT" | awk -F'"' '{print $4}'| tail -n 1)" "New Project Name $RANDOM" --output "$OUTPUT_FILE_UPDATE_PROJECT" 2>&1| tee "$OUTPUT_FILE_UPDATE_PROJECT"
delete_project "$(grep '"id":' "$OUTPUT_FILE_UPDATE_PROJECT" | awk -F'"' '{print $4}'| tail -n 1)" --output "$OUTPUT_FILE_DELETE_PROJECT" 2>&1| tee "$OUTPUT_FILE_DELETE_PROJECT"
