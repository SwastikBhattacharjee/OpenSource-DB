# Importing required Libraries
from flask import Flask, request, jsonify
import json
import time
import string
import random
import hashlib





# Create a Flask application
app = Flask(__name__)

# Set the path to your favicon file
app.config['FAVICON'] = 'logo.ico'

# Set the name of your API
app.name = 'OpenSource DB'

# Create a dictionary to store the data
data = {}
passcodes = {}





# Load existing data and passcodes from files
try:
    with open('database.json', 'r') as openfile:
        data = json.load(openfile)
    with open('passcodes.json', 'r') as openfile:
        passcodes = json.load(openfile)
except:
    data = {}
    passcodes = {}





@app.errorhandler(404)
def not_found_error(error):
    """
    Handle 404 errors by returning a JSON response.

    Parameters:
        error: Error object.

    Returns:
        JSON response with error details and status code 404.
    """
    saveData()
    return jsonify({
        'message': 'This endpoint is not found or is currently disabled!',
        'error': str(error)
    }), 404





@app.errorhandler(405)
def method_not_allowed_error(error):
    """
    Handle 405 errors by returning a JSON response.

    Parameters:
        error: Error object.

    Returns:
        JSON response with error details and status code 405.
    """
    saveData()
    return jsonify({
        'message': 'Try setting the method to either GET, PUT, DELETE or POST. Check the documentation to see which endpoint accepts which kind of method.',
        'error': str(error)
    }), 405





