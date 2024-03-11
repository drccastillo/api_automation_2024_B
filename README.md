# api_automation_2024_B

Welcome to the API Automation course repository!

This repository serves as the central hub for all activities related to the API Automation course. Throughout this course, you'll engage in a variety of hands-on exercises, assignments, and projects to solidify your understanding and practical skills in automating tests for APIs.

## Task 01: Todoist API Testing Script

## Overview
This bash script is designed to perform testing on the Todoist API. It includes functionalities to test various endpoints of the Todoist API such as getting all projects, creating a new project, updating an existing project, and deleting a project. The script incorporates positive and negative testing scenarios to ensure robustness and reliability of the API.

## Usage
1. Clone the repository to your local machine.
2. Navigate to the directory containing the script.
3. Make sure you have `curl` installed on your system.
4. Set your Todoist API key (`API_KEY`) in the script.
5. Run the script using the command `./todoist_api_testing.sh`.

## Output
### Positive Test Results:
- The responses for positive test cases will be stored in the `outputs/` directory with the following filenames:
  - `todoist_get_projects.txt`: Response for retrieving all projects.
  - `todoist_post_project.txt`: Response for creating a new project.
  - `todoist_put_project.txt`: Response for updating a project.
  - `todoist_delete_project.txt`: Response for deleting a project.

### Negative Test Results:
- The responses for negative test cases will also be stored in the `outputs/` directory with the same filenames as above, but with appended negative test case descriptions.

## Negative Testing
The script incorporates negative testing scenarios to evaluate the robustness and error-handling capabilities of the Todoist API. These scenarios include:
- Invalid authentication tokens
- Incorrect URLs
- Incorrect HTTP methods
- Missing or incorrect request parameters

## Disclaimer
This script is provided for educational and testing purposes only. Use it responsibly and ensure compliance with Todoist's terms of service and API usage guidelines.
