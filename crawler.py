from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize FirecrawlApp with the API key from environment variables
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# List of URLs to scrape
urls = [
    "https://www.holisticai.com/eu-ai-act-risk-calculator",
    "https://www.holisticai.com/red-teaming",
    "https://www.holisticai.com/about",
    "https://www.holisticai.com/analyst-coverage"
]

# Loop through each URL and scrape
for url in urls:
    try:
        # Scrape the website
        result = app.scrape_url(url, params={'formats': ['markdown', 'html']})
        # Extract and save the markdown content
        markdown_content = result.get('markdown', '')
        with open(f"{url.split('//')[1].replace('/', '_')}.md", "w", encoding="utf-8") as file:
            file.write(markdown_content)
        print(f"Scraped and saved content from {url}")
    except Exception as e:
        print(f"An error occurred while scraping {url}: {str(e)}")
