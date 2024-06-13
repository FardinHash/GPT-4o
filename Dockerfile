# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for voice processing
RUN pip install edge-tts nemo_toolkit transformers huggingface_hub

# Expose port 7860 for Gradio
EXPOSE 7860

# Define environment variable to avoid Python buffering
ENV PYTHONUNBUFFERED=1

# Set the entry point for the container to run any script
ENTRYPOINT ["python", "app.py"]