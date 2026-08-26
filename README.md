# AI News Aggregator

An AI-powered news aggregation pipeline that collects articles from multiple AI-related sources, extracts article content, generates AI summaries, and produces a concise daily AI news digest.

## Overview

The AI News Aggregator is a Python backend designed to automate the process of keeping up with developments across the AI industry.

The application currently collects news from:

- OpenAI

- Anthropic

- Google AI

Articles are stored in PostgreSQL, their full content is extracted when available, and OpenAI is used to generate concise summaries.

The application then combines the summarized articles into a daily AI news digest and stores the result in PostgreSQL.

## Features

### Article ingestion

- Fetches articles from multiple configured sources.

- Supports RSS-based and web-based fetching.

- Prevents duplicate articles using the article URL.

- Stores article metadata in PostgreSQL.

### Article content extraction

- Fetches the full content of newly ingested articles.

- Uses BeautifulSoup and HTTP requests for web content extraction.

- Handles unavailable pages gracefully.

- Permanently skips articles returning HTTP 404 responses.

- Only attempts content extraction for articles discovered during the current ingestion run.

### AI summarization

- Uses the OpenAI API to generate concise article summaries.

- Stores generated summaries in PostgreSQL.

- Generates summaries only when an article does not already have one.

### Daily AI digest

- Selects articles published after the previous digest.

- Combines their AI-generated summaries.

- Uses an LLM to generate a concise daily digest.

- Includes article titles, summaries, sources, and original URLs.

- Stores generated digests in PostgreSQL.

- Prevents duplicate digests for the same date.

### Safe daily execution

The main application can be run with a single command:

```bash

uv run python -m app.cli


The CLI:

1. Checks whether today’s digest already exists.
2. Fetches new articles from configured sources.
3. Stores newly discovered articles.
4. Fetches content for newly ingested articles.
5. Generates missing AI summaries.
6. Generates the daily digest.
7. Saves the digest to PostgreSQL.

If today’s digest already exists, the application stops without unnecessarily fetching sources or making additional AI API calls.

Architecture
                  ┌─────────────────┐
                  │  News Sources   │
                  │                 │
                  │ OpenAI          │
                  │ Anthropic       │
                  │ Google AI       │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    Fetchers     │
                  │                 │
                  │ RSS / Web       │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   PostgreSQL    │
                  │                 │
                  │ Sources         │
                  │ Articles        │
                  │ Digests         │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Content Fetcher │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   OpenAI API    │
                  │                 │
                  │ AI Summaries    │
                  │ Daily Digest    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Daily Digest   │
                  │   PostgreSQL    │
                  └─────────────────┘


Project Structure

ai-news-aggregator/
│
├── app/
│   ├── agents/
│   │   ├── digest.py
│   │   └── summarizer.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── repositories.py
│   │   └── ...
│   │
│   ├── fetchers/
│   │   ├── anthropic.py
│   │   ├── content.py
│   │   ├── router.py
│   │   ├── rss.py
│   │   └── ...
│   │
│   ├── services/
│   │   ├── daily_digest.py
│   │   ├── fetch_content.py
│   │   ├── generate_summary.py
│   │   └── ingest.py
│   │
│   ├── cli.py
│   └── models.py
│
├── docker/
│   └── docker-compose.yml
│
├── .env
├── .gitignore
├── pyproject.toml
├── README.md
└── uv.lock


Tech Stack

* Python 3.12+
* PostgreSQL 16
* SQLAlchemy
* OpenAI API
* BeautifulSoup
* Requests
* Feedparser
* Pydantic
* uv
* Docker / Docker Compose

Local Setup

1. Clone the repository

git clone <your-repository-url>
cd ai-news-aggregator

2. Install dependencies

This project uses uv.
uv sync

3. Start PostgreSQL
docker compose -f docker/docker-compose.yml up -d

4. Configure environment variables

Create a .env file in the project root:
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql+psycopg://ai_news:ai_news_password@localhost:5432/ai_news
Never commit .env or API keys to GitHub.

5. Create database tables

Run the project’s database table creation script:
uv run python -m app.db.create_tables

6. Run the aggregator
uv run python -m app.cli
The application will fetch new articles, extract content, generate missing summaries, and create the daily digest.

Running the Pipeline Manually

The application is intentionally usable without a continuously running scheduler.

Run:
uv run python -m app.cli

Whenever the command is executed, the application checks whether a digest already exists for the current date.

This makes manual execution the default mode and keeps automated scheduling optional.

Optional Automation

The project is designed so that the same CLI command can later be triggered by a scheduler.

The scheduler does not contain the application logic. It simply executes:
uv run python -m app.cli

This makes scheduled execution optional while keeping the core application independently usable.

Potential deployment options include:

* Docker-based scheduling
* Render scheduled jobs
* Cron
* Other cloud scheduler services

Database

The application uses PostgreSQL with SQLAlchemy.

The main entities are:

Sources

Stores configured news sources.

Articles

Stores:

* Source
* Title
* URL
* Publication date
* Original summary
* Full article content
* AI-generated summary
* Content-fetch status
* Creation timestamp

Digests

Stores:

* Digest date
* Generated digest content
* Creation timestamp

Error Handling

The pipeline includes several safeguards:

* Duplicate URLs are ignored during ingestion.
* HTTP 404 content pages are marked as permanently unavailable.
* Temporary content-fetch failures can be retried.
* Missing article content does not crash the entire pipeline.
* Missing AI summaries are generated only when required.
* Duplicate daily digests are prevented.
* Running the CLI multiple times on the same day does not repeatedly fetch sources or call the LLM once today’s digest already exists.

Example Workflow

Run application
      │
      ▼
Check today's digest
      │
      ├── Already exists ──► Stop
      │
      ▼
Fetch configured sources
      │
      ▼
Insert new articles
      │
      ▼
Fetch article content
      │
      ▼
Generate missing AI summaries
      │
      ▼
Generate daily digest
      │
      ▼
Save digest to PostgreSQL

Current Status

The core backend pipeline is implemented and tested end-to-end.

Completed:

* Multi-source article ingestion
* RSS and web fetching
* PostgreSQL persistence
* SQLAlchemy models and repositories
* Article deduplication
* Article content extraction
* Content-fetch failure handling
* OpenAI article summarization
* Daily digest generation
* Digest persistence
* Duplicate-digest protection
* Single-command application workflow
* Optional automation architecture

Future Improvements

Planned improvements include:

* YouTube channel ingestion
* Additional AI news sources
* Email delivery of daily digests
* Web interface for browsing articles and digests
* API endpoints
* Automated scheduled deployment
* Cloud deployment
* Improved monitoring and logging
* Automated test suite
* User-specific digest preferences

Project Goal

The long-term goal is to turn the pipeline into a configurable AI news intelligence system where users can define the sources and topics they care about and receive a concise, personalized digest instead of manually checking dozens of AI news sources every day.