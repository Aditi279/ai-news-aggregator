# AI News Aggregator

An AI-powered news aggregation pipeline that collects articles from multiple AI-related sources, extracts article content, generates AI summaries, and produces a concise daily AI news digest.

## Overview

The AI News Aggregator is a Python backend designed to automate the process of keeping up with developments across the AI industry.

The application currently collects news from:

- OpenAI
- Anthropic
- Google AI

Articles are stored in PostgreSQL, their full content is extracted when available, and the OpenAI API is used to generate concise summaries.

The application then combines the summarized articles into a daily AI news digest and stores the result in PostgreSQL.

## Architecture

```
News Sources
    |
    +-- OpenAI
    +-- Anthropic
    +-- Google AI
    |
    v
Fetchers
    |
    +-- RSS
    +-- Web
    |
    v
PostgreSQL / Supabase
    |
    +-- Sources
    +-- Articles
    +-- Digests
    |
    v
Content Fetcher
    |
    v
OpenAI API
    |
    +-- Article summaries
    +-- Daily digest
    |
    v
Daily AI News Digest
    |
    v
Stored in PostgreSQL
```



## Features



### Article ingestion

- Fetches articles from multiple configured sources.
- Supports RSS-based and web-based fetching.
- Prevents duplicate articles using the article URL.
- Stores article metadata in PostgreSQL.
- Handles source-level ingestion failures without stopping the entire pipeline.



### Article content extraction

- Fetches full article content for newly discovered articles.
- Uses BeautifulSoup and HTTP requests for web content extraction.
- Handles unavailable pages gracefully.
- Permanently skips articles returning HTTP 404 responses.
- Allows temporary failures to be retried.
- Only attempts content extraction for articles discovered during the current ingestion run.



### AI summarization

- Uses the OpenAI API to generate concise article summaries.
- Stores generated summaries in PostgreSQL.
- Generates summaries only when an article does not already have one.
- Handles individual summarization failures without crashing the entire pipeline.



### Daily AI digest

- Selects articles published after the previous digest.
- Generates missing article summaries.
- Combines summarized articles into a concise daily digest.
- Uses an LLM to rank and summarize the most important developments.
- Includes article titles, summaries, sources, and original URLs.
- Stores generated digests in PostgreSQL.
- Prevents duplicate digests for the same date.



### Safe execution

The main application can be run with:

```
uv run python -m app.cli
```

The CLI:

1. Checks whether today's digest already exists.
2. Fetches new articles from configured sources.
3. Stores newly discovered articles.
4. Fetches content for newly ingested articles.
5. Generates missing AI summaries.
6. Generates the daily digest.
7. Saves the digest to PostgreSQL.

If today's digest already exists, the application stops without unnecessarily making additional AI API calls.

## Deployment

The project has been tested running in a cloud environment using:

- GitHub Actions
- Supabase PostgreSQL
- OpenAI API
- Python 3.12
- uv

The GitHub Actions workflow is stored at:

```
.github/workflows/daily-digest.yml
```

The workflow securely receives the following values from GitHub repository secrets:

```
OPENAI_API_KEY
DATABASE_URL
```



### Current automation mode

The workflow currently uses manual execution.

This is intentional.

The project is designed so that the same workflow can later be scheduled automatically, but automatic daily execution is currently disabled to avoid recurring OpenAI API costs.

The production workflow has been successfully executed through GitHub Actions and verified against the Supabase database.

## Local Setup



### 1. Clone the repository

```
git clone https://github.com/Aditi279/ai-news-aggregator.git
cd ai-news-aggregator
```



### 2. Install dependencies

This project uses uv.

```
uv sync
```



### 3. Start PostgreSQL locally

Docker Compose is provided for local development:

```
docker compose -f docker/docker-compose.yml up -d
```



### 4. Configure environment variables

Create a .env file in the project root with your local PostgreSQL and OpenAI API configuration.

The repository includes a template:

```
.env.example
```

Never commit .env or API keys to GitHub.

### 5. Create database tables

```
uv run python -m app.db.create_tables
```



### 6. Run the aggregator

```
uv run python -m app.cli
```

The application will fetch new articles, extract content, generate missing summaries, and create the daily digest.

## Running the Pipeline Manually

The application is intentionally usable without a continuously running scheduler.

Run:

