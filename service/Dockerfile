FROM python:latest
WORKDIR /scripts
COPY receiveCSV.py /scripts/
COPY requirements.txt /scripts/
COPY csvprocessorsql.py /scripts/
RUN pip install -r /scripts/requirements.txt
USER 1001
EXPOSE 5000
CMD python receiveCSV.py