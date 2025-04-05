"""Module for handling output of PubMed search results."""

import csv
import logging
import sys
from typing import Dict, List, Optional, TextIO

import pandas as pd
from pandas import DataFrame

# Configure logging
logger = logging.getLogger(__name__)

class OutputHandler:
    """Handler for outputting PubMed search results."""
    
    def __init__(self, debug: bool = False) -> None:
        """
        Initialize the output handler.
        
        Args:
            debug: Whether to print debug information
        """
        self.debug = debug
        if self.debug:
            logger.setLevel(logging.DEBUG)

    def output_results(
        self, 
        articles: List[Dict[str, str]], 
        output_file: Optional[str] = None
    ) -> None:
        """
        Output the results to CSV file or stdout.
        
        Args:
            articles: List of article dictionaries
            output_file: Optional path to output file
        """
        if not articles:
            logger.warning("No articles to output")
            return

        # Prepare data for CSV
        data: List[Dict[str, str]] = []
        for article in articles:
            try:
                row = {
                    "PubmedID": str(article.get("pmid", "")),
                    "Title": str(article.get("title", "")).strip(),
                    "Publication Date": str(article.get("publication_date", "")),
                    "Non-academic Author(s)": "; ".join(
                        [str(a) for a in article.get("non_academic_authors", [])]
                    ),
                    "Company Affiliation(s)": "; ".join(
                        [str(c) for c in article.get("company_affiliations", [])]
                    ),
                    "Corresponding Author Email": str(article.get("corresponding_email", ""))
                }
                data.append(row)
            except Exception as e:
                logger.error(f"Error formatting article {article.get('pmid')}: {e}")
                continue

        # Output results
        try:
            df: DataFrame = pd.DataFrame(data)
            if output_file:
                df.to_csv(output_file, index=False, encoding='utf-8')
                logger.info(f"Successfully wrote {len(data)} articles to {output_file}")
            else:
                df.to_csv(sys.stdout, index=False)
                logger.info(f"Displayed {len(data)} articles in stdout")
                
        except Exception as e:
            logger.error(f"Failed to output results: {e}")
            raise