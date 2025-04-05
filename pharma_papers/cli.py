"""Command-line interface for the PubMed Paper Fetcher."""

import argparse
import logging
import re
import sys
from typing import List, Optional

from pharma_papers.affiliations import AffiliationAnalyzer
from pharma_papers.output import OutputHandler
from pharma_papers.parser import PubMedParser
from pharma_papers.pubmed import PubMedClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: Command-line arguments (defaults to sys.argv[1:])

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed with pharmaceutical company affiliations"
    )
    parser.add_argument("query", help="PubMed search query")
    parser.add_argument(
        "-f", "--file", help="Output file path (default: print to stdout)", default=None
    )
    parser.add_argument(
        "-d", "--debug", help="Print debug information", action="store_true"
    )
    parser.add_argument(
        "-e", "--email", help="Email address for PubMed API (required)", required=True
    )
    parser.add_argument(
        "-k", "--api-key", help="NCBI API key for higher rate limits", default=None
    )
    parser.add_argument(
        "-m",
        "--max-results",
        help="Maximum number of results to fetch",
        type=int,
        default=10000,
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the command-line interface.

    Args:
        args: Command-line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        if not sys.argv[1:]:  # Show help if no args
            parse_args(["-h"])
            return 0

        parsed_args = parse_args(args)

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", parsed_args.email):
            logger.error("Invalid email format")
            return 1

        # Configure logging level
        if parsed_args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")

        # Initialize components
        pubmed_client = PubMedClient(
            email=parsed_args.email, api_key=parsed_args.api_key
        )
        parser = PubMedParser()
        affiliation_analyzer = AffiliationAnalyzer()
        output_handler = OutputHandler(debug=parsed_args.debug)

        # Search PubMed
        pmids = pubmed_client.search(
            parsed_args.query, max_results=parsed_args.max_results
        )

        if not pmids:
            logger.warning("No results found for query")
            return 0

        # Fetch article details
        records = pubmed_client.fetch_details(pmids)

        # Parse articles
        articles = parser.parse_articles(records)

        # Filter for articles with company affiliations
        company_articles = [
            article
            for article in articles
            if affiliation_analyzer.is_company_affiliated(article)
        ]

        if not company_articles:
            logger.warning("No articles with pharmaceutical company affiliations found")
            return 0

        # Output results
        output_handler.output_results(company_articles, parsed_args.file)

        return 0
    except Exception as e:
        logger.error(f"Error: {e}")
        if parsed_args and parsed_args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
