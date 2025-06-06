# Set the OpenMPI base image
FROM ubuntu:22.04

# Install required dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libopenmpi-dev \
    openmpi-bin \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m mpiuser && \
    mkdir /app && \
    chown mpiuser:mpiuser /app

# Copy the requirements.txt file into the container
COPY requirements.txt /tmp/requirements.txt

# Install Python packages from requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt 

# Switch to the non-root user
USER mpiuser

# Set the working directory
WORKDIR /app

# Copy the application files
COPY --chown=mpiuser:mpiuser . .

# Run the application using mpirun
CMD ["mpirun", "--hostfile", "hosts", "-np", "6", "python3", "ml_service.py"]