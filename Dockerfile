FROM python:3.8-slim-buster
WORKDIR /chatops
COPY . .
RUN chmod +x script.sh
CMD cd /chatops && ./script.sh
