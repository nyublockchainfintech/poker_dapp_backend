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

## References

Communative Encryption

- [Cryptography Fundamentals: Commutative Encryption](https://billatnapier.medium.com/cryptography-fundamentals-commutative-encryption-19ba4c4c2173#:~:text=With%20commutative%20encryption%2C%20we%20can,can%20decrypt%20in%20any%20order.)
- [Commutative Encryption with SHAKE-128/SHAKE-256 and Python](https://asecuritysite.com/commul/comm_stream)

Mental Pokeer

- [Mental Poker Wiki](https://en.wikipedia.org/wiki/Mental_poker)
- [Fast Mental Poker Protocol](https://eprint.iacr.org/2009/439.pdf)
- [Mental Poker Github](https://github.com/zachratliff/mental-poker)

Game State

- When a player cashes out of the game, the player calls the smart contract
  from the client side. They send a signed snapshot (signed by everyone) of the
  last valid game balances
- I have to track the game state separately
