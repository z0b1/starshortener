# Star Shortener
Star Shortener is a simple URL shortener, it uses FastAPI connected to a Neon serverless Postgres database and makes unique short id's.

## Hero

![Demo GIF](/public/assets/demo.gif)

### Try it [here](https://urs.z0b1.tech/)

## Features
- No(minimal) CSS UI
- FastAPI
- Serverless Postgres
- Unique short ID's for each URL

## How to run locally

1. Clone repo `git clone https://github.com/z0b1/starshortener.git`
2. cd into the repo `cd starshortener`
3. Create a local .env file with this format `DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE?schema=public&sslmode=require"`
> Make sure to put .env in the .gitignore. NEVER SHARE YOUR .env FILES
4. Make a virtual enviorment `python -m venv .venv`/`python3 -m venv .venv` and activate it `.venv\Scripts\activate.bat`/`.venv\Scripts\Activate.ps1`/`source .venv/bin/activate`
5. Run the FastAPI server `uvicorn api.index:app --reload`
6. Open your browser at `http://127.0.0.1:8000` and enjoy!
7. When finished with running locally you can deactivate the venv with `deactivate`

## How it works 

To achieve maximum speed at minimum cost&trade;, this shortener is built as a stateless micro-app using FastAPI and an async Prisma ORM client deployed on Vercels serverless infra. While a subdomain based routing system was considered for aesthetics, I didnt want all the DNS wildcard trouble and complex multi domain SSL provisioning. To prevent stateless function spikes from crushing database connection limits, the app targets a connection pooled Neon PostgreSQL proxy handled inside a clean FastAPI context lifespan, keeping redirect lookups fast, non-blocking, and isolated under high concurrency.

## Credits

[FastAPI](https://fastapi.tiangolo.com/)
[Jinja2](https://jinja.palletsprojects.com/en/stable/)


