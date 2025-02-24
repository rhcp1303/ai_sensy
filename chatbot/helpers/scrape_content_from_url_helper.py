import requests
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse
import textwrap
import logging

logger = logging.getLogger(__name__)


def scrape_all_visible_text(url):
    """
        Scrapes all visible text content from a given URL.

        This function fetches the HTML content of the specified URL, parses it using
        BeautifulSoup, and extracts the text content from various common HTML elements
        (paragraphs, headings, lists, table cells, spans, and divs). It also checks
        the robots.txt file to ensure that scraping is allowed for the given URL.

        Args:
            url (str): The URL of the web page to scrape.

        Returns:
            str | None: The combined text content of the visible elements, separated by newlines,
                       or None if an error occurs or scraping is disallowed by robots.txt.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the HTTP request.
            Exception: If any other error occurs during the scraping process.

        Example:
            ```python
            url = "[https://www.example.com](https://www.example.com)"
            text = scrape_all_visible_text(url)
            if text:
                print(text)
            else:
                print("Failed to scrape text from the URL.")
            ```
        """

    try:
        rp = urllib.robotparser.RobotFileParser()
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        robots_url = base_url + "/robots.txt"
        rp.set_url(robots_url)
        rp.read()
        if not rp.can_fetch("*", url):
            logger.info(f"Scraping disallowed by robots.txt: {url}")
            return None
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        all_text = []
        for element in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "td", "th", "span", "div"]):
            text = element.get_text(strip=False)
            if text:
                all_text.append(text)
        combined_text = "\n".join(all_text)
        return combined_text
    except requests.exceptions.RequestException as e:
        logger.info(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return None


def wrap_text(text, width=80):
    wrapped_text = textwrap.fill(text, width=width)
    return wrapped_text
