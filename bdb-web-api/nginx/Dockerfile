###########################################################################
# Dockerfile for nginx to receive requests on port 80 and route it to the #
# appropriate backend based on the URL for the PoC demo                   #
###########################################################################

FROM nginx:alpine
MAINTAINER "dev@bigchaindb.com"
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
