# Clarification Questions for test_project

## Architecture

**Q1:** Should `main.py` be a standalone script (run directly with `python main.py`) or a module importable by other scripts?
> ANSWER:

**Q2:** What Python version should be targeted (e.g., 3.9, 3.11, 3.12)?
> ANSWER:

## Features

**Q3:** For the hello world output — should it print to stdout only, or also write to a log file?
> ANSWER:

**Q4:** Should the hello world message be a fixed string, or configurable via a command-line argument or environment variable?
> ANSWER:

## Data Pipeline (Future)

**Q5:** You mentioned a data pipeline as the eventual goal — what is the data source? (e.g., CSV files, database, REST API, message queue)
> ANSWER:

**Q6:** What is the data destination / output format? (e.g., transformed CSV, database table, another API)
> ANSWER:

**Q7:** Should the pipeline run on a schedule (cron), be triggered manually, or react to events (e.g., file drop, webhook)?
> ANSWER:

## Deployment

**Q8:** What is the target deployment environment? (e.g., local machine, Docker container, cloud VM, serverless)
> ANSWER:

**Q9:** Should `requirements.txt` pin exact versions (e.g., `requests==2.31.0`) or use ranges (e.g., `requests>=2.28`)?
> ANSWER:

## Project Structure

**Q10:** Should the project include tests (e.g., a `tests/` folder with pytest)? Even for the hello world stage?
> ANSWER:

**Q11:** Is there a preferred logging library or level of logging detail expected? (e.g., `print`, stdlib `logging`, `loguru`)
> ANSWER:
