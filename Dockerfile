# Use an official lightweight Python image.
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (curl for downloading tectonic, etc.)
RUN apt-get update && apt-get install -y \
    curl \
    libfontconfig1 \
    libgraphite2-dev \
    libharfbuzz-dev \
    libicu-dev \
    libssl-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Tectonic (modern LaTeX engine)
RUN curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh \
    && mv tectonic /usr/local/bin/

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# removing playwright if not needed to save space/time, but keeping it if unsure.
# If playwright is needed, we need "playwright install deps" which is heavy. 
# Assuming it's NOT needed based on analysis, but installing requirements generic.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend_server:app", "--host", "0.0.0.0", "--port", "8000"]
