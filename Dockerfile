# Setup environment
FROM python:3.10-slim

# Developer configuration settings
ENV ASSEMBLIT_ENV "PROD"
ENV ASSEMBLIT_VERSION "main"
ENV ASSEMBLIT_DEBUG False

# Web-app configuration settings
ENV ASSEMBLIT_NAME "assemblit"
ENV ASSEMBLIT_HOME_PAGE_NAME "app"
ENV ASSEMBLIT_GITHUB_REPOSITORY_URL "https://github.com/thomaseleff/assemblit"
ENV ASSEMBLIT_GITHUB_BRANCH_NAME "main"

# Port configuration settings
ENV ASSEMBLIT_CLIENT_PORT 8501
ENV PORT ${ASSEMBLIT_CLIENT_PORT}

# Database configuration settings
ENV ASSEMBLIT_DIR "/${ASSEMBLIT_NAME}"

# Set the working directory (cannot be the root directory for Streamlit)
WORKDIR "/${ASSEMBLIT_NAME}"

# Update and install
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    nano \
    git --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip

# Clone from Github
RUN git clone --branch ${ASSEMBLIT_GITHUB_BRANCH_NAME} "${ASSEMBLIT_GITHUB_REPOSITORY_URL}.git" .

# Build and install from the working directory
RUN pip3 install -e .

# Expose the network port(s)
EXPOSE ${ASSEMBLIT_CLIENT_PORT}

# Run
CMD assemblit run ${ASSEMBLIT_HOME_PAGE_NAME}.py
