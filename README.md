# OpenSource DB 🌱

## Overview 🌐

**OpenSource DB** is a lightweight and flexible API that allows users to create, manage, and manipulate data in various custom databases. Designed with simplicity and extensibility in mind, the application uses Python's Flask framework to expose RESTful API endpoints for database operations.

---

## Summary of the Code 📝

This project uses Flask to build a RESTful API for managing custom databases. The API stores its data in JSON files, ensuring persistence across sessions. Key highlights include:
1. **Endpoints**:
   - CRUD operations for databases and their contents.
   - Backup and health check functionalities.
   - Search capabilities within databases.
2. **Security**:
   - Each database has a unique passcode encrypted with SHA-256 for secure access.
   - Input validation prevents invalid or malicious requests.
3. **Error Handling**:
   - Custom handlers for `404` (Not Found) and `405` (Method Not Allowed) errors.
4. **Utilities**:
   - Random passcode generation and secure encryption.
   - File I/O operations for data persistence.

---

## Features 🚀

- **Create and Manage Databases**: Dynamically create new databases with a unique name.
- **Data Operations**: Add, edit, delete, and view data within a database.
- **Search Functionality**: Query databases for specific data using flexible search parameters.
- **Data Backup**: Save and back up your database for restoration.
- **Security**: Secure operations with unique passcodes for each database.
- **API Health Check**: Easily monitor the health of the API.

---

## Technologies Used 💻

- **Framework**: Flask
- **Storage**: JSON files for data persistence
- **Encryption**: SHA-256 for passcode encryption
- **Language**: Python 3.x

---

## Setup and Installation ⚙️

### Prerequisites
1. Python 3.x installed on your machine.
2. Install `pip` for managing Python packages.

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/SwastikBhattacharjee/OpenSource-DB.git
   cd OpenSource-DB
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the API locally:
   ```
   http://127.0.0.1:5000/
   ```

---

## API Documentation 📚

### Endpoints

#### **1. `/create_database`**
- **Method**: `POST`
- **Description**: Creates a new database with a unique name.
- **Parameters**:
  - `name` (string): Name of the database.
- **Response**:
  - `201`: Database created successfully.
  - `400`: Name is missing or already exists.
- **Example**:
  ```bash
  curl -X POST "http://127.0.0.1:5000/create_database?name=example_db"
  ```

#### **2. `/add_to_database/<name>`**
- **Method**: `POST`
- **Description**: Adds data to a specific database.
- **Parameters**:
  - `name` (string): Name of the database.
  - `key` (string): Key to associate with the data.
  - `passcode` (string): Database passcode.
- **Request Body**: JSON data to be added.
- **Response**:
  - `201`: Data added successfully.
  - `404`: Database or key not found.
  - `400`: Invalid input.
- **Example**:
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  -d '{"data": "example"}' \
  "http://127.0.0.1:5000/add_to_database/example_db?key=example_key&passcode=pass123"
  ```

#### **3. `/view_database/<name>`**
- **Method**: `GET`
- **Description**: Retrieves the contents of a database.
- **Parameters**:
  - `name` (string): Name of the database.
  - `passcode` (string): Database passcode.
- **Response**:
  - `200`: Database retrieved successfully.
  - `404`: Database not found.
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/view_database/example_db?passcode=pass123"
  ```

#### **4. `/delete_database/<name>`**
- **Method**: `DELETE`
- **Description**: Deletes a database.
- **Parameters**:
  - `name` (string): Name of the database.
  - `passcode` (string): Database passcode.
- **Response**:
  - `200`: Database deleted.
  - `404`: Database not found.
- **Example**:
  ```bash
  curl -X DELETE "http://127.0.0.1:5000/delete_database/example_db?passcode=pass123"
  ```

#### **5. `/search_in_database/<name>`**
- **Method**: `GET`
- **Description**: Searches for specific data within a database.
- **Parameters**:
  - `name` (string): Name of the database.
  - `search_param` (string): Key to search for.
  - `passcode` (string): Database passcode.
- **Response**:
  - `200`: Data found.
  - `404`: Data not found.
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/search_in_database/example_db?search_param=example_key&passcode=pass123"
  ```

#### **6. `/backup`**
- **Method**: `POST`
- **Description**: Triggers a data backup.
- **Response**:
  - `200`: Backup successful.
- **Example**:
  ```bash
  curl -X POST "http://127.0.0.1:5000/backup"
  ```

#### **7. `/health`**
- **Method**: `GET`
- **Description**: Checks the health of the API.
- **Response**:
  - `200`: API is healthy.
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/health"
  ```

---

## Security Features 🔒

- **Encrypted Passcodes**: Passcodes are hashed using SHA-256.
- **Rate Limiting**: Add `Flask-Limiter` for protection against API abuse.
- **Validation**: Input validation ensures database names and passcodes conform to requirements.

---

## Future Enhancements 🌟

1. **User Authentication**: Implement JWT or API keys for secure access.
2. **Database Restoration**: Add functionality to restore from backups.
3. **Pagination**: Handle large datasets efficiently.
4. **Advanced Search**: Enable complex queries and filters.

---

## About the Author ✨

Swastik Bhattacharjee is the developer behind OpenSource DB. Passionate about backend development, Swastik aims to create efficient and secure APIs that simplify database operations. This project is a testament to his commitment to open-source innovation.

---

## Contributing 🤝

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
