# Pharma Papers Fetcher

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![TestPyPI](https://img.shields.io/testpypi/v/pharma-papers-rithik01)](https://test.pypi.org/project/pharma-papers-rithik01/)

A Python tool to fetch PubMed research papers with pharmaceutical/biotech company affiliations and export them as structured CSV.

## Features

- 🔍 **Advanced PubMed Search** - Supports all [PubMed query syntax](https://pubmed.ncbi.nlm.nih.gov/advanced/)
- 🏢 **Industry Affiliation Detection** - Identifies pharma/biotech company connections using heuristic filtering
- 📊 **Structured CSV Output** - Ready for analysis in Excel/Pandas with 6 key columns
- ⚙️ **Configurable CLI** - Debug mode, API key support, and output customization

## Code Structure
pharma_papers/
├── cli.py # Command-line interface
├── pubmed.py # PubMed API client
├── parser.py # XML parsing logic
├── affiliations.py # Company detection heuristics
└── output.py # CSV generation
tests/ # Unit tests

## Installation

### Prerequisites
- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation)

### Setup
```bash
# Clone repository
git clone https://github.com/Rithik224661/pubMed-paper-fetcher.git
cd pubMed-paper-fetcher

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

Usage
Basic Command
poetry run get-papers-list "cancer[Title]" -e your@email.com -f output.csv
Command Options
Flag	Description	Example
-e	Required email for NCBI	-e user@domain.com
-f	Output file path	-f results.csv
-k	NCBI API key (optional)	-k 123abc...
-m	Max results (default: 10000)	-m 500
-d	Enable debug mode	--debug
Example Queries
# Search with company filter
poetry run get-papers-list "(cancer[Title]) AND (pfizer[AFFL])" -e user@email.com -f results.csv

# Recent clinical trials
poetry run get-papers-list "diabetes[Title] AND clinical trial[PTYP] AND 2023:2025[PDAT]" -e user@email.com -f trials.csvOutput Format
CSV files contain these columns:

PubmedID - Unique identifier

Title - Paper title

PublicationDate - YYYY-MM-DD format

NonAcademicAuthors - Industry-affiliated authors

CompanyAffiliations - Detected companies

CorrespondingAuthorEmail - Contact address

Dependencies
Core Libraries
Package	  Purpose	      Version
Biopython	PubMed API    access	>=1.80
pandas	  CSV export	  >=2.0
requests	HTTP requests	>=2.31

Development Tools
poetry run pytest   # Run unit tests
poetry run mypy .   # Type checking
poetry run black .  # Code formatting
poetry run isort .  # Import sorting

Publishing
Available on TestPyPI:
pip install -i https://test.pypi.org/simple/ pharma-papers-rithik01