@app.route('/', methods=['GET'])
def api_documentation():
    """
    Display the API documentation.

    Returns:
        JSON response with API details and endpoints.
    """
    api_documentation = {
        "api_name": "OpenSource DB",
        "description": "This API allows you to manage and manipulate data in various databases.",
        "version": "1.3",
        "author": "Swastik Bhattacharjee",
        "data_from": "*",
        "endpoints": [
            {
                "endpoint": "/create_database",
                "methods": ["POST"],
                "description": "Creates a new database with the given name.",
                "parameters": [
                    {"name": "name", "type": "string", "description": "The name of the database."}
                ],
                "response": [
                    {"status_code": 400, "message": "Database with this name already exists."},
                    {"status_code": 201, "message": "Database created successfully."},
                    {"status_code": 400, "message": "Expected a name as an argument."}
                ],
                "example": "POST /create_database?name=example_db"
            },
            {
                "endpoint": "/add_to_database/<string:name>",
                "methods": ["POST"],
                "description": "Adds data to the database for the given name.",
                "parameters": [
                    {"name": "name", "type": "string", "description": "The name of the database."},
                    {"name": "key", "type": "string", "description": "The key by which it should be added."},
                    {"name": "passcode", "type": "string", "description": "The passcode of the database."}
                ],
                "request_body": "JSON data to be added to the database.",
                "response": [
                    {"status_code": 201, "message": "Data added to Database successfully."},
                    {"status_code": 404, "message": "Database not found."},
                    {"status_code": 400, "message": "Expected a JSON object to be sent in the request body."}
                ],
                "example": "POST /add_to_database/example_db?key=item_key&passcode=pass123"
            },
            {
                "endpoint": "/view_database/<string:name>",
                "methods": ["GET"],
                "description": "Retrieves a specific database entry based on the given name.",
                "parameters": [
                    {"name": "name", "type": "string", "description": "The name of the database to retrieve."},
                    {"name": "passcode", "type": "string", "description": "The passcode of the database."}
                ],
                "response": [
                    {"status_code": 200, "message": "JSON response containing the corresponding database entry."},
                    {"status_code": 404, "message": "Database not found."}
                ],
                "example": "GET /view_database/example_db?passcode=pass123"
            },
            {
                "endpoint": "/delete_database/<string:name>",
                "methods": ["DELETE"],
                "description": "Deletes a specific database entry based on the given name.",
                "parameters": [
                    {"name": "name", "type": "string", "description": "The name of the database to delete."},
                    {"name": "passcode", "type": "string", "description": "The passcode of the database."}
                ],
                "response": [
                    {"status_code": 200, "message": "Database deleted successfully."},
                    {"status_code": 404, "message": "Database not found."}
                ],
                "example": "DELETE /delete_database/example_db?passcode=pass123"
            },
            {
                "endpoint": "/search_in_database/<string:name>",
                "methods": ["GET"],
                "description": "Searches for data within a specific database based on the given name.",
                "parameters": [
                    {"name": "search_param", "type": "string", "description": "The key to search for within the database."},
                    {"name": "passcode", "type": "string", "description": "The passcode of the database."}
                ],
                "response": [
                    {"status_code": 200, "message": "JSON response containing the data matching the search criteria."},
                    {"status_code": 404, "message": "Database or search parameter not found."},
                    {"status_code": 500, "message": "An error occurred while searching the database."}
                ],
                "example": "GET /search_in_database/example_db?search_param=item_key&passcode=pass123"
            },
            {
                "endpoint": "/delete_from_database/<string:database>/<string:key>",
                "methods": ["DELETE"],
                "description": "Deletes specific data within a database based on the given database name and data key.",
                "parameters": [
                    {"name": "database", "type": "string", "description": "The name of the database."},
                    {"name": "key", "type": "string", "description": "The key of the data to delete."},
                    {"name": "passcode", "type": "string", "description": "The passcode of the database."}
                ],
                "response": [
                    {"status_code": 200, "message": "Data deleted successfully."},
                    {"status_code": 404, "message": "Database or data key not found."},
                    {"status_code": 500, "message": "An error occurred while deleting the data."}
                ],
                "example": "DELETE /delete_from_database/example_db/item_key?passcode=pass123"
            },
            {
                "endpoint": "/edit_in_database/<string:database>/<string:key>",
                "methods": ["PUT"],
                "description": "Edits specific data within a database based on the given database name and data key.",
                "parameters": [
                    {"name": "database", "type": "string", "description": "The name of the database."},
                    {"name": "key", "type": "string", "description": "The key of the data to edit."},
                    {"name": "passcode", "type": "string", "description": "The passcode of the database."}
                ],
                "request_body": "JSON data with new values to update the existing data.",
                "response": [
                    {"status_code": 200, "message": "Data edited successfully."},
                    {"status_code": 404, "message": "Database or data key not found."},
                    {"status_code": 500, "message": "Expected a JSON object to be sent in the request body."}
                ],
                "example": "PUT /edit_in_database/example_db/item_key?passcode=pass123"
            },
            {
                "endpoint": "/download_data/<string:name>",
                "methods": ["GET"],
                "description": "Downloads the data of a specific database.",
                "parameters": [
                    {"name": "name", "type": "string", "description": "The name of the database to download."},
                    {"name": "passcode", "type": "string", "description": "The passcode of the database."}
                ],
                "response": [
                    {"status_code": 200, "message": "JSON response containing the database data."},
                    {"status_code": 404, "message": "Database not found."}
                ],
                "example": "GET /download_data/example_db?passcode=pass123"
            },
            {
                "endpoint": "/backup",
                "methods": ["POST"],
                "description": "Trigger data backup.",
                "parameters": [],
                "response": [
                    {"status_code": 200, "message": "Data backup completed successfully."}
                ],
                "example": "POST /backup"
            },
            {
                "endpoint": "/query_data",
                "methods": ["GET"],
                "description": "Query data in a specific database.",
                "parameters": [
                    {"name": "database_name", "type": "string", "description": "The name of the database to query."},
                    {"name": "search_param", "type": "string", "description": "The search parameter to filter data."},
                    {"name": "passcode", "type": "string", "description": "The passcode of the database."}
                ],
                "response": [
                    {"status_code": 200, "message": "JSON response containing queried data."},
                    {"status_code": 404, "message": "Database not found."},
                    {"status_code": 500, "message": "An error occurred while querying the data."}
                ],
                "example": "GET /query_data?database_name=example_db&search_param=item_key&passcode=pass123"
            },
            {
                "endpoint": "/health",
                "methods": ["GET"],
                "description": "Check the health and status of the API.",
                "parameters": [],
                "response": [
                    {"status_code": 200, "message": "API is running and healthy."},
                    {"status_code": 500, "message": "API is not running as expected."}
                ],
                "example": "GET /health"
            }
        ]
    }
    saveData()
    return jsonify(api_documentation)





