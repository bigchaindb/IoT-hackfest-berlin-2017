FROM python:3.5
RUN mkdir /lt
COPY ui/ /lt
ENTRYPOINT ["python3"]
CMD ["-m", "http.server", "8002"]
