# Choose base image
FROM python:3.10.14-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install necessary build tools and libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    fonts-nanum-coding \
    fonts-nanum-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy necessary files to the container
COPY team_analysis_prototype.py /app
COPY pyproject.toml /app
COPY granduer.csv /app

# Install Poetry and dependencies
RUN pip install --upgrade pip
RUN pip install poetry

# Export dependencies from pyproject.toml to requirements.txt, excluding dev-dependencies
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 to the outside world
EXPOSE 8123

# Define environment variable
ENV STREAMLIT_SERVER_PORT 8123

# Copy Nanum fonts to matplotlib font directory
RUN cp /usr/share/fonts/truetype/nanum/Nanum* /usr/local/lib/python3.10/site-packages/matplotlib/mpl-data/fonts/ttf/ \
    && rm -rf /home/ubuntu/.cache/matplotlib/*

# Run Streamlit when the container launches
CMD ["streamlit", "run", "team_analysis_prototype.py", "--server.port=8123", "--server.address=0.0.0.0"]