# Use minimal Python 3.13 base image (Alpine = very small footprint)
FROM python:3.13-alpine

# Set working directory inside the container
WORKDIR /app

# Copy requirements file from host and rename it to requirements.txt
COPY requirements.ps_sim.txt requirements.txt

# Install Python dependencies without caching to keep image small
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy application source code into the container
COPY src/powerstation_simulator/ src/

# Default command: run the main Python entrypoint
CMD ["sh", "-c", "python src/main.py"]
