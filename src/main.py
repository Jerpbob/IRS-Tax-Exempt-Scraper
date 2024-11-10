from scrapers.scrape_ein import EIN_Scraper
from scrapers.scrape_990 import NineNineZero_Scraper

def get_valid_ein(url, pages):
    scraped_ein = EIN_Scraper(url).scrape(pages)
    print(scraped_ein)
    return scraped_ein

def filter_ein(url, scraped_ein):
    filtered_ein = NineNineZero_Scraper(url).scrape(scraped_ein)

    print(filtered_ein)
    return filtered_ein

def scrape_ein(url, pages):
    scraped_ein = get_valid_ein(url, pages)
    filtered_ein = filter_ein(url, scraped_ein)
    return filtered_ein

if __name__ == '__main__':
    url = 'https://apps.irs.gov/app/eos/'
    results = scrape_ein(url, [1,2,3,4,5])
    print(results)