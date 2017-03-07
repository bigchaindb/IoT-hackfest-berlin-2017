FROM python:3.5
RUN mkdir /vw
COPY ui/ /vw
ENTRYPOINT ["python3"]
CMD ["-m", "http.server", "8001"]
