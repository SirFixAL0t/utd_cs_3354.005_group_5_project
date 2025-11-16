# SyncUp Project - CS3354.005 Group 5
_By Students, for Students, for all your Scheduling needs._
## Intro
**SyncUp** is a platform designed by students for students to make coordination and schedule planning much easier.  Whether it's balancing group hangouts, study sessions, or simply just club meetings, SyncUp makes it simple to align schedules and stay connected.

## Scope
The project involves developing a calendar-based scheduling app that allows students to link their school accounts using their student ID or email to import class schedules automatically. The app will enable users to add friends from their school, view shared availability, and compare schedules to find overlapping free time for socializing, studying, or group work.

### Key features
1. calendar syncing
2. permission-based visibility of schedules
3. smart suggestions for common free periods
4. privacy controls to manage who can view a user’s availability.
5. and more!

### Calendar integration
The app will integrate with school systems where possible, support manual input for institutions that are not supported, and prioritize data security and user privacy in compliance with educational data standards.

## Members
* Frabina Edwin
* Evan Spahr
* Fahim Hassan
* Henry Nguyen
* Fred Enrriquez
* Hasti Patel

## Backend Development Guide

This guide provides instructions for frontend developers on how to run the backend server and integrate it with the React UI.

### Running the Backend Server

To run the backend server for local development and testing, follow these steps:

1.  **Install Dependencies**: Make sure you have Python 3.12 or higher installed. Then, install the required packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment**: Create a `.env` file in the project root. You can copy the `.env.example` file as a template. This file controls settings like the server port and frontend URL.

3.  **Run the Server**: Start the server by running the `run.py` script.
    ```bash
    python run.py
    ```
    The server will start on the host and port specified in your `.env` file (e.g., `http://127.0.0.1:8000`). The `--reload` flag is enabled by default, so the server will restart automatically when you change the code.

4.  **Access the API**: Once the server is running, you can access the API at the configured address. The interactive API documentation (provided by Swagger UI) is available at `/docs` (e.g., `http://127.0.0.1:8000/docs`).

### Integrating with a React Frontend

To connect your React application to this backend, you will make HTTP requests to the various API endpoints.

1.  **CORS Configuration**: The backend is configured to accept requests from the URL specified in the `FRONTEND_ORIGIN` environment variable in your `.env` file.

2.  **Making API Calls from React**: You can use any HTTP client library in your React app, such as `axios` or the built-in `fetch` API. Here is an example of how to register a new user using `axios`:

    ```javascript
    import axios from 'axios';

    const API_URL = 'http://127.0.0.1:8000';

    const registerUser = async (userData) => {
      try {
        const response = await axios.post(`${API_URL}/auth/register`, userData);
        return response.data;
      } catch (error) {
        console.error('Error registering user:', error.response.data);
        throw error;
      }
    };
    ```

3.  **Authentication**: Most endpoints require authentication. When a user logs in via the `/auth/token` endpoint, the backend will return an `access_token`. You must store this token (e.g., in local storage or component state) and include it in the `Authorization` header for all subsequent requests:

    ```javascript
    // Set the token for all future axios requests
    axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
    ```

## API Testing Portal

FastAPI provides an automatic, interactive API documentation portal that you can use to test the backend without a UI.

1.  **Start the Server**: Follow the instructions in the "Running the Backend Server" section.
2.  **Open the Portal**: Navigate to `/docs` on your running server (e.g., `http://127.0.0.1:8000/docs`).

### How to Use the Testing Portal

1.  **Find an Endpoint**: The portal lists all available API endpoints, grouped by tags (e.g., "auth", "calendar").
2.  **Try it Out**: Click on an endpoint to expand it, then click the "Try it out" button.
3.  **Fill in Parameters**: The portal will show all the required parameters and provide an editable text area for the request body. You can copy-paste payloads here.
4.  **Execute**: Click the "Execute" button to send the request to your running server. The portal will display the server's response, including the status code and response body.

### Testing Authenticated Endpoints

To test endpoints that require a user to be logged in, follow these steps:

1.  **Get a Token**:
    *   Go to the `/auth/token` endpoint in the portal.
    *   Click "Try it out".
    *   Enter a user's email as the `username` and their password as the `password`.
    *   Click "Execute".
    *   Copy the `access_token` from the response body.

2.  **Authorize Your Session**:
    *   At the top right of the page, click the "Authorize" button.
    *   In the "Value" field of the popup, paste the full token, including the word "Bearer" (e.g., `Bearer eyJhbGciOi...`).
    *   Click "Authorize", then "Close".

You can now test any of the locked endpoints, and the portal will automatically include your token in the request headers.