@app.route('/health', methods=['GET'])
def health():
    """
    Check the health and status of the API.

    Returns:
        JSON response indicating whether the API is healthy.
    """
    # Check if your API has any specific health checks to perform.
    # You can include additional checks based on your application's needs.

    # For this example, we'll assume the API is healthy if it's running.
    # You can customize this logic based on your application's requirements.
    is_healthy = True

    # Define the response based on the health status.
    if is_healthy:
        response = {
            'status': 'healthy',
            'message': 'API is running and healthy.'
        }
        status_code = 200
    else:
        response = {
            'status': 'unhealthy',
            'message': 'API is not running as expected.'
        }
        status_code = 500
    saveData()
    return jsonify(response), status_code





def validateName(name):
  """
  Validate the provided database name.

  Parameters:
      name (str): The name of the database to validate.

  Returns:
      tuple: A boolean indicating validity, a JSON response, and an HTTP status code.
  """

  if len(name) < 4 or len(name) > 25:
    return False, jsonify({'message': 'Database name must be between 4 and 25 characters.'}), 400

  if not str(name[0]).isalpha():
    return False, json({"message": "Database name must start with a letter."}), 400

  if str(name[-1] ) == '_':
    return False, jsonify({'message': 'Database name cannot end with an underscore.'}), 400
  
  # Check if the name contains only valid characters
  valid_grammar = set('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_')

  if not set(name).issubset(valid_grammar):
    return False, jsonify({'message': 'Database name contains invalid characters.'}), 400

  return True, jsonify({'message': 'Database name is valid'}), 201

  



def validatePasscode(passcode):
  """
  Validate the provided passcode for a database.

  Parameters:
      passcode (str): The passcode to validate.

  Returns:
      tuple: A boolean indicating validity, a JSON response, and an HTTP status code.
  """
  # Check if the passcode is given
  if not passcode:
    saveData()
    return False, jsonify({'message': 'Passcode for the database not provided. Provide a passcode as the parameter'}), 400
  
  # Check if the passcode is valid
  if not (encryptPasscode(passcode) == passcodes[name]['passcode']):
    saveData()
    return False, jsonify({'message': 'Invalid passcode for the database.'}), 400

  return True, jsonify({'message': 'Valid passcode!.'}), 201





@app.route('/create_database', methods=['POST'])
def create_database():
    """
    Create a new database with the specified name.

    Parameters:
        None (expects 'name' in the query parameters).

    Returns:
        JSON response with success or error message.
    """
    try:
        # Get the name parameter from the request
        name = request.args.get('name')

        # Check if name is given
        if not name:
          return jsonify({'message': 'Expected a name as an argument.'}), 400

        # Validate the name parameter
        valid, response, status_code = validateName(name)
        if not valid:
          return response, status_code


        # Check if a database with the same name already exists
        if name in data:
            return jsonify({'message': 'Database with this name already exists.'}), 400

        # Create a new database with an empty dictionary
        data[name] = {}
        passcode = generatePasscode()
        passcodes[name] = {'passcode': encryptPasscode(passcode), 'created_at': time.time()}

        saveData()
    
        return jsonify({
          'message': 'Database created successfully.',
          'passcode': passcode,
          'created_at': time.time()
        }), 201
    except:
        saveData()
        return jsonify({'message': 'Expected a name as an argument.'}), 400





