FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install virtualenv
RUN pip install --no-cache-dir virtualenv

# Create a virtual environment and activate it
RUN python -m virtualenv venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Run main.py when the container launches
CMD ["python", "./main.py"]

