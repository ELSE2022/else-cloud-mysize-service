# Dockerfile
# FROM directive instructing base image to build upon
FROM python:3.6
# EXPOSE port 5000 to allow communication to/from server
EXPOSE 5000
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
#ENTRYPOINT ["python"]
#CMD ["start.sh"]