@app.route('/add_to_database/<string:name>', methods=['POST'])
def add_to_database(name):
    """
    Add data to a specified database.

    Parameters:
        name (str): The name of the database.

    Returns:
        JSON response with success or error message.
    """
    try:
      # Validate the name parameter
      valid, response, status_code = validateName(name)
      if not valid:
        return response, status_code

      # Get the name parameter from the request
      if not (name in data):
        saveData()
        return jsonify({'message': 'Database not found.'}), 404


      passcode = request.args.get('passcode')

      # Validate the passcode
      valid, response, status_code = validatePasscode(passcode)
      if not valid:
        return response, status_code


      # Assuming JSON data is sent in the request body
      data_to_add = request.json
      

      # Get the name parameter from the request
      key = request.args.get('key')
      
      
      if key:
        data[name][str(key)] = data_to_add
        saveData()
        return jsonify({'message': 'Data added to Database successfully.'}), 201
      else:
        saveData()
        return jsonify({'message': 'Data key not found in the database.'}), 404
          
    except:
      saveData()
      return jsonify({'message': 'Expected a JSON object and a parameter termed "name" to be sent in the request body.'}), 400






@app.route('/view_database/<string:name>', methods=['GET'])
def view_database(name):
    """
    Retrieve the contents of a specific database.

    Parameters:
        name (str): The name of the database.

    Returns:
        JSON response containing the database contents or an error message.
    """
    # Validate the name parameter
    valid, response, status_code = validateName(name)
    if not valid:
      return response, status_code

    # Check if the database exists in the 'data' dictionary
    if name in data:
      passcode = request.args.get('passcode')

      # Validate the passcode
      valid, response, status_code = validatePasscode(passcode)
      if not valid:
        return response, status_code

      # Return the corresponding database entry as a JSON response
      saveData()
      return jsonify(data[name])
    else:
        # Return a JSON response with a 'message' key set to 'Database not found.' and a status code of 404
        saveData()
        return jsonify({'message': 'Database not found.'}), 404
    





@app.route('/delete_database/<string:name>', methods=['DELETE'])
def delete_database(name):
    """
    Deletes a specific database entry based on the given name.

    Parameters:
        name (str): The name of the database to delete.

    Returns:
        If the database exists, returns a JSON response with a 'message' key set to 'Database deleted successfully.' and a status code of 200.
        If the database does not exist, returns a JSON response with a 'message' key set to 'Database not found.' and a status code of 404.
    """
  
    # Validate the name parameter
    valid, response, status_code = validateName(name)
    if not valid:
      return response, status_code

    # Check if the database exists in the 'data' dictionary
    if name in data:
        passcode = request.args.get('passcode')

        # Validate the passcode
        valid, response, status_code = validatePasscode(passcode)
        if not valid:
          return response, status_code

        # Delete the corresponding database entry
        del data[name]
        # Return a JSON response with a 'message' key set to 'Database deleted successfully.' and a status code of 200
        saveData()
        return jsonify({'message': 'Database deleted successfully.'}), 200
    else:
        # Return a JSON response with a 'message' key set to 'Database not found.' and a status code of 404
        saveData()
        return jsonify({'message': 'Database not found.'}), 404
    






@app.route('/search_in_database/<string:name>', methods=['GET'])
def search_in_database(name):
    """
    Searches for data within a specific database based on the given name.

    Parameters:
        name (str): The name of the database to search within.

    Returns:
        If the database exists, returns a JSON response containing the data matching the search criteria.
        If the database does not exist or the search parameter is not found, returns a JSON response with a 'message' key set to 'Database or search parameter not found.' and a status code of 404.
    """
    try:
  
        # Validate the name parameter
        valid, response, status_code = validateName(name)
        if not valid:
          return response, status_code

        if name in data:
          passcode = request.args.get('passcode')

          # Validate the passcode
          valid, response, status_code = validatePasscode(passcode)
          if not valid:
            return response, status_code

          search_param = request.args.get('search_param')

          # Check if the search parameter exists in the database
          if search_param in data[name]:
              saveData()
              # Return the matching data as a JSON response
              return jsonify(data[name][search_param])
          else:
              saveData()
              return jsonify({'message': 'Search parameter not found in the database.'}), 404
        else:
            saveData()
            return jsonify({'message': 'Database not found.'}), 404
    except:
        saveData()
        return jsonify({'message': 'An error occurred while searching the database.'}), 500
    






