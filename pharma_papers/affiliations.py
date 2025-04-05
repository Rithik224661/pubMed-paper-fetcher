"""Module for identifying company affiliations in PubMed articles."""

import logging
import re
from typing import Dict, List, Set

# Configure logging
logger = logging.getLogger(__name__)


class AffiliationAnalyzer:
    """Analyzer for identifying company affiliations in PubMed articles."""

    def __init__(self) -> None:
        """Initialize the affiliation analyzer."""
        # List of known pharmaceutical and biotech companies
        self.known_companies: Set[str] = {
            "pfizer",
            "merck",
            "novartis",
            "roche",
            "sanofi",
            "johnson & johnson",
            "glaxosmithkline",
            "gsk",
            "astrazeneca",
            "abbvie",
            "eli lilly",
            "bristol-myers squibb",
            "amgen",
            "gilead",
            "biogen",
            "regeneron",
            "vertex",
            "moderna",
            "biontech",
            "genentech",
            "boehringer ingelheim",
            "takeda",
            "bayer",
            "novo nordisk",
            "celgene",
            "alexion",
            "incyte",
            "biomarin",
            "alnylam",
            "seagen",
        }

        # Company suffixes that indicate a commercial entity
        self.company_suffixes: Set[str] = {
            "inc",
            "inc.",
            "llc",
            "ltd",
            "ltd.",
            "limited",
            "corp",
            "corp.",
            "corporation",
            "pharmaceuticals",
            "pharma",
            "therapeutics",
            "biosciences",
            "biotechnology",
            "laboratories",
            "labs",
            "gmbh",
            "co.",
            "co",
            "ag",
            "s.a.",
            "plc",
            "n.v.",
        }

    def is_company_affiliated(self, article: Dict) -> bool:
        """
        Determine if an article has authors affiliated with companies.

        Args:
            article: Article dictionary with author and affiliation information

        Returns:
            True if at least one author is affiliated with a company
        """
        return len(article.get("non_academic_authors", [])) > 0

    def extract_company_affiliations(self, affiliations: List[str]) -> List[str]:
        """
        Extract company names from a list of affiliation strings.

        Args:
            affiliations: List of affiliation strings

        Returns:
            List of identified company names
        """
        companies = []

        for affiliation in affiliations:
            company_name = self._identify_company(affiliation)
            if company_name and company_name not in companies:
                companies.append(company_name)

        return companies

    def _identify_company(self, affiliation: str) -> str:
        """
        Identify a company name from an affiliation string.

        Args:
            affiliation: Affiliation string

        Returns:
            Identified company name or empty string if not found
        """
        # Check for known companies
        affiliation_lower = affiliation.lower()
        for company in self.known_companies:
            if company in affiliation_lower:
                # Try to extract the full company name with proper capitalization
                pattern = re.compile(re.escape(company), re.IGNORECASE)
                match = pattern.search(affiliation)
                if match:
                    return match.group(0)
                return company

        # Look for company suffixes
        for suffix in self.company_suffixes:
            pattern = re.compile(
                r"([A-Z][A-Za-z0-9\-\s]+)\s+" + re.escape(suffix), re.IGNORECASE
            )
            match = pattern.search(affiliation)
            if match:
                return f"{match.group(1)} {suffix}"

        return ""
