# TFG-Server

TFG-Server is the backend system for an intelligent route recommendation service for Electric Vehicles (EVs). Its primary goal is to process routing requests from EV users and recommend optimal charging stations based on current battery levels, distance, charging times, and energy prices.

## Project Structure

```
├── data/                 # Raw data files (OSM, JSONs) and analysis notebooks
├── logs/                 # System logs
├── src/
│   ├── Domain/           # Business logic, entities, and controllers
│   ├── Persistence/      # Database and API clients
│   ├── Presentation/     # MQTT communication layer
│   └── Utils/            # Logging and constants
├── main.py               # Application entry point
├── pyproject.toml        # Project dependencies and configuration
└── dbcreation.sql        # Database schema definition
```

## Setup environment

### Using `uv` (recommended)

```bash
uv sync
```

### Using `pip`

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate in Windows
pip install -e .
```

### .env

Create a `.env` file in the root directory with the following content:

```
# MQTT configuration
MQTT_BROKER_HOST =
MQTT_BROKER_PORT =
MQTT_MAX_WORKERS =

MQTT_USER =
MQTT_PASSWORD =
MQTT_CLIENT_ID =

# MySQL / MariaDB configuration
DB_HOST =
DB_PORT =
DB_NAME =
DB_USER =
DB_PASSWORD =

# Other configurations
# LOG_LEVEL = "DEBUG"


# OpenChargeMap API key for data downloading
OCM_API_KEY =
```

## Setup database

> The recommended version of MariaDB is 10.5 due to known [bugs](https://jira.mariadb.org/browse/MDEV-26123).

Firstly, the schema must be created by running the `dbcreation.sql` script in your MariaDB instance.

In the folder `data/` there are jupyter notebooks that can be used to populate the database with the necessary data for testing and development.

## Program Architecture

The program follows a clean, layered architecture to separate concerns:

### 1. Presentation Layer (`src/Presentation/`)

**MQTT Listener**: Acts as the external interface. It listens for routing requests on the `vehicles/requests` topic and publishes the calculated charging options back to the vehicles. It uses a `ThreadPoolExecutor` to handle multiple requests concurrently.

### 2. Domain Layer (`src/Domain/`)

Contains business logic and core entities:

- **Entities**: Pydantic models for `EVUser`, `Vehicle`, `ChargingStation`, `Charger`, `Service`, `Request`, and `Option`.
- **DAOs (Data Access Objects)**: Provide a clean interface for the domain layer to interact with the persistence layer without knowing the underlying database implementation. Improves decoupling and testability.
- **Controllers**:
  - `ControlRequests`: The main orchestrator that validates requests and calculates the best charging options.
  - `ControlRoute`: Handles route geometry, distances, and durations using a local OSRM (Open Source Routing Machine) server.
  - `ControlPrice`: Fetches hourly energy prices from the REE (Red Eléctrica Española) API to estimate charging costs.

### 3. Persistence Layer (`src/Persistence/`)

- **DB Broker**: A Singleton that manages the connection pool to the database (MariaDB), ensuring efficient resource usage.
- **Web Client**: Handles external HTTP requests (e.g., to the REE API).

### 4. Utils Layer (`src/Utils/`)

Contains a centralized logging configuration (`logger.py`) and global constants (`constants.py`).

## Execution

To start the server, simply run:

```bash
uv run main.py
```

`LOG_LEVEL` can be modified

---

*Developed by Daniel Sánchez Castro for TFG 2026.*
