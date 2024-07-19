FROM python:3.9-buster

WORKDIR /usr/src/app

# Copy the application code into the container
COPY . .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command can be overridden by docker-compose
CMD [ "python3", "-m" , "flask", "run"]