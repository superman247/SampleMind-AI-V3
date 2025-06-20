# This is a sample Dockerfile for your Cursor environment.
# You can customize it to install any tools or packages you need.

# We'll use a stable version of Ubuntu as our base image.
FROM ubuntu:22.04

# Set DEBIAN_FRONTEND to noninteractive to avoid prompts during package installation.
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install some common development tools.
# - git: for version control
# - curl & wget: for downloading files
# - python3 & python3-pip: for running Python code
# - build-essential: for compiling C/C++ code, which many packages depend on
RUN apt-get update && apt-get install -y \
  git \
  curl \
  wget \
  python3 \
  python3-pip \
  build-essential \
  # Clean up the apt cache to reduce the image size.
  && rm -rf /var/lib/apt/lists/*

# --- CUSTOMIZATION EXAMPLES ---
# You can add your own commands below to customize the environment.

# Example: Install Node.js and npm (using NodeSource for a recent version)
# RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
# RUN apt-get install -y nodejs

# Example: Install other Python packages using pip
# RUN pip3 install numpy pandas scikit-learn

# Create a non-root user. This is a security best practice.
RUN useradd -ms /bin/bash agent

# Switch to the new user.
USER agent

# Set the working directory to the user's home.
WORKDIR /home/agent
