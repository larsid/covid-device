# COVID Device Simulator

## Overview

This repository contains a lightweight Python service that simulates an IoT device streaming patient vitals to a remote COVID-19 monitoring platform. The simulator repeatedly generates random vital signs, registers itself with the remote API, and keeps the server up to date until the process exits.

The project is helpful for:

- Testing remote monitoring back ends without deploying real hardware.
- Demonstrating how a medical IoT device might communicate with a REST API.
- Validating Docker-based deployment pipelines via the included GitHub Actions workflow.

## How it works

The core logic lives in [`device.py`](device.py). When launched, the script:

1. Creates a unique identifier for the simulated device (either from the `UID` environment variable or a randomly generated UUID).
2. Connects to the configured API base URL (default `http://localhost:8000`).
3. Registers the device by POSTing generated vital-sign data to `/users` and storing the returned numeric identifier.
4. Enters a loop where it periodically updates the user record with new vitals via PUT requests to `/users/{id}`.
5. Attempts to delete the user (`DELETE /users/{id}`) if the process encounters an unhandled exception.

### Generated vital signs

Every update transmits a JSON payload with the following fields:

- `name`: Identifier of the device instance.
- `temperature`: Random body temperature between 35.0 °C and 39.0 °C.
- `heart_rate`: Integer beats-per-minute ranging from 0 to 119.
- `blood_pressure`: Integer systolic pressure between 5 and 129 mmHg.
- `respiratory_rate`: Integer breaths-per-minute between 5 and 29.

The timing between updates is randomized to mimic irregular reporting intervals (2–5 seconds).

## Getting started

### Prerequisites

- Python 3.9 or newer
- [`pip`](https://pip.pypa.io/) for dependency management

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **Note:** The current `requirements.txt` lists [`httpx`](https://www.python-httpx.org/), the HTTP client used for API calls.

### Running the simulator

```bash
python device.py
```

Optional environment variables:

- `URL`: Base URL of the monitoring API (default `http://localhost:8000`).
- `UID`: Explicit identifier for the device. If omitted, a random UUID is used.

The simulator will continue running until interrupted (Ctrl+C), periodically sending updated vitals to the remote server.

## Docker support

A `Dockerfile` is included to containerize the simulator. Build and run it with:

```bash
docker build -t covid-device .
docker run --rm -e URL="http://your-api:8000" covid-device
```

The repository also provides a GitHub Actions workflow (`.github/workflows/docker-image.yml`) that builds and pushes the Docker image to Docker Hub whenever a version tag (`v*.*.*`) is pushed.

## Contributing

1. Fork the repository and create a feature branch.
2. Make your changes and add tests or documentation updates as needed.
3. Ensure the simulator runs locally or inside Docker.
4. Open a pull request describing your changes.

Feel free to file issues for questions, feature requests, or bug reports.

## License

Specify the license that applies to the project (e.g., MIT, Apache 2.0). Update this section when a license is chosen.
