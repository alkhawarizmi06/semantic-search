import requests
from bs4 import BeautifulSoup
from search_logging import get_logger

logger = get_logger(__name__)

def get_all_entries_from_xml(url) :
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    r = requests.get(url, headers=headers)

    logger.info (f"retrieved page is {r}")
    soup = BeautifulSoup(r.text, "xml")

    logger.info (f"retrieved soup is {soup}")

    # URLS
    all_url_tags = soup.find_all("url")
    allUrls = []
    for urls in all_url_tags :
        allUrls.append(urls.findNext("loc").text)

    # SITEMAPS
    sitemapList = soup.find_all("sitemap")
    allSitemaps = []
    for sitemap in sitemapList:
        allSitemaps.append(sitemap.findNext("loc").text)

    return ({"sitemaps" : allSitemaps, "urls" : allUrls})

def get_urls(url) :
    xml = get_all_entries_from_xml(url)
    print(xml)
    allUrls = xml['urls']
    sitemaps = xml['sitemaps']
    visitedSitemaps = []

    while (sitemaps) :
        for sitemap in sitemaps :
            if sitemap not in visitedSitemaps :
                visitedSitemaps.append(sitemap)
                xml = get_all_entries_from_xml(sitemap)
                sitemaps.extend(xml['sitemaps'])

                for elt in xml['urls'] :
                    allUrls.append(elt)
            else :
                sitemaps.remove(sitemap)

    return(allUrls)


