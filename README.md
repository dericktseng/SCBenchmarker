# SCBenchmarker
You know you suck. But you don't know *how* much you suck. Introducing SCBenchmarker, a program to effectively tell you not only *how* much you suck, but also *where* you suck. See how much you botched a professional build, and where you can improve!

## Usage:
* Install required libraries (Installation in section below)
* Modify `src/config.py`. Recommended settings (all others remaining default):
    * `FLASK_ENV="production"`
    * `DEBUG=False`
    * `TESTING=False`
    * `SERVER_NAME=` As you see fit
* `python3 SCBenchmarker.py` OR `python3 src/server.py`
    * Alternate entry point in `src/server.py` is preferred as a convenience for uwsgi server setup.

## Installation:
`pip install -r requirements.txt`

Requirements:
* Python3 and pip
* Flask (and dependencies)
* zephyrus_sc2_parser (and dependencies)