@app.route('/delete_from_database/<string:database>/<string:key>', methods=['DELETE'])
def delete_from_database(database, key):
    """
    Deletes specific data within a database based on the given database name and data key.

    Parameters:
        database (str): The name of the database.
        key (str): The key of the data to delete.

    Returns:
        If the database and data key exist, deletes the data and returns a JSON response with a 'message' key set to 'Data deleted successfully.' and a status code of 200.
        If the database or data key do not exist, returns a JSON response with a 'message' key set to 'Database or data key not found.' and a status code of 404.
    """
    try:
        # Validate the name parameter
        valid, response, status_code = validateName(database)
        if not valid:
          return response, status_code

        if database in data:
            passcode = request.args.get('passcode')

            # Validate the passcode
            valid, response, status_code = validatePasscode(passcode)
            if not valid:
              return response, status_code

            if key in data[database]:
                del data[database][key]
                saveData()
                return jsonify({'message': 'Data deleted successfully.'}), 200
            else:
                saveData()
                return jsonify({'message': 'Data key not found in the database.'}), 404
        else:
            saveData()
            return jsonify({'message': 'Database not found.'}), 404
    except Exception as e:
        saveData()
        print("Exception:-", e)
        return jsonify({'message': 'An error occurred while deleting the data.'}), 500
      
    





@app.route('/edit_in_database/<string:database>/<string:key>', methods=['PUT'])
def edit_in_database(database, key):
    """
    Edits specific data within a database based on the given database name and data key.

    Parameters:
        database (str): The name of the database.
        key (str): The key of the data to edit.

    Returns:
        If the database and data key exist, edits the data with new values provided in the request body
        and returns a JSON response with a 'message' key set to 'Data edited successfully.' and a status code of 200.
        If the database or data key do not exist, returns a JSON response with a 'message' key set to 'Database or data key not found.' and a status code of 404.
    """
    try:
        # Validate the name parameter
        valid, response, status_code = validateName(database)
        if not valid:
          return response, status_code

        if database in data:
            passcode = request.args.get('passcode')

            # Validate the passcode
            valid, response, status_code = validatePasscode(passcode)
            if not valid:
              return response, status_code

            key = str(key)
            if key in data[database]:
                new_data = request.json  # Assuming JSON data with new values is sent in the request body
                data[database][key] = new_data
                saveData()
                return jsonify({'message': 'Data edited successfully.'}), 200
            else:
                saveData()
                return jsonify({'message': 'Data key not found in the database.'}), 404
        else:
            saveData()
            return jsonify({'message': 'Database not found.'}), 404
    except:
        saveData()
        return jsonify({'message': 'Expected a JSON object to be sent in the request body.'}), 500
    






@app.route('/download_data/<string:name>', methods=['GET'])
def download_data(name):
    # Validate the name parameter
    valid, response, status_code = validateName(name)
    if not valid:
      return response, status_code

    # Check if the database exists in the 'data' dictionary
    if name in data:
      passcode = request.args.get('passcode')

      # Validate the passcode
      valid, response, status_code = validatePasscode(passcode)
      if not valid:
        return response, status_code


      # Return the corresponding database entry as a JSON response
      saveData()
      return jsonify(data[name])
    else:
        # Return a JSON response with a 'message' key set to 'Database not found.' and a status code of 404
        saveData()
        return jsonify({'message': 'Database not found.'}), 404







