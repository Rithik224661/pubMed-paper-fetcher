# Pharma Papers Fetcher

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

A Python tool to fetch PubMed research papers with pharmaceutical/biotech company affiliations and export them as CSV.

## Features

- 🔍 **Advanced PubMed Search** - Supports all [PubMed query syntax](https://pubmed.ncbi.nlm.nih.gov/advanced/)
- 🏢 **Industry Affiliation Detection** - Identifies pharma/biotech company connections
- 📊 **Structured CSV Output** - Ready for analysis in Excel/Pandas
- ⚙️ **Configurable CLI** - Multiple output options and debugging

## Code Organization

The project follows a modular structure:
pharma_papers/
├── cli.py # Command-line interface
├── pubmed.py # PubMed API client
├── parser.py # XML parsing logic
├── affiliations.py # Company detection
└── output.py # CSV generation
tests/ # Unit tests


## Installation

### Prerequisites
- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation)

### Setup
```bash
git clone https://github.com/yourusername/pharma-papers.git
cd pharma-papers
poetry install

Usage
Basic Command
poetry run get-papers-list "cancer[Title]" -e your@email.com -f output.csv

Options
Flag	Description	Example
-e	Required email for NCBI	-e user@domain.com
-f	Output file path	-f results.csv
-k	NCBI API key (optional)	-k 123abc...
-m	Max results (default: 10000)	-m 500
-d	Debug mode	--debug
Example Queries

# Search with company filter
poetry run get-papers-list "(cancer[Title]) AND (pfizer[AFFL] OR novartis[AFFL])" -e user@email.com -f results.csv

# Recent clinical trials
poetry run get-papers-list "cancer[Title] AND clinical trial[PTYP] AND 2023:2025[PDAT]" -e user@email.com -f trials.csv

Output Format
CSV file containing:

PubmedID: Unique identifier

Title: Paper title

Publication Date: YYYY-MM-DD format

Non-academic Author(s): Industry-affiliated authors

Company Affiliation(s): Detected companies

Corresponding Author Email: Contact address

Dependencies
Package	Purpose	Link
Biopython	PubMed API access	biopython.org
pandas	CSV export	pandas.pydata.org
requests	HTTP requests	requests.readthedocs.io
typing-extensions	Type hints	pypi.org/project/typing-extensions

Development
Testing
poetry run pytest  # Run unit tests
Code Quality
poetry run mypy .  # Type checking
poetry run black .  # Code formatting
poetry run isort .  # Import sorting

## Tools & Libraries Used

The project utilizes these key components:

### Core Libraries
| Library | Purpose | Documentation |
|---------|---------|---------------|
| [Biopython](https://biopython.org/) | PubMed API interaction | [Bio.Entrez Docs](https://biopython.org/docs/1.75/api/Bio.Entrez.html) |
| [pandas](https://pandas.pydata.org/) | Data processing & CSV export | [pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html) |
| [requests](https://requests.readthedocs.io/) | HTTP requests | [Requests Docs](https://requests.readthedocs.io/en/latest/) |

### Development Tools
| Tool | Usage | Link |
|------|-------|------|
| [Poetry](https://python-poetry.org/) | Dependency management | [Poetry Docs](https://python-poetry.org/docs/) |
| [pytest](https://docs.pytest.org/) | Testing framework | [pytest Guide](https://docs.pytest.org/en/7.4.x/) |
| [mypy](https://mypy.readthedocs.io/) | Static type checking | [mypy Docs](https://mypy.readthedocs.io/en/stable/) |

### Supplementary Packages
- `typing-extensions`: For type hints compatibility
- `python-dateutil`: Date parsing utilities
- `loguru`: Enhanced logging (optional)