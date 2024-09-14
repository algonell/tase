# Tel Aviv Stock Exchange Data Scrapper
Python utilities to scrape historical price data from [TASE](https://www.tase.co.il/).
In addition, financial data of the TA-35 companies can be scraped to calculate the PE ratio of the index.

## Prerequisites

``` pip install -r requirements.txt ```

[ChromeDriver](https://chromedriver.chromium.org/)
- Linux: copy to /usr/bin
- Windows: place in the same directory as the script or add to PATH

## Stocks

![Stocks](/Pics/Stocks.png)

## ETF

![ETF](/Pics/ETF.png)

## Sample

![Plot](/Pics/Plot.png)

## TA-35 PE Ratio calculation
Use the following script to scrape the financial data of the TA-35 companies.
```
cd TA35
python scrapeData.py
```
You need a TASE account to download the data; the script will prompt you to log in via the browser.
After scraping the data, you can calculate the PE ratio of the TA-35 index by running the `dataAnalysis.ipynb` notebook.