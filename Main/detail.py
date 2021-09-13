import bs4
import cfscrape
import logging
from Main.light_model import LightNovelInfo

def create_light_novel_info(match, scrape_instance):
    content_url = match.get("href")
    view_url = "http://lndb.info/light_novel/view/{}".format(content_url.split("/")[-1])
    fetch_message = "Fetch information from: {}".format(view_url)
    logging.info(fetch_message)
    light_novel_page = scrape_instance.get(view_url, headers={
        "Referer": content_url,
        "Connection": "keep-alive",
        "host": "lndb.info",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    })
    light_novel_page_soup = bs4.BeautifulSoup(light_novel_page.content, "html.parser")

    light_novel_title = content_url.split("/")[-1].replace("_", " ")
    information_message = "Fetch information from light novel: {}".format(light_novel_title)
    logging.info(information_message)
    light_novel_info = LightNovelInfo(title=light_novel_title, lndb_link=content_url)
    secondary_info = light_novel_page_soup.find("div", {"class": "secondary-info"})
    if secondary_info is not None:
        info_values = secondary_info.findAll("td", {"class": "secondary-info-value"})

        for info_value in info_values:
            info_key = info_value.parent.find("td")
            if "Author" in info_key.text:
                light_novel_info.author = info_value.text.strip()
            if "Illustrator" in info_key.text:
                light_novel_info.illustrator = info_value.text.strip()
            if "Genre" in info_key.text:
                genres = info_value.text.split(",")
                light_novel_info.genre = [genre.lstrip() for genre in genres]
            if "Volumes" in info_key.text:
                light_novel_info.volumes = info_value.text

    plot_section = light_novel_page_soup.find("div", {"class": "lightnovelabout"})
    if plot_section is not None:
        plot_paragraph =  plot_section.find("p", {"class": "paragraph-info"})
        p =  str(plot_paragraph)
        q = p.replace('<p class="paragraph-info">', '').strip()
        r = q.replace('</p>', '')
        s = r.split('<br/><br/>')
        plot_content = s[0].strip()
    else: plot_content = ''
    light_novel_info.plot = plot_content
    
    alternative_titles = light_novel_page_soup.find("div", {"class": "lightnovelassociatedtitles"})
    alternative_titles_list = alternative_titles.find("p", {"class": "paragraph-info"}) if alternative_titles is not None else ''
    a =  str(alternative_titles_list)
    b = a.replace('<p class="paragraph-info">', '')
    c = b.replace('<br/> </p>', '').strip()
    d = c.split('<br/>')
    light_novel_info.alternative = [e.lstrip() for e in d]

    cover_section = light_novel_page_soup.find("div", {"class": "lightnovelcovers"})
    cover_element_list = cover_section.findAll("a", {"class": "highslide"}) if cover_section is not None else []
    covers = {}
    for volume_number, cover_element in enumerate(cover_element_list, start=1):
        covers[volume_number] = "http://lndb.info/{}".format(cover_element.get("href"))

    light_novel_info.covers = covers

    return light_novel_info

def get_detail(url):
    scrape = cfscrape.create_scraper()
    match = {"href": "http://lndb.info/light_novel/"+url}
    return create_light_novel_info(match, scrape)
