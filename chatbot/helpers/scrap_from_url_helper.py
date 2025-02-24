import requests
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse
import textwrap


def scrape_all_visible_text(url):
    try:
        rp = urllib.robotparser.RobotFileParser()
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        robots_url = base_url + "/robots.txt"
        rp.set_url(robots_url)
        rp.read()
        if not rp.can_fetch("*", url):
            print(f"Scraping disallowed by robots.txt: {url}")
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
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def wrap_text(text, width=80):
    wrapped_text = textwrap.fill(text, width=width)
    return wrapped_text
