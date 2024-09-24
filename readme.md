# Fetch Rewards Backend Challenge Submission by Aditya Bilawar

This repository contains a Python-based solution for the Fetch Rewards Backend Challenge. The application is a RESTful API built using Flask that allows you to manage payer points, spend points, and retrieve point balances.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository** (if applicable) or copy the source code to your local machine.

2. **Install the required dependencies** using pip:

    ```bash
    pip install Flask
    ```

## Running the Application

1. **Start the Flask server**:

    ```bash
    python fetch_backend_challenge.py
    ```

   Make sure to replace `fetch_backend_challenge` with the actual name of the Python file containing your code. The server will start on `http://localhost:8000`.

## API Endpoints

### 1. Add Points

- **Endpoint**: `/add`
- **Method**: `POST`
- **Description**: Adds points for a specific payer at a specific timestamp.
- **Request Payload**:
    ```json
    {
      "payer": "DANNON",
      "points": 1000,
      "timestamp": "2022-10-31T10:00:00Z"
    }
    ```
- **Response**: Returns a `200 OK` status if the points are successfully added.

### 2. Spend Points

- **Endpoint**: `/spend`
- **Method**: `POST`
- **Description**: Spends points from the oldest available transactions across all payers.
- **Request Payload**:
    ```json
    {
      "points": 5000
    }
    ```
- **Response**: Returns a JSON array of payers and the points deducted from each.
    ```json
    [
      {"payer": "DANNON", "points": -100},
      {"payer": "UNILEVER", "points": -200},
      {"payer": "MILLER COORS", "points": -4700}
    ]
    ```

### 3. Get Balance

- **Endpoint**: `/balance`
- **Method**: `GET`
- **Description**: Retrieves the current points balance for each payer.
- **Response**: Returns a JSON object representing the balance of each payer.
    ```json
    {
      "DANNON": 1000,
      "UNILEVER": 0,
      "MILLER COORS": 5300
    }
    ```

## Important Notes

- All data is stored in memory, so data will be lost when the server is restarted.
- Make sure to send requests with a valid JSON payload.

## Testing

You can test the endpoints using tools such as Postman or curl. I used Postman and highly recommend downloading it and testing it with it.

### Example with curl:

```bash
curl -X POST "http://localhost:8000/add" -H "Content-Type: application/json" -d '{"payer": "DANNON", "points": 1000, "timestamp": "2022-10-31T10:00:00Z"}'
