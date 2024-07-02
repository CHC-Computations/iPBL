Code repository for iPBL project funded by the NPRH programme


# CSV to RDF converter Documentation


## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [API Endpoints](#api-endpoints)
5. [Directory Structure](#directory-structure)
6. [License](#license)

## Installation

To run this application locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/CHC-Computations/iPBL.git
    cd csv-to-rdf-api
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```bash
    python app.py
    ```

The application will be available at `http://127.0.0.1:5000/`.

## Configuration

The configuration for upload and output directories is set in the `config.py` file:

```python
# config.py
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
```

You can change these paths according to your preferences.

## Usage

### Web Interface

1. **Upload a CSV File:**
   - Navigate to the homepage at `http://127.0.0.1:5000/`.
   - Use the file upload form to select and upload a CSV file.
   - Select the desired RDF format (e.g., XML, Turtle).

2. **Documentation:**
   - Access the API documentation at `http://127.0.0.1:5000/documentation`.

### API Endpoints

1. **Upload CSV and Convert to RDF:**
   - Endpoint: `/api/upload`
   - Method: `POST`
   - Parameters:
     - `file`: The CSV file to be uploaded.
     - `format`: The desired RDF format (e.g., `xml`, `turtle`).
     - `display`: Optional. If included, the response will include the RDF content.
   - Example request using `curl`:
     ```bash
     curl -X POST -F "file=@path/to/your/file.csv" -F "format=turtle" http://127.0.0.1:5000/api/upload
     ```

2. **Download RDF File:**
   - Endpoint: `/download/<filename>`
   - Method: `GET`
   - Description: Download the converted RDF file.
   - Example URL: `http://127.0.0.1:5000/download/output.turtle`

## Directory Structure

The project structure is organized as follows:

```
csv-to-rdf-api/
│
├── app.py
├── config.py
├── api/
│   ├── __init__.py
│   └── routes.py
├── rdf/
│   ├── __init__.py
│   └── builder.py
├── templates/
│   ├── upload.html
│   └── documentation.html
└── static/
    └── swagger.json
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
