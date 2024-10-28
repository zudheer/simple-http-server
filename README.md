
# Simple HTTP Server

This Python script runs a basic HTTP server capable of handling limited requests, including file retrieval, echoing strings, reading user-agent headers, and simple file creation. It can be easily started using command-line arguments.

### Features

1. **Echo Endpoint** (`GET /echo/{string}`): Returns the specified string in the response body.
2. **User-Agent Endpoint** (`GET /user-agent`): Reads and returns the User-Agent from the request header.
3. **File Retrieval** (`GET /files/{filename}`): Returns the contents of a file if it exists in the specified directory.
4. **File Creation** (`POST /files/{filename}`): Creates a file in the specified directory with the provided content.

### Prerequisites

- Python 3.7 or later
- Run in an environment with internet access if needed for dependencies

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project_directory>
   ```

### Usage

To start the server, run the script with the following command:
```bash
python my_server.py -d <directory>
```

Replace `<directory>` with the path to the directory where files will be read from or written to.

**Example**:
```bash
python my_server.py -d ./files
```

#### Endpoints

1. **Echo Endpoint**  
   - **Request**: `GET /echo/{string}`  
   - **Response**: Returns the string in the response body.

2. **User-Agent Endpoint**  
   - **Request**: `GET /user-agent`  
   - **Response**: Returns the User-Agent header sent in the request.

3. **File Retrieval**  
   - **Request**: `GET /files/{filename}`  
   - **Response**: Returns the contents of the specified file if it exists.

4. **File Creation**  
   - **Request**: `POST /files/{filename}`  
   - **Response**: Creates the specified file in the directory with the provided content.

### Example Requests

- **Echo a String**:
  ```bash
  curl -i http://localhost:4221/echo/hello
  ```

- **Retrieve User-Agent**:
  ```bash
  curl -i http://localhost:4221/user-agent -A "MyCustomAgent/1.0"
  ```

- **Retrieve a File**:
  ```bash
  curl -i http://localhost:4221/files/example.txt
  ```

- **Create a File**:
  ```bash
  curl -i -X POST http://localhost:4221/files/newfile -d "Hello, World!"
  ```

### Exiting the Server

Stop the server by pressing `Ctrl + C`.

### License

This project is licensed under the MIT License.
