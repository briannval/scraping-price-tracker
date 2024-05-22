import os
import re
import time
from datetime import datetime as dt

import pandas as pd
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from data import AGODA_URL, TIKET_URL, TRAVELOKA_URL


class Ota:
    """
    Class to scrape prices from various OTA websites
    """

    def __init__(self):
        self.name = "OTA Price Scraper"
        self.scraping_results = {
            "Date & Time": [],
            "Hotel Name": [],
            "Tiket Price": [],
            "Traveloka Price": [],
            "Agoda Price": [],
        }
        self.df = None

    def __convert_scraped_string(self, s):
        return int(
            "".join(
                re.findall(r"\d+", s),
            ),
        )

    def __get_comparison(self, comparator, comparison):
        if comparator == comparison:
            return "NO DIFF", 0

        if comparator > comparison:
            return "HIGHER", ((comparator - comparison) / comparator)

        return "LOWER", ((comparison - comparator) / comparator)

    def init_hotel(self, hotel):
        """
        Initialize hotel name and scraping time & date
        """
        self.scraping_results["Date & Time"].append(
            dt.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.scraping_results["Hotel Name"].append(hotel)

    def tiket_scraping(self, hotel_name, driver):
        """
        Scraping source from tiket.com
        """
        try:
            driver.get(TIKET_URL)
            time.sleep(2)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div[3]/div/div[2]/div[2]/div/div[2]/div[1]",
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[2]/div[5]/div/div/section/div/div/div/div[1]/div/div/div/label/input",
            ).send_keys(
                hotel_name,
            )
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[2]/div[5]/div/div/section/div/div/div/div[2]/div",
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div[3]/div/div[2]/div[2]/div/div[2]/button",
            ).click()
            time.sleep(4)
            res = self.__convert_scraped_string(
                driver.find_element(
                    By.XPATH,
                    "//h3[contains(text(), 'IDR')]",
                ).text
            )
            self.scraping_results["Tiket Price"].append(res)
            print(f"Result for tiket: {res} \n")
        except NoSuchElementException:
            self.scraping_results["Tiket Price"].append("UNAVAILABLE")
            print(f"Unable to scrape for {hotel_name} in Tiket")

    def traveloka_scraping(self, hotel_name, driver):
        """
        Scraping source from traveloka.com
        """
        try:
            driver.get(TRAVELOKA_URL)
            time.sleep(2)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[5]/div/div/div[2]/div/div[1]/div[1]/div/div[1]/input",
            ).send_keys(
                hotel_name,
            )
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[5]/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div[1]/div[2]",
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[5]/div[2]/div/div[2]/div/div[5]/div[2]/div",
            ).click()
            time.sleep(4)
            """
            ADS?
            driver.find_element(
                By.XPATH,
                "/html/body/div[19]/div/div[2]/div/div[1]",
            ).click()
            time.sleep(2)
            """
            res = self.__convert_scraped_string(
                driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div[5]/div[2]/div/div[2]/div[3]/div/div/div[2]/div[3]/div/div/div[1]/div[3]/div/div[3]/div[1]",
                ).text
            )
            self.scraping_results["Traveloka Price"].append(res)
            print(f"Result for traveloka: {res} \n")
        except NoSuchElementException:
            self.scraping_results["Traveloka Price"].append("UNAVAILABLE")
            print(f"Unable to scrape for {hotel_name} in Traveloka")

    def agoda_scraping(self, hotel_name, driver):
        try:
            driver.get(AGODA_URL)
            time.sleep(2)
            """
            driver.find_element(
                By.XPATH,
                "/html/body/div[9]/div[2]/div/section/section/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div",
            )
            time.sleep(1)
            """
            input_element = driver.find_element(
                By.XPATH,
                "/html/body/div[9]/div[2]/div/section/section/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div/div/input",
            )
            input_element.clear()
            input_element.send_keys(
                hotel_name,
            )
            time.sleep(1)
            while True:
                try:
                    driver.find_element(
                        By.XPATH,
                        "/html/body/div[9]/div[2]/div/section/section/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/ul/li",
                    ).click()
                    break
                except ElementClickInterceptedException:
                    driver.find_element(
                        By.XPATH,
                        "/html/body/div[16]/div[2]/button",
                    ).click()
                    time.sleep(1)

            """
            actions = ActionChains(driver)
            actions.send_keys(Keys.SPACE)
            time.sleep(1)
            actions.send_keys(Keys.SPACE)
            """
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[9]/div[2]/div/section/section/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/div[3]",
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[9]/div[2]/div/section/section/div/div[2]/div[2]/div/div/div[2]/div/button",
            ).click()
            time.sleep(4)
            res = self.__convert_scraped_string(
                driver.find_elements(
                    By.XPATH, "//span[@class='PropertyCardPrice__Value']"
                )[0].text
            )
            self.scraping_results["Agoda Price"].append(res)
            print(f"Result for Agoda: {res} \n")

        except NoSuchElementException:
            self.scraping_results["Agoda Price"].append("UNAVAILABLE")
            print(f"Unable to scrape for {hotel_name} in Agoda")

    def hb_scraping(self, hotel_name, driver):
        pass

    def expedia_scraping(self, hotel_name, driver):
        pass

    def __prepare_for_download(self):
        if self.df is None:
            self.df = pd.DataFrame(self.scraping_results)
        if not os.path.exists("result"):
            os.makedirs("result")

    def download_as_excel(self):
        self.__prepare_for_download()
        file_path = os.path.join("result", "ota.xlsx")  # Default output path
        self.df.to_excel(file_path, sheet_name="Hotels", index=False)
        print(f"Successfully downloaded to {file_path}")

    def download_as_csv(self):
        self.__prepare_for_download()
        file_path = os.path.join("result", "ota.csv")  # Default output path
        self.df.to_csv(file_path, sep=",", index=False)
        print(f"Successfully downloaded to {file_path}")
