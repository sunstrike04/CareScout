
# CareScout

CareScout is a full-stack healthcare search application designed to help students and residents in Illinois find nearby hospitals and healthcare facilities based on location and insurance compatibility.

Developed as a team project, CareScout combines location-based search with healthcare and insurance data to help users explore potentially suitable healthcare options.

## Features

- **Insurance-based filtering:** Find hospitals and healthcare facilities based on a user's insurance provider.
- **Location-based recommendations:** Rank healthcare facilities by distance from a user-provided address.
- **Hospital data processing:** Work with structured hospital and insurance information.
- **Interactive web interface:** Submit search criteria and view matching facilities.
- **Backend API:** Process search requests through a Python Flask server.

## Tech Stack

- **Frontend:** React, JavaScript, HTML, CSS
- **Backend:** Python, Flask, Flask-CORS
- **Data Processing:** pandas
- **Data Storage:** CSV and serialized datasets
- **Other:** REST-style API endpoints, Git

## Project Structure

```text
CareScout/
├── frontend/                  # React frontend
├── backend/                   # Additional backend components
├── backend_flask.py           # Flask API
├── distance_filter.py         # Distance ranking and insurance filtering
├── hospitaldatabase.py        # Hospital data processing
├── insurance_scraper.py       # Insurance data collection
├── scraper.py                 # Data collection utilities
├── insurances_csv.py          # Insurance data processing
├── run_carescout.sh           # Application startup script
└── README.md
```

## How It Works

CareScout connects a React frontend to a Flask backend that processes healthcare search requests.

1. **User input:** The user provides an address and insurance provider.
2. **API request:** The frontend sends the information to the Flask backend.
3. **Distance ranking:** The backend ranks hospitals based on their distance from the supplied address.
4. **Insurance filtering:** The application filters the ranked facilities according to insurance compatibility.
5. **Results:** Matching facilities are returned to the frontend for display.

The backend uses pandas to work with hospital and insurance datasets.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/data` | GET | Returns the loaded hospital dataset as JSON |
| `/filter` | POST | Accepts an address and insurance provider, then returns filtered hospital results |

Example request to `/filter`:

```json
{
  "userInfo": [
    "Champaign, IL",
    "Example Insurance Provider"
  ]
}
```

The backend expects two values: a user address and an insurance provider.

## Technical Highlights

- Full-stack application connecting a React frontend with a Python Flask backend.
- API endpoints for retrieving hospital data and processing user search criteria.
- Distance-based ranking combined with insurance compatibility filtering.
- Structured healthcare data processing using Python and pandas.
- Python utilities for collecting and processing hospital and insurance information.

## Motivation

Finding healthcare can be challenging when patients need to consider both proximity and insurance coverage.

CareScout explores how software can make this process easier by combining location-based search with structured insurance information in a single application.

This project is a prototype and should not be used to verify current insurance coverage or make emergency healthcare decisions.
