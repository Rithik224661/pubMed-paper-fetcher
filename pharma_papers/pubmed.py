"""Module for interacting with the PubMed API."""

import logging
import time
from typing import Dict, List, Optional, Any

from Bio import Entrez

# Configure logging
logger = logging.getLogger(__name__)

class PubMedClient:
    """Client for interacting with the PubMed API."""

    def __init__(self, email: str, api_key: Optional[str] = None) -> None:
        """
        Initialize with rate limiting (3 requests/sec max without API key)
        """
        self.email = email
        self.api_key = api_key
        Entrez.email = email
        if api_key:
            Entrez.api_key = api_key
            self.delay = 0.1  # 10 requests/sec with API key
        else:
            self.delay = 0.34  # 3 requests/sec without key

    def search(self, query: str, max_results: int = 10000) -> List[str]:
        try:
            handle = Entrez.esearch(
                db="pubmed",
                term=query,
                retmax=max_results,
                sort="relevance",
                usehistory="y"  # Enable session caching
            )
            record = Entrez.read(handle)
            handle.close()
            time.sleep(self.delay)
            return record.get("IdList", [])
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

    def fetch_details(self, pmids: List[str]) -> Dict[str, Any]:
        try:
            # Process in batches of 200 (NCBI's recommended max)
            batch_size = 200
            all_records = {"PubmedArticle": []}
            
            for i in range(0, len(pmids), batch_size):
                batch = pmids[i:i + batch_size]
                handle = Entrez.efetch(
                    db="pubmed",
                    id=",".join(batch),
                    retmode="xml"
                )
                records = Entrez.read(handle)
                handle.close()
                if "PubmedArticle" in records:
                    all_records["PubmedArticle"].extend(records["PubmedArticle"])
                time.sleep(self.delay)
                
            return all_records
        except Exception as e:
            logger.error(f"Fetch failed: {e}")
            raise