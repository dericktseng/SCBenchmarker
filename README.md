# SCBenchmarker
You know you suck. But you don't know *how* much you suck. Introducing SCBenchmarker, a program to effectively tell you not only *how* much you suck, but also *where* you suck. See how much you botched a professional build, and where you can improve!

## Usage:
* Install required libraries (Installation in section below)
* Modify `src/config.py`. Recommended settings (all others remaining default):
    * `FLASK_ENV="production"`
    * `DEBUG=False`
    * `TESTING=False`
    * `SERVER_NAME=127.0.0.1:9999`
* `python3 SCBenchmarker.py`
* A `systemctl` unit file is provided, as well as a basic `uwsgi.ini` for quick hosting setup.

## Installation:
`pip install -r requirements.txt`

Requirements:
* Python3 and pip
* Flask (and dependencies)
* zephyrus\_sc2\_parser (and dependencies)
