import cfscrape
import bs4
import logging
from Main.detail import get_detail

def find_light_novel(title):
    scrape = cfscrape.create_scraper()
    lndb_info_query = "http://lndb.info/search?text={}".format(title)
    logging.info("Requesting: {}".format(lndb_info_query))
    page = scrape.get(lndb_info_query,
                        headers={"connection": "keep-alive", "host": "lndb.info"})
    search = bs4.BeautifulSoup(page.content, "html.parser")

    if "search?text=" in page.url:
        light_novel_list = search.find("div", {"id": "bodylightnovelscontentid"})
        light_novels = light_novel_list.findAll('a')

        search_result = []

        for individual in light_novels:
            item = {
                'title': individual.text.strip(),
                'lndb': individual['href'],
            }
            search_result.append(item)
    else:
        search_result = get_detail(page.url)
    return search_result
    
