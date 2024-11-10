import time
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class EIN_Scraper:
    def __init__(self, url: str):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)
        # self.driver = webdriver.Firefox()
        self.url = url

    def connect_irs(self):
        URL = self.url
        self.driver.get(URL)

    def select_texas(self):
        css_selector = 'select[aria-label="State Select an option"]'
        drop_down_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        drop_down = Select(drop_down_button)
        drop_down.select_by_visible_text('Texas')
    
    def select_search(self):
        css_selector = 'button[aria-label="Search"]'
        search_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        search_button.click()

    def results_per_page_250(self):
        css_selector = 'select[aria-label="Results Per Page Select an option"]'
        drop_down_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        drop_down = Select(drop_down_button)
        drop_down.select_by_visible_text('250')
        time.sleep(.5)

    def change_page(self, page: int):
        css_selector = 'input[aria-label="Jump To"]'
        input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        input.send_keys(str(page))

        css_selector = 'button[aria-label="Go"]'
        go = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        go.click()
        time.sleep(.5)

    def extract_ein(self) -> str:
        css_selector = 'table.w-full'
        ein = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        ein_lst = str(ein.text)
        return ein_lst

    def filter_ein(self, ein_lst: str) -> str:
        regex = r'\b(\d{2}-\d{7}).+Texas\sUnited\sStates\s.+Copies\sof\sReturns\b'
        copies_of_returns = re.findall(regex, ein_lst)
        return copies_of_returns

    def extract_pages(self, page_lst: list[int]) -> list[str]:
        extracted_ein = []
        for page in page_lst:
            self.change_page(page)
            ein_lst = self.extract_ein()
            ein_990 = self.filter_ein(ein_lst)
            extracted_ein.extend(ein_990)
            # time.sleep(.5)
        return extracted_ein
    
    def scrape(self, page_lst):
        self.connect_irs()
        self.select_texas()
        self.results_per_page_250()
        ein_lst = self.extract_pages(page_lst)
        self.driver.quit()
        return ein_lst
    

# css_selector = 'table.w-full'
# companies = WebDriverWait(self.driver, 10).until(
#     EC.presence_of_element_located(
#         (By.CSS_SELECTOR, css_selector)
#     )
# )
# companies = str(companies.text)
# regex = r'\b(\d{2}-\d{7}).+Texas\sUnited\sStates\s.+Copies\sof\sReturns\b'
# copies_of_returns = re.findall(regex, companies)
# print(copies_of_returns)
# time.sleep(10)

if __name__ == '__main__':
    url = 'https://apps.irs.gov/app/eos/'
    scrape_irs = EIN_Scraper(url)
    results = scrape_irs.scrape([1, 2, 3, 4])
    print(results)
    print(len(results))