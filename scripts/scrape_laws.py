import requests
from bs4 import BeautifulSoup
import os
import time
import logging

# Set up logging to save messages to a file and show them on screen
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler("data/scrape_laws.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Website and laws to scrape
BASE_URL = "https://www.gesetze-im-internet.de/"
LAWS = {
    "aufenthg_2004": "aufenthg_2004/",
    "gg": "gg/",
    "bgb": "bgb/",
    "sgb_4": "sgb_4/",
    "stgb": "stgb/"
}
OUTPUT_DIR = "data/raw/"

def create_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logger.info("Created folder: data/raw/")

def clean_text(text):
    """Remove extra spaces from text."""
    return ' '.join(text.split()).strip()

def scrape_law(url, law_id):
    """Get title and text of a law from its webpage."""
    try:
        # Visit the website page
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Check for errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the title
        title_tag = soup.find('h1')
        title = clean_text(title_tag.text if title_tag else law_id.upper())

        # Find the main content
        content_div = soup.find('div', class_='jnhtml') or soup.find('body')
        content = clean_text(content_div.get_text(separator=' ') if content_div else "No content found")

        if content == "No content found":
            logger.warning(f"No text found for {url}")
        return title, content
    except requests.RequestException as e:
        logger.error(f"Could not scrape {url}: {e}")
        return None, None

def save_law(title, content, law_id):
    """Save law's title and text to a file."""
    filename = os.path.join(OUTPUT_DIR, f"{law_id}.txt")
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n")
            file.write(f"Content: {content}\n")
        logger.info(f"Saved: {filename}")
    except IOError as e:
        logger.error(f"Could not save {filename}: {e}")

def scrape_laws():
    """Scrape all 5 German laws and save them as text files."""
    logger.info("Starting to scrape 5 German laws")
    create_output_dir()

    # Iterate through each law
    for law_id, path in LAWS.items():
        url = f"{BASE_URL}{path}"
        logger.info(f"Scraping: {url}")
        title, content = scrape_law(url, law_id)
        if title and content:
            save_law(title, content, law_id)
        else:
            logger.warning(f"Skipped {law_id} due to error")
        time.sleep(1)  # Wait 1 second to be polite to the website
    logger.info("Finished scraping")

if __name__ == "__main__":
    scrape_laws()