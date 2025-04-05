"""Tests for the affiliations module."""

import unittest

from pharma_papers.affiliations import AffiliationAnalyzer


class TestAffiliationAnalyzer(unittest.TestCase):
    """Test cases for the AffiliationAnalyzer class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.analyzer = AffiliationAnalyzer()

    def test_is_company_affiliated(self) -> None:
        """Test is_company_affiliated method."""
        # Article with company affiliations
        article_with_company = {"non_academic_authors": ["Smith J", "Doe A"]}
        self.assertTrue(self.analyzer.is_company_affiliated(article_with_company))

        # Article without company affiliations
        article_without_company = {"non_academic_authors": []}
        self.assertFalse(self.analyzer.is_company_affiliated(article_without_company))

    def test_extract_company_affiliations(self) -> None:
        """Test extract_company_affiliations method."""
        affiliations = [
            "Pfizer Inc., New York, NY, USA",
            "Department of Biology, University of Example, Example City, USA",
            "Novartis Pharmaceuticals, Basel, Switzerland",
        ]

        companies = self.analyzer.extract_company_affiliations(affiliations)
        self.assertEqual(len(companies), 2)
        self.assertIn("Pfizer", companies)
        self.assertIn("Novartis", companies)


if __name__ == "__main__":
    unittest.main()
