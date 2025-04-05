"""Module for parsing PubMed API results."""

import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Configure logging
logger = logging.getLogger(__name__)

class PubMedParser:
    """Parser for PubMed API results."""

    def parse_articles(self, records: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse PubMed records into article dictionaries."""
        articles = []
        
        if not records.get('PubmedArticle'):
            logger.warning("No PubmedArticle found in records")
            return articles
            
        for article in records['PubmedArticle']:
            try:
                article_info = self._extract_article_info(article)
                if article_info:
                    articles.append(article_info)
            except Exception as e:
                pmid = article.get('MedlineCitation', {}).get('PMID', 'Unknown')
                logger.error(f"Error parsing article {pmid}: {e}")
                continue
                
        return articles

    def _extract_article_info(self, article: Dict) -> Optional[Dict]:
        """Extract relevant information from a PubMed article."""
        try:
            medline_citation = article.get('MedlineCitation', {})
            article_data = medline_citation.get('Article', {})
            
            # Extract basic information
            pmid = str(medline_citation.get('PMID', ''))
            title = str(article_data.get('ArticleTitle', ''))
            pub_date = self._extract_publication_date(article_data)
            
            # Extract author information
            authors, non_academic_authors, company_affiliations, corresponding_email = (
                self._extract_author_info(article_data)
            )
            
            # Only include articles with company affiliations
            if not company_affiliations:
                return None
                
            return {
                'pmid': pmid,
                'title': title,
                'publication_date': pub_date,
                'authors': authors,
                'non_academic_authors': non_academic_authors,
                'company_affiliations': company_affiliations,
                'corresponding_email': corresponding_email
            }
        except Exception as e:
            logger.error(f"Error extracting article info: {e}")
            return None

    def _extract_publication_date(self, article_data: Dict) -> str:
        """Extract publication date from article data."""
        try:
            pub_date_info = article_data.get('Journal', {}).get('JournalIssue', {}).get('PubDate', {})
            
            year = str(pub_date_info.get('Year', ''))
            month = str(pub_date_info.get('Month', '1'))
            day = str(pub_date_info.get('Day', '1'))
            
            # Convert month name to number
            if month.isalpha():
                try:
                    month = str(datetime.strptime(month, "%b").month)
                except ValueError:
                    try:
                        month = str(datetime.strptime(month, "%B").month)
                    except ValueError:
                        month = "1"
            
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}" if year else ""
        except Exception as e:
            logger.error(f"Error extracting publication date: {e}")
            return ""

    def _extract_author_info(self, article_data: Dict) -> Tuple[
        List[str], List[str], List[str], Optional[str]
    ]:
        """Extract author information from article data."""
        authors = []
        non_academic_authors = []
        company_affiliations = []
        corresponding_email = None
        
        for author in article_data.get('AuthorList', []):
            try:
                # Extract author name
                last_name = author.get('LastName', '')
                fore_name = author.get('ForeName', '')
                initials = author.get('Initials', '')
                
                author_name = f"{last_name} {fore_name}" if fore_name else f"{last_name} {initials}" if initials else last_name
                if not author_name.strip():
                    continue
                    
                authors.append(author_name)
                
                # Extract affiliations
                affiliations = []
                for affil in author.get('AffiliationInfo', []):
                    if affil_text := affil.get('Affiliation'):
                        affiliations.append(affil_text)
                        # Check for email
                        if not corresponding_email:
                            if email_match := re.search(r'[\w\.-]+@[\w\.-]+', affil_text):
                                corresponding_email = email_match.group(0)
                
                # Check for company affiliation
                is_non_academic = any(self._is_company_affiliation(affil) for affil in affiliations)
                if is_non_academic:
                    non_academic_authors.append(author_name)
                    for affil in affiliations:
                        if company_name := self._extract_company_name(affil):
                            if company_name not in company_affiliations:
                                company_affiliations.append(company_name)
            except Exception as e:
                logger.error(f"Error parsing author: {e}")
                continue
                
        return authors, non_academic_authors, company_affiliations, corresponding_email

    def _is_company_affiliation(self, affiliation: str) -> bool:
        """Check if affiliation is from a pharmaceutical/biotech company."""
        affiliation_lower = affiliation.lower()
        
        # Academic indicators (negative)
        academic_keywords = {
            'university', 'college', 'institute', 'school', 'hospital',
            'medical center', 'clinic', 'foundation', 'academy'
        }
        
        # Company indicators (positive)
        company_keywords = {
            'pharma', 'pharmaceutical', 'biotech', 'therapeutics',
            'inc.', 'llc', 'ltd', 'gmbh', 'biosciences', 'laboratories'
        }
        
        has_company = any(kw in affiliation_lower for kw in company_keywords)
        has_academic = any(kw in affiliation_lower for kw in academic_keywords)
        
        return has_company and not has_academic

    def _extract_company_name(self, affiliation: str) -> Optional[str]:
        """Extract company name from affiliation string."""
        try:
            # Pattern for company names
            patterns = [
                r'([A-Z][A-Za-z0-9\s&-]+)\s+(?:Pharma|Pharmaceuticals|Biotech|Therapeutics|Inc\.?|LLC|Ltd\.?|GmbH)',
                r'([A-Z][A-Za-z0-9\s&-]+)(?:,\s+Inc\.?|,\s+LLC|,\s+Ltd\.?|,\s+GmbH)'
            ]
            
            for pattern in patterns:
                if match := re.search(pattern, affiliation, re.IGNORECASE):
                    return match.group(1).strip()
                    
            return None
        except Exception as e:
            logger.error(f"Error extracting company name: {e}")
            return None