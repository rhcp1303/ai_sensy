import requests
from bs4 import BeautifulSoup


def scrape_content(url, element_selector, attribute=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        elements = soup.select(element_selector)
        scraped_data = []
        for element in elements:
            if attribute:
                value = element.get(attribute)
                if value:
                    scraped_data.append(value)
            else:
                scraped_data.append(str(element))
        return scraped_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return []
