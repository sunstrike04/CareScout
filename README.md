
# CareScout

CareScout is a full-stack healthcare search application designed to help students and residents in Illinois find nearby hospitals and healthcare facilities that accept their insurance.

The application combines location-based filtering with insurance compatibility checks to help users identify potentially suitable healthcare options.

## Features

- **Insurance-based filtering:** Find hospitals and healthcare facilities based on a user's insurance provider.
- **Location-based recommendations:** Rank healthcare facilities by their distance from a user-provided address.
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

### API Endpoints

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

## Getting Started

### Prerequisites

- Python 3
- Node.js
- npm

### Option 1: Startup Script

Clone the repository:

```bash
git clone https://github.com/sunstrike04/CareScout.git
cd CareScout
```

Run the included startup script:

```bash
chmod +x ./run_carescout.sh
./run_carescout.sh
```

### Option 2: Manual Setup

Start the Flask backend:

```bash
pip3 install flask flask-cors pandas
python3 backend_flask.py
```

In a separate terminal, start the React frontend:

```bash
cd frontend
npm install
npm start
```

The frontend and backend run as separate processes during local development.

Additional dependencies may be required for data processing and address-based distance calculations.

## Engineering Highlights

- Built a full-stack application connecting a React interface with a Python Flask backend.
- Implemented API endpoints for retrieving hospital data and processing user search criteria.
- Combined distance ranking with insurance compatibility filtering.
- Worked with structured healthcare datasets using Python and pandas.
- Developed data collection and processing utilities for hospital and insurance information.

## Motivation

Finding healthcare can be challenging when patients need to consider both proximity and insurance coverage.

CareScout explores how software can make this process easier by combining location-based search with structured insurance information in a single application.

This project is a prototype and should not be used to verify current insurance coverage or make emergency healthcare decisions.
