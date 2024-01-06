# Poker d/App Python Backend

## About The Project

Python backend for NYU Blockchain and Fintech Club's Poker d/App

## Pre-requisites

Project Dependencies

- [Docker](https://docs.docker.com/engine/install/)
- [Poetry](https://pypi.org/project/poetry/)

## Getting Started

1. Clone the repo

   ```sh
   git clone https://github.com/nyublockchainfintech/poker_dapp_backend
   ```

2. Install dependencies
   ```sh
   poetry install
   ```
3. Start Development Web Server

   Local Deployment

   ```sh
   uvicorn poker_dapp_backend.server.main:app --reload # Runs on port 8000
   ```

   Docker Deployment

   ```sh
   docker compose up --build -d
   ```

4. Run Tests

   ```sh
   pytest -v
   ```

## Useful Commands for Development

- Build Docker Image

  ```sh
  docker build .
  ```

- Fresh Rebuild

  ```sh
  docker compose build --no-cache
  docker compose up -d --build
  ```

- Setup Python virtual environment with Poetry

  ```sh
   poetry config virtualenvs.in-project true # Make poetry use local .venv folder
   poetry install # Install dependencies
   source .venv/bin/activate # Activate virtual environment in zsh
   source .venv/bin/activate.[fish|csh] # For other shell types
  ```

- Save dependencies to requirements.txt

  ```sh
  poetry export --without-hashes --format=requirements.txt > requirements.txt
  ```
