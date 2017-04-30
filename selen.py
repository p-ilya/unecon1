from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from urllib.request import urlretrieve
import time


# noinspection PyByteLiteral
class Unecon_Downloader():
    # абсолютный путь к драйверу
    driver = webdriver.Chrome('C:/Distrib/chromedriver.exe')
    collected_links = []

    def load_schedule_page(self):
        url = 'http://unecon.ru/schedule'
        self.driver.get(url)

        select = Select(self.driver.find_element_by_id(
            'edit-term-node-tid-depth-hierarchical-select-selects-0'
        ))
        select.select_by_value('label_0')

        submit_bttn = self.driver.find_element_by_id('edit-submit-schedule-view')
        time.sleep(5)
        submit_bttn.click()
        time.sleep(5)

    def retrieve_links(self):
        #stable '//*[@id="content"]/div[2]/div[2]/table/tbody/tr/td[1]/div/ul/li/a'
        link_list = self.driver.find_elements_by_xpath(
            '//*[@id="content"]/div[2]/div[2]/table/tbody/tr/td[1]/div/ul/li/a'
            )
        return link_list

    def next_page(self):
        try:
            next_page_bttn = self.driver.find_element_by_xpath(
                '//*[@id="content"]/div[2]/div[3]/ul/li[last()]/a')
            next_page_bttn.click()
            time.sleep(5)
            return True
        
        except NoSuchElementException as e:
            print('Cant flip to next page due to this:\n' + e.msg)
            return False

    def download_files(self):
        s = 0
        for link in self.collected_links:
            destination = link.rsplit('/', 1)[1]
            try:
                urlretrieve(link, destination)
            except ValueError:
                print('This strange error again.')
            s += 1
        print('Downloaded {} files.'.format(s))

    def close_page(self):
        self.driver.close()

    def scenario(self):
        # загрузить страницу в нужном виде
        self.load_schedule_page()
        # получить ссылки с первой страницы
        for l in self.retrieve_links():
            self.collected_links.append(l.get_attribute('href'))
        # перелистнуть на вторую стрницу
        self.next_page()

        # получаить ссылки с остальных страниц
        while True:
            a = self.next_page()
            if not a: break
            for l in self.retrieve_links():
                self.collected_links.append(l.get_attribute('href'))
            #print('Links total: {}'.format(len(self.collected_links)))

        print('Links total: {}'.format(len(self.collected_links)))

        self.close_page()
        self.driver.quit()
        self.download_files()

if __name__ == '__main__':
    downloader = Unecon_Downloader()
    downloader.scenario()
    #downloader.load_schedule_page()
    #tds = downloader.retrieve_links()
    #downloader.driver.quit()
