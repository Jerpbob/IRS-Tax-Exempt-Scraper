import time
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class NineNineZero_Scraper:
    def __init__(self, url: str):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)
        # self.driver = webdriver.Firefox()
        self.url = url

    def connect_irs(self):
        URL = self.url
        self.driver.get(URL)

    def select_db(self):
        css_selector = 'select[aria-label="Select Database Select an option"]'
        drop_down_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        drop_down = Select(drop_down_button)
        drop_down.select_by_visible_text(
            'Copies of Returns (990, 990-EZ, 990-PF, 990-T)')

    def input_ein(self, ein):
        css_selector = 'input[id="einTerm"]'
        input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        input.send_keys(ein)
        print('inputted ein!')

    def select_search(self):
        css_selector = 'button[aria-label="Search"]'
        search_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        search_button.click()
        print('selected search!')

    def select_org(self):
        css_selctor = 'a[href="/app/eos/details/"]'
        link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selctor)
            )
        )
        link.click()
        print('selected org')

    def check_valid(self):
        css_selector = 'div[id="returnsAccordion"]'
        consecutive = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        print('checking if valid')
        text = consecutive.text
        valid_test = True
        if '990-EZ' in text or '990T' in text:
            valid_test = False
        else:
            regex = r'Tax\sYear\s(\d{4})\sForm\s990'
            years = re.findall(regex, text)
            is_consecutive = all(int(years[i]) >= int(years[i-1]) - 2  for i in range(1, 3))
            valid_test = is_consecutive
            # valid_test = years
        print(years)
        return valid_test
    
    def select_back(self):
        css_selector = 'button[aria-label="Back"]'
        back = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        back.click()

        css_selector = 'input[id="einTerm"]'
        input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        input.clear()
        print('cleared ein!')
    
    def check_valid_eins(self, ein_lst: list[str]) -> list[str]:
        valid_ein = []
        for ein in ein_lst:
            time.sleep(5)
            print(ein)
            try:
                self.input_ein(ein)
                self.select_search()
                self.select_org()
                valid = self.check_valid()
                self.select_back()
                if valid:
                    valid_ein.append(ein)
            except:
                self.select_back()
                continue
        return valid_ein


    def scrape(self, ein_lst):
        start = time.time()
        self.connect_irs()
        self.select_db()
        ein_lst = self.check_valid_eins(ein_lst)
        self.driver.quit()
        end = time.time()
        print('Time: ', (end - start) * 10**3, 'ms')
        return ein_lst

if __name__ == '__main__':
    url = 'https://apps.irs.gov/app/eos/'
    scrape_irs = NineNineZero_Scraper(url)
    ein_lst = [
        '742730665', 
        '842998955', 
        '814429898', 
        '920920552', 
        '832844412', 
        '900070372', 
        '474714415', 
        '873962402', 
        '383868253', 
        '273842735', 
        '462131343', 
        '760439305', 
        '742924578', 
        '752542434', 
        '813474082', 
        '202768192', 
        '510174252', 
        '742311530', 
        '871722582', 
        '742007539', 
        '463173749'
    ]
    results = scrape_irs.scrape(ein_lst)
    print(results)
    print(len(results))