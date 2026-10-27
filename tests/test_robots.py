"""robots.txt handling in the crawler."""

from types import SimpleNamespace

from app.services.crawler import Crawler


def _crawler(robots_text, status=200):
    crawler = Crawler.__new__(Crawler)
    crawler.session = SimpleNamespace(
        headers={"User-Agent": "Kucibok-Prospector/1.1"},
        get=lambda url, timeout=5: SimpleNamespace(status_code=status, text=robots_text),
    )
    return crawler


def test_other_agent_block_does_not_block_us():
    robots = "User-agent: BadBot\nDisallow: /\n"
    assert _crawler(robots)._check_robots_txt("https://example.com/about")


def test_specific_path_disallowed():
    robots = "User-agent: *\nDisallow: /private/\n"
    crawler = _crawler(robots)
    assert not crawler._check_robots_txt("https://example.com/private/x")
    assert crawler._check_robots_txt("https://example.com/about")
