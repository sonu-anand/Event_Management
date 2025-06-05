# Project_Name:Event_Management

Event_Management is a simple application designed to help users organize, manage, and track events efficiently. It allows users to create events, manage attendees, set schedules, all in one place.

## Installation

Step-by-step instructions on how to get the project running:

Follow these steps to get the Event_Management project running on your Windows machine:

Step 1. **Clone the repository**

Open Command Prompt or PowerShell and run:

```bash
git clone https://github.com/sonu-anand/Event_Management


Step 2. **Setting up Virtual Environment on Windows**

Step 3. Open Command Prompt or PowerShell

Step 4. Navigate to your project directory

Step 5. Create a virtual environment: python -m venv venv

Step 6. Activate the virtual environment: venv\Scripts\activate.bat

Step 7. Install dependencies inside the virtual environment: pip install -r requirements.txt

Step 8. Run application: python run.py

## Assumptions

1. The users will run the application on a Windows operating system with Python (version 3.6 or above) installed.

2. Users have basic familiarity with command-line tools to set up and run the project.

3. All required dependencies will be installed successfully via pip in a virtual environment.

4. The internet connection will be available for downloading dependencies and any necessary updates.

5. Event data provided by users will be accurate and formatted as expected by the application.

## Sample API Request

Endpoints:

1. add_events(http://127.0.0.1:1234/events):
    request_type: POST

    {
    "name":"A Charity Drive for Orphanage Support",
    "location":"Ranchi",
    "start_time":"2025-06-06 09:00 AM",
    "end_time":"2025-09-06 11:00 AM",
    "max_capacity":100
    }

2. get_all_events(http://127.0.0.1:1234/events)
    request_type: GET

3. register_attendees(http://127.0.0.1:1234/events/1/attendees)
    request_type: POST

    {
    "name":"Sonu Anand",
    "email":"xyz_123@gmail.com",
    "event_id":1
    }

4. get_registered_attendees(http://127.0.0.1:1234/events/1/attendees)
    request_type: GET

5. change_timezone(http://127.0.0.1:1234/change_timezone)
    request_type: GET

    {
    "timezone":"Europe/London"
    }

6. paginated_attendees_list(http://127.0.0.1:1234/events/1/attendees/page/1/per_page_record/3)
    request_type: GET

## Standout Features

1. Validations have been implemented to ensure all required input data is provided and not empty. If any key is missing or its value is empty, the system will respond with a list of the missing or empty fields.

2. The start time and end time must be in the format YYYY-MM-DD hh:mm AM/PM (e.g., 2025-06-06 09:00 AM). If the format is incorrect, the system will return an error indicating the issue.

3.The max_capacity key, event_id key must be an integer. Validation has been added to ensure this, and an error will be returned if a non-integer value is provided.

4. Email validation has been added while enetring data into register table.

5. Timezone should in the format like Eg.America/New_York, Europe/London, Asia/Singapore. If it fails to do so then an error message will be displayed.

6. Pagination has been implemented and requires the event_id of the specific event. Additionally, page (the page number to retrieve) and per_page_record (the number of records to display per page) must be provided as inputs.

7. Additionally, an event_management.sql file is included in directory Database Schema to replicate the database schema, and a Postman collection named Event Management.postman_collection.json is provided in directory Postman Collection to help set up and test the API endpoints.