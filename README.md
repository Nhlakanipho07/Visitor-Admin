# Visitor Admin

## How to setup mongo_visitor_admin.

### 1. Start by cloning the repo:

- run ```git clone git@github.com:Nhlakanipho07/Visitor-Admin.git```

  in a linux terminal / git bash for Windows.

### 2. Navigate to the project directory:

- Open a code editor and navigate to **Visitor-Admin**.

### 3. How to set the environment variable:

- Create a `.env` file in the root directory of this repository.
- Inside this file, fill it in with:
    
    ```
    MONGODB_URI="mongodb://username:password@localhost:27017"
    MONGO_INITDB_ROOT_USERNAME=username
    MONGO_INITDB_ROOT_PASSWORD=password
    ```
- Replace `password` with a desired password, and likewise with `username`.
- Close the file.


### 4. Set up a Docker container:

- Install Docker from the Docker website if not already installed.
- Install Docker Desktop if not already installed.
- Open a terminal and navigate to **Visitor-Admin**:
    - Open `Docker Desktop`
    - Run `docker compose up -d`
    - This should pull the mongo image 4.4
- Once complete, run `docker ps` to see if `mongodb_container` is running.
- If `mongodb_container` is running then the container is setup correctly.

### 5. Set up a virtual environment:

- Create a virtual environment by running:
    - ``python -m venv <env>`` in Windows terminal.
    - ``python3 -m venv <env>`` in macOS/Linux terminal.

- Activate the virtual environment:
  - On Windows, run ``<env>\Scripts\activate`` in the terminal.
  - On macOS/Linux, run ``source <env>/bin/activate`` in the terminal.

### 6. Install mongo_visitor_admin:

- Run ``pip install .`` to install the package.
- Run ``pip install -r requirements.txt`` to install all the dependencies listed in ``requirements.txt``.
- To verify that all the dependencies are installed properly, run ``pip freeze``
- Ensure that the recommended python interpreter is selected.


## How to use mongo_visitor_admin:

- Navigate to `visitor_admin/main.py`.
- Inside `main.py`:
  - `create_visitor_indexes()` has to be called first to create indexes prior to using any CRUD operations.
  - From the imported functions, under `create_visitor_indexes()`, call any function one wishes to use with its respective argument values.
  - To see what arguments a function requires, open `visitor_admin/visitor_index.py`, and look for the function one wants to call.


## How to run tests:

- In the terminal:
  - Stop `mongodb_container` by running `docker compose down`.

  - To run all tests:

    - On Windows: 
        - `python -m unittest tests/test_mongodb_connection_manager.py`
        - `python -m unittest tests/test_visitor_index.py`

    - On Linux: 
        - `python3 -m unittest tests/test_mongodb_connection_manager.py`
        - `python3 -m unittest tests/test_visitor_index.py`

  - To run a specific test:

    - On Windows: 
        - `python -m unittest tests.test_mongodb_connection_manager.TestMongoDBConnectionManager.<test_method_name>`
        - `python -m unittest tests.test_visitor_index.TestVisitorIndex.<test_method_name>`

    - On Linux: 
        - `python3 -m unittest tests.test_mongodb_connection_manager.TestMongoDBConnectionManager.<test_method_name>`
        - `python3 -m unittest tests.test_visitor_index.TestVisitorIndex.<test_method_name>`

  *Note: replace `<test_method_name>` with a test method name of the specific test method found in `test_mongodb_connection_manager.py` or `test_visitor_index.py` respectively*

## Deactivate virtual environment:

- Run ``deactivate`` in the terminal.
