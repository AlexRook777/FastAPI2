# FastAPI Book API

This is a simple Book API built with FastAPI.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AlexRook777/FastAPI2.git
   cd FastAPI2
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows, use:
   # venv\Scripts\activate
   
   # On macOS and Linux, use:
   # source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, use the following command:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Running the Tests

To run the tests, use the following command:

```bash
pytest
