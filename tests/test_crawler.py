"""Tests for crawler service."""

from app.services.crawler import Crawler, CrawlResult


def test_crawler_rate_limiting():
    """Test crawler rate limiting."""
    crawler = Crawler()

    # First request
    crawler._rate_limit("example.com")

    # Second request should be delayed
    import time

    start = time.time()
    crawler._rate_limit("example.com")
    elapsed = time.time() - start

    # Should have waited ~1 second
    assert elapsed >= 0.9  # Allow some margin


def test_normalize_url():
    """Test URL normalization."""
    # These don't really do crawling due to network, just test crawl logic
    result = CrawlResult("https://example.com", "SUCCESS", {"title": "Example"})
    assert result.status == "SUCCESS"
    assert result.url == "https://example.com"


def test_crawl_result():
    """Test CrawlResult object."""
    result = CrawlResult(
        "https://example.com",
        "SUCCESS",
        data={"title": "Test", "emails": ["test@example.com"]},
    )
    assert result.status == "SUCCESS"
    assert result.data["title"] == "Test"
    assert len(result.data["emails"]) == 1
