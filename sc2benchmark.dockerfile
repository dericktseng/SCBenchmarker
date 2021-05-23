FROM python:3.8.5
RUN git clone https://github.com/MetriC-DT/SCBenchmarker.git
WORKDIR SCBenchmarker
RUN pip install -r requirements.txt
CMD [ "python3", "SCBenchmarker.py" ]