@app.route('/query_data', methods=['GET'])
def query_data():
    """
    Retrieves data from a specified database based on the provided search parameter.
    
    Parameters:
        None
    
    Returns:
        - If the 'database_name' parameter is not found in the data dictionary, returns a JSON response with a message of 'Database not found.' and a status code of 404.
        - If the 'search_param' parameter is provided, returns a JSON response with the query results containing all key-value pairs from the specified database that match the search parameter. If no matches are found, an empty dictionary is returned.
        - If the 'search_param' parameter is not provided, returns a JSON response with all key-value pairs from the specified database.
        - If any exception occurs during the execution of the function, returns a JSON response with an error message and a status code of 500.
    """
    try:
        database_name = request.args.get('database_name')

        # Validate the name parameter
        valid, response, status_code = validateName(database_name)
        if not valid:
          return response, status_code
          
        search_param = request.args.get('search_param')
        
        if database_name not in data:
            saveData()
            return jsonify({'message': 'Database not found.'}), 404
        
        if search_param:
            passcode = request.args.get('passcode')

            # Validate the passcode
            valid, response, status_code = validatePasscode(passcode)
            if not valid:
              return response, status_code

            # Search for data in the specified database based on the search parameter
            query_result = {}
            for key, value in data[database_name].items():
                if search_param.lower() in key.lower() or search_param.lower() in str(value).lower():
                    query_result[key] = value
            saveData()
            return jsonify(query_result)
        else:
            saveData()
            # Return all data in the specified database
            return jsonify(data[database_name])
    except Exception as e:
        saveData()
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500






# Function to save data to a JSON file
def save_data_to_file():
    """
    Saves the data to a file named 'data_backup.json'.

    Parameters:
        None

    Returns:
        None
    """
    with open('data_backup.json', 'w') as file:
        json.dump(data, file)






# Create an endpoint to trigger data backup
@app.route('/backup', methods=['POST'])
def backup_data():
    """
    Endpoint for backing up data.

    This function is called when a POST request is made to the '/backup' route. It saves the data to a file and returns a JSON response with a success message.

    Parameters:
    None

    Returns:
    A tuple containing a JSON response and an HTTP status code. The JSON response contains a message indicating the success of the backup operation.
    """
    save_data_to_file()
    saveData()
    return jsonify({'message': 'Data backup completed successfully.'}), 200






def saveData():
  """
  Save data to a JSON file.

  This function takes no parameters and does not return anything. It saves the
  given data as a JSON object in a file named "database.json" in the current
  directory.

  Parameters:
    None

  Returns:
    None
  """
  global data
  global passcodes
  # Convert data to a JSON string with indentation
  json_object = json.dumps(data, indent=4)

  # Convert passcodes to a JSON string with indentation
  passcode_object = json.dumps(passcodes, indent=4)

  # Print a message to console
  print("[SERVER] SAVED DATA ON METHOD CALL!")
  
  # Open the file in write mode and write the JSON string to it
  with open("database.json", "w") as outfile:
    outfile.write(json_object)

  # Open the file in write mode and write the JSON string to it 
  with open("passcodes.json", "w") as outfile:
    outfile.write(passcode_object)






def generatePasscode():
  """
  Generate a random passcode.

  This function generates a random passcode consisting of 6 digits.

  Parameters:
    None

  Returns:
    A string representing the generated passcode.
  """
  # Generate a random passcode consisting of 15 digits
  passcode = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=15))

  # Return the passcode
  return passcode





def encryptPasscode(passcode):
  """
  Encrypt a passcode using the Fernet encryption algorithm.
  
  This function takes a passcode as input and encrypts it using the SHA 256 encryption algorithm.
  
  Parameters:
    passcode (str): The passcode to be encrypted.
    
  Returns:
    A string representing the encrypted passcode.
  """
  # Hash the passcode using the SHA 256 encryption algorithm
  result = hashlib.sha256(passcode.encode()) 

  # Return the hexadecimal representation of the hashed passcode
  return result.hexdigest()





# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
