# Use an official Python runtime as a parent image
FROM python:3.6.4-stretch

# Set the working directory to /app
RUN mkdir /flask_service
WORKDIR /flask_service

# Install any needed packages specified in requirements.txt
ADD flask_service/requirements.txt /flask_service
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
ADD ./flask_service /flask_service

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
# add package to python's path
ENV PYTHONPATH $PYTHONPATH:/flask_service

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8


# Run app.py when the container launches
CMD ["python", "run_app.py"]



