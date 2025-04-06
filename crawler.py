from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize FirecrawlApp with the API key from environment variables
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# List of URLs to scrape
urls = [
    "https://www.trail-ml.com/",
    "https://www.trail-ml.com/governance",
    "https://www.trail-ml.com/bootcamp",
    "https://www.trail-ml.com/use-cases/development",
    "https://www.trail-ml.com/use-cases/ai-lifecycle-governance",
    "https://www.trail-ml.com/iso-42001",
    "https://www.trail-ml.com/use-cases/regulatory-compliance",
    "https://www.trail-ml.com/use-cases/risk-management",
    "https://www.trail-ml.com/eu-ai-act",
    "https://www.trail-ml.com/blog",
    "https://www.credo.ai/",
    "https://www.credo.ai/product",
    "https://www.credo.ai/solutions/ai-adoption",
    "https://www.credo.ai/solutions/vendor-compliance",
    "https://www.credo.ai/solutions/risk-management",
    "https://www.credo.ai/solutions/regulations-and-standards",
    "https://www.credo.ai/advisory",
    "https://www.credo.ai/advisory/academy",
    "https://www.credo.ai/advisory/sprint", #stops here
    "https://www.credo.ai/advisory/springboard",
    "https://www.credo.ai/advisory/assessments-audit-readiness",
    "https://www.credo.ai/solutions/gen-ai",
    "https://www.credo.ai/solutions/vendor-compliance",
    "https://www.credo.ai/solutions/ai-adoption",
    "https://www.credo.ai/solutions/regulations-and-standards",
    "https://www.credo.ai/solutions/risk-management",
    "https://www.credo.ai/solutions/artifacts",
    "https://www.credo.ai/solutions/regulations-and-standards",
    "https://www.credo.ai/eu-ai-act", #stops here
    "https://www.credo.ai/responsible-ai/iso-42001",
    "https://www.credo.ai/responsible-ai/nist-ai-rmf",
    "https://www.credo.ai/responsible-ai/bias-audit-with-credo-ai",
    "https://www.credo.ai/company",
    "https://www.credo.ai/credo-bility",
    "https://www.credo.ai/glossary",
    "https://www.holisticai.com/",
    "https://www.holisticai.com/ai-governance-platform",
    "https://www.holisticai.com/ai-safeguard",
    "https://www.holisticai.com/ai-audit", #stops here
    "https://www.holisticai.com/ai-audit",
    "https://www.holisticai.com/ai-tracker",
    "https://www.holisticai.com/eu-ai-act-readiness",
    "https://www.holisticai.com/nyc-bias-audit",
    "https://www.holisticai.com/nist-ai-risk-management",
    "https://www.holisticai.com/digital-services-act-audit",
    "https://www.holisticai.com/iso-iec-42001-certification",
    "https://www.holisticai.com/colorado-sb21-169",
    "https://www.holisticai.com/colorado-sb205",
    "https://www.holisticai.com/use-case/ai-risk-posture-reporting",
    "https://www.holisticai.com/use-case/ai-bias-assessment",
    "https://www.holisticai.com/use-case/ai-conformity-assessment",
    "https://www.holisticai.com/use-case/ai-inventory",
    "https://www.holisticai.com/use-case/3rd-party-vendor-management",
    "https://www.holisticai.com/industry/financial-services",
    "https://www.holisticai.com/industry/consumer-goods",
    "https://www.holisticai.com/industry/technology",
    "https://www.holisticai.com/industry/insurance",
    "https://www.holisticai.com/industry/human-capital-management", #stops here
    "https://www.holisticai.com/role/chief-information-officer",
    "https://www.holisticai.com/role/head-of-data-ai",
    "https://www.holisticai.com/role/compliance-and-legal",
    "https://www.holisticai.com/role/chief-data-officer",
    "https://www.holisticai.com/role/chief-technology-officer",
    "https://www.holisticai.com/role/chief-technology-officer",
    "https://www.holisticai.com/role/product",
    "https://www.holisticai.com/role/chief-information-security-officer",
    "https://www.holisticai.com/case-study",
    "https://www.holisticai.com/eu-ai-act-risk-calculator", #stops here
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
