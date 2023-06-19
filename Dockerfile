FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file
COPY src/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
#COPY . .
COPY /src .
COPY .env .

# Expose the port on which your FastAPI application runs
EXPOSE 8000

# Start the application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