```
uv run python -m app.cli
```

Whenever the command is executed, the application checks whether a digest already exists for the current date.

This makes manual execution the default mode while keeping automated scheduling optional.

## Database

The application uses PostgreSQL with SQLAlchemy.

The main entities are:

### Sources

Stores configured news sources.

### Articles

Stores:

- Source
- Title
- URL
- Publication date
- Original summary
- Full article content
- AI-generated summary
- Content-fetch status
- Creation timestamp



### Digests

Stores:

- Digest date
- Generated digest content
- Creation timestamp



## Error Handling

The pipeline includes several safeguards:

- Duplicate article URLs are ignored during ingestion.
- Source-level failures do not stop other sources from being processed.
- HTTP 404 content pages are marked as permanently unavailable.
- Temporary content-fetch failures can be retried.
- Missing article content does not crash the entire pipeline.
- Individual AI summarization failures are logged and do not stop other articles.
- Missing AI summaries are generated only when required.
- Duplicate daily digests are prevented.
- Running the CLI multiple times on the same day does not repeatedly generate the digest.
- Production pipeline operations use structured logging.



## Project Structure

```
ai-news-aggregator/
|
+-- app/
|   +-- agents/
|   |   +-- digest.py
|   |   +-- summarizer.py
|   |
|   +-- db/
|   |   +-- database.py
|   |   +-- models.py
|   |   +-- repositories.py
|   |
|   +-- fetchers/
|   |   +-- anthropic.py
|   |   +-- content.py
|   |   +-- router.py
|   |   +-- rss.py
|   |
|   +-- services/
|   |   +-- daily_digest.py
|   |   +-- fetch_content.py
|   |   +-- generate_summary.py
|   |   +-- ingest.py
|   |
|   +-- cli.py
|   +-- models.py
|
+-- tests/
|   +-- conftest.py
|   +-- test_repositories.py
|
+-- .github/
|   +-- workflows/
|       +-- daily-digest.yml
|
+-- docker/
|   +-- docker-compose.yml
|
+-- .env.example
+-- .gitignore
+-- pyproject.toml
+-- README.md
+-- uv.lock
```



## Tech Stack

- Python 3.12
- PostgreSQL
- Supabase
- SQLAlchemy
- OpenAI API
- BeautifulSoup
- Requests
- Feedparser
- Pydantic
- uv
- Docker / Docker Compose
- pytest
- GitHub Actions



## Testing

The project includes an automated pytest test suite covering:

- Repository operations
- Article creation
- Article content fetching
- HTTP 404 handling
- HTTP failure handling
- AI summary generation
- Summary failure handling
- Daily digest generation
- Duplicate digest protection
- Empty article handling
- CLI orchestration
- Source-level ingestion failures
- OpenAI API key validation

Run the complete test suite with:

```
uv run pytest
```

Current test result:

```
23 passed
```



## Production Verification

The application has been successfully executed through GitHub Actions using the production Supabase database.

The cloud workflow successfully:

- Checked out the repository
- Set up Python 3.12
- Installed dependencies using uv
- Connected to Supabase PostgreSQL
- Fetched configured news sources
- Detected duplicate articles
- Completed the application pipeline successfully

The production database was migrated from the local PostgreSQL database and verified with:

```
Sources: 3
Articles: 1249
Digests: 5
```



## Current Status



### Completed

- Multi-source article ingestion
- RSS and web fetching
- PostgreSQL persistence
- SQLAlchemy models and repositories
- Article deduplication
- Article content extraction
- Content-fetch failure handling
- OpenAI article summarization
- Daily digest generation
- Digest persistence
- Duplicate-digest protection
- Source-level error handling
- Production logging
- Separate test database
- Automated pytest test suite
- Supabase PostgreSQL deployment
- GitHub Actions deployment
- Secure GitHub repository secrets
- Successful cloud execution



### Future Improvements

- YouTube channel ingestion
- Additional AI news sources
- Email delivery of daily digests
- Web interface for browsing articles and digests
- API endpoints
- Scheduled automatic execution
- Improved monitoring and alerting
- User-specific digest preferences
- Database migrations with Alembic



## Project Goal

The long-term goal is to turn the pipeline into a configurable AI news intelligence system where users can define the sources and topics they care about and receive a concise, personalized digest instead of manually checking dozens of AI news sources every day.