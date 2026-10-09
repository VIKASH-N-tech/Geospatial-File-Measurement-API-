# Geospatial-File-Measurement-API-
Geospatial File Measurement API is a Python FastAPI-based backend that accepts Shapefile ZIP and KML files, extracts geographic features, and calculates polygon areas and line lengths. It handles coordinate reference systems (CRS), validates uploads, provides structured JSON responses, and offers REST endpoints for file information and measurement results.
# Geospatial File Measurement API

A Python-based REST API built with FastAPI to upload and process geospatial files in Shapefile ZIP and KML formats. It extracts geographic features and calculates polygon areas and line lengths while handling Coordinate Reference Systems (CRS) correctly.

## Features

* Upload Shapefile (`.zip`) and KML (`.kml`) files.
* Extract feature IDs, geometry types, coordinates, CRS, and attributes.
* Calculate polygon area in square metres and hectares.
* Calculate line length in metres and kilometres.
* Transform geographic coordinates into an appropriate projected CRS before measurement.
* Retrieve file information and measurement results through REST API endpoints.
* Validate uploaded files and handle errors gracefully.
* Interactive API documentation using Swagger UI.

## Technology Stack

* Python
* FastAPI
* GeoPandas
* Shapely
* PyProj
* Fiona
* Pydantic
* Pytest

## Project Structure

```text
geospatial-file-measurement-api/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   ├── file_service.py
│   │   ├── geometry_service.py
│   │   ├── measurement_service.py
│   │   └── crs_service.py
│   ├── schemas/
│   │   ├── file_schema.py
│   │   └── measurement_schema.py
│   └── storage/
│       └── metadata_store.py
├── uploads/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

*Note: Adjust the structure to match the files actually present in your repository.*

## Setup Instructions

### Prerequisites

Install the following software:

* Python 3.11 or later
* Git
* Visual Studio Code (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/geospatial-file-measurement-api.git
cd geospatial-file-measurement-api
```

Replace `YOUR-USERNAME` with your GitHub username and use your actual repository URL.

### Step 2: Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux or macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Ensure that `requirements.txt` contains all the dependencies used by your project.

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you have not created `requirements.txt` yet, include the required packages such as FastAPI, Uvicorn, GeoPandas, Shapely, PyProj, Fiona, python-multipart, and Pytest. Pin compatible versions after testing your environment.

### Step 4: Configure the Project

Create the required upload and storage directories if they do not already exist.

```bash
mkdir uploads
```

If your application uses environment variables, create a `.env` file using `.env.example` as a template.

Do not commit secrets, private credentials, or sensitive uploaded files to GitHub.

### Step 5: Run the Application

If your FastAPI application instance is named `app` in `app/main.py`, execute:

```bash
uvicorn app.main:app --reload
```

If your entry point is different, replace `app.main:app` with the correct Python module and application instance.

The application will usually be available at:

* API base URL: `http://127.0.0.1:8000`
* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Endpoint                        | Description                          |
| ------ | ------------------------------- | ------------------------------------ |
| GET    | `/health`                       | Check API status                     |
| POST   | `/api/files/`                   | Upload and process a geospatial file |
| GET    | `/api/files/{id}/`              | Retrieve file information            |
| GET    | `/api/files/{id}/measurements/` | Retrieve feature measurements        |

The endpoints above describe the intended API. Confirm that each route is implemented in your application.

## How to Use the API

### Upload a File

Send a POST request to:

```text
/api/files/
```

Use `multipart/form-data` with a file field named `file` if that is the field defined by your endpoint.

Example using curl:

```bash
curl -X POST "http://127.0.0.1:8000/api/files/" -F "file=@survey.kml"
```

For a Shapefile, upload a ZIP archive containing the required Shapefile components.

### Retrieve File Information

```text
GET /api/files/{id}/
```

Replace `{id}` with the ID returned by the upload endpoint.

### Retrieve Measurements

```text
GET /api/files/{id}/measurements/
```

The response should include supported measurements, feature attributes, geometry types, and CRS information according to your implementation.

## Measurement and CRS Handling

* Polygon geometries are measured by area.
* LineString geometries are measured by length.
* Point geometries do not require measurements.
* Geographic coordinates such as EPSG:4326 must be transformed into an appropriate projected coordinate system before calculating planar area or length.
* Missing CRS information and unsupported geometries should be handled explicitly.

Measurement accuracy depends on the source data, geometry validity, and the selected projected CRS.

## Running Tests

Activate your virtual environment and run:

```bash
pytest
```

Add tests for file uploads, polygon area, line length, CRS transformations, invalid files, and unsupported geometries.

## Troubleshooting

**ModuleNotFoundError**

Ensure your virtual environment is activated and dependencies are installed.

**File upload errors**

Check the accepted file extensions, multipart field name, file size limits, and file contents.

**CRS or measurement errors**

Verify the source CRS and ensure the geometry is transformed rather than merely relabelled.

**Application fails to start**

Confirm that the module path and FastAPI application variable match your project.

## Learning Outcomes

* Building REST APIs using FastAPI.
* Processing geospatial files with Python.
* Working with coordinate reference systems.
* Calculating geometric measurements.
* Validating file uploads and handling errors.
* Writing automated tests and documenting APIs.

## Future Enhancements

* Add a web-based interface for uploading and visualizing files.
* Support additional geospatial formats.
* Add asynchronous processing for large files.
* Implement persistent storage and processing history.
* Add map previews and downloadable measurement reports.
* Improve CRS selection and measurement validation.

## License

Choose a suitable open-source license, such as the MIT License, and add a `LICENSE` file if you intend to distribute the project under that license.

## Author

**VIKASH**

GitHub: `https://github.com/YOUR-USERNAME`
