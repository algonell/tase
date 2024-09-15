# Description: This script scrapes data from the Tel Aviv Stock Exchange (TASE) website.
# It downloads the following data:
# 1. Index components
# 2. Currency exchange rates
# 3. Company finance report
# 4. Optionally: Security history end-of-day (EOD) [Uncomment the line in the for loop to download this data]
# The data is saved in the 'data' folder in the current working directory.
# The script uses Selenium to automate the process of downloading the data.
# The script requires the user to log in to the TASE website manually (doing so with a Google account might not work with Selenium).
# Author: Marc Berneman

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import pandas as pd
import time
from tqdm import tqdm

sleep_time = 1
sleep = lambda : time.sleep(sleep_time)

download_dir = Path.cwd() / 'data'
download_dir.mkdir(exist_ok=True)

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": str(download_dir)}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

url = 'https://www.tase.co.il/en'
driver.get(url)
input('Press Enter after you log in...')

def get_index_components():
    if not (download_dir / 'indexcomponents.csv').exists():
        url = 'https://market.tase.co.il/en/market_data/index/142/components/index_weight'
        driver.get(url)

        sleep()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'icon-download'))).click()
        sleep()
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'CSV'))).click()
        sleep()

def get_company_finance_report(security_id):
    file_download = download_dir / 'companyFinanceReport.csv'
    file_download.unlink(missing_ok=True)
    file = download_dir / f'{symbol}FinanceReport.csv'
    if not file.exists():
        url = f'https://market.tase.co.il/en/market_data/security/{security_id}/major_data'
        driver.get(url)

        sleep()
        string: str = driver.page_source
        idx = string.find('company/')
        string = string[idx:][8:]
        idx = string.find('/')
        company_id = string[:idx]
        url = f'https://market.tase.co.il/en/market_data/company/{company_id}/financial_reports'
        driver.get(url)

        sleep()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'icon-download'))).click()
        sleep()
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'CSV'))).click()
        sleep()

        file_download.rename(file)


def get_security_history_eod(security_id):
    file_download = download_dir / 'securityHistoryEOD.csv'
    file_download.unlink(missing_ok=True)
    file = download_dir / f'{symbol}securityHistoryEOD.csv'
    if not file.exists():
        url = f'https://market.tase.co.il/en/market_data/security/{security_id}/historical_data/eod?pType=6'
        driver.get(url)

        sleep()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'icon-download'))).click()
        sleep()
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'CSV'))).click()
        sleep()

        file_download.rename(file)

def get_currency_exchange():
    if not (download_dir / 'dailyreviewforeignexchange.csv').exists():
        url = 'https://market.tase.co.il/en/market_data/daily-review/exchange_rates'
        driver.get(url)

        sleep()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'icon-download'))).click()
        sleep()
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'CSV'))).click()
        sleep()


while True:
    try:
        get_index_components()
        get_currency_exchange()

        file = download_dir / 'indexcomponents.csv'
        df = pd.read_csv(file, header=2)
        df.columns = df.columns.str.strip()  # remove space from column names
        df = df[['Symbol', 'Security No']]

        for i in tqdm(range(len(df))):
            symbol = df['Symbol'].iloc[i]
            security_id = df['Security No'].iloc[i]

            get_company_finance_report(security_id)
            # get_security_history_eod(security_id)
    except TimeoutException:
        input('\nTimeoutException: please fix the issue and press Enter. Bringing the window into view might help...')
        continue
    break

driver.quit()