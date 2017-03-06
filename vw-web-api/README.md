# VW Front-End API

This script runs the Front-End API for the VW use case.

You can use the included Dockerfile to run it:

```
docker build -t vw-web-api:latest .
docker run --rm -it -p 5000:5000 vw-web-api
```

Test it with the following request:

```
http//WEBSITE_HOST:5000/trips/001
```
