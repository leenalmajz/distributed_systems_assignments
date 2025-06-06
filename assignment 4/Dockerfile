# Set the OpenMPI base image
FROM ubuntu:22.04

# Install required dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libopenmpi-dev \
    openmpi-bin \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt /tmp/requirements.txt

# Install Python packages from requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt 

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Set the entrypoint to run mpirun
ENTRYPOINT ["mpirun"]