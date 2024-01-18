from io import TextIOWrapper
import multiprocessing
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import logging
# input: pe6NwpaZybKMxVIWuII7/GhwYiMtz8Ygcsb2toFWAKBYzvifFbWbp2gXV9m3MxqhHLJyX8uNlfLtAfIc9JdT9pgf4AGLMwOwqja2v8eodkEmttgDgiuSzPukxMs9L/kGzMbT5ilDBdiubggdmWjeVJi0NjyWrj35VoZZKJLeDeYARU3hPlLyPAFLqiVg+5dGiipi9TzZT2wF/lqoKSh45kWSaQ4U==
# output: https://bluemediafiles.com/get-url.php?url=EdevaqOMG4g9d9IALluXJHqMmVgpWFizBAFtbcYzMYh/IuIxKyaw6pSPkM9/GMTiDdugdWeJ0jWj5oZJeeAUhlyALig5GiiTZ2FloS4kSQU=


def bluemediafiles_decodeKey(encoded: str):
    key = ''
    i = int(len(encoded) / 2 - 5)
    # i = i - 2
    while i >= 0:
        key += encoded[i]
        i = i - 2
    i = int(len(encoded) / 2 + 4)
    # i = i - 2
    while i < len(encoded):
        key += encoded[i]
        i = i + 2
    return key


def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

# https://repack-games.com/page/2/


def repack_games(log_file: TextIOWrapper, conn, pageNum: int):
    r = Request("https://repack-games.com/page/{0}/".format(
        pageNum), headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(r).read()
    bs = BeautifulSoup(html, "html.parser")
    articles = bs.findAll("ul", class_="modern-articles")
    for article in articles:
        result = str(article).find("https://repack-games.com/")
        if result != -1:
            print(str(article)[result:])


# Scrape Meta data, and Games from IGG-Games,
# Then upload the result to database.


def scrape_igg(pageNum: int):
    page = [dict, list]
    r = Request(
        'https://igg-games.com/page/{0}'.format(pageNum), headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(r).read()
    bs = BeautifulSoup(html, "html.parser")
    nameList = bs.findAll('article')
    # <article
    # <meta          Name
    # <meta          Uploader
    # <meta          Timestamp
    # <meta          Publisher
    # <div           Image
    # <h2            Download Link
    # <p             Genre
    for name in nameList:
        logging.debug(name.get_text())
        ls = []
        for a in name:
            # .replace("\\", "").replace(",","").replace("'", "").replace('"',"").replace("<","").replace(">","")
            ls.append(str(a))
        game_links = igg_games_scrape_game(str(ls[11]))
        ls[1] = ls[1].replace('<meta content="', "").replace(
            ' Free Download" property="name"/>', "")
        # ALl are posted by admin lol.
        name = ls[1]

        page.append((game_links, ls))
        logging.debug('__________________________________________________')
        continue
        conn.execute("INSERT INTO game_entry VALUES(?,?,?,?,?,?,?,?)",
                     (name, ls[3], ls[5].replace('<meta content="', "").replace('" property="dateModified"/>', ""), ls[7], ls[9], ls[11], ls[13], ls[15]))
        conn.execute("INSERT OR REPLACE INTO game_links(name,megaup_net,mega_nz,fichier1_com,gofile_io,anonFiles_com,rapidgator_net,uptobox_com,clicknupload_to,pixeldrain_com,torrent) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (
            name,
            '|'.join(game_links["megaup_net"], ),
            '|'.join(game_links["mega_nz"]),
            '|'.join(game_links["fichier1_com"]),
            '|'.join(game_links["gofile_io"]),
            '|'.join(game_links["anonFiles_com"]),
            '|'.join(game_links["rapidgator_net"]),
            '|'.join(game_links["uptobox_com"]),
            '|'.join(game_links["clicknupload_to"]),
            '|'.join(game_links["pixeldrain_com"]),
            '|'.join(game_links["torrent"])))
        conn.commit()
        log_file.write('__________________________________________________')
    return page


def insert_page_into_db(conn, page):
    for item in page[2:]:
        game_links = item[0]
        ls = item[1]
        conn.execute("INSERT INTO game_entry VALUES(?,?,?,?,?,?,?,?)",
                 (ls[1], ls[3], ls[5].replace('<meta content="', "").replace('" property="dateModified"/>', ""), ls[7], ls[9], ls[11], ls[13], ls[15]))
        conn.execute("INSERT OR REPLACE INTO game_links(name,megaup_net,mega_nz,fichier1_com,gofile_io,anonFiles_com,rapidgator_net,uptobox_com,clicknupload_to,pixeldrain_com,torrent) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (
        ls[1],
        '|'.join(game_links["megaup_net"], ),
        '|'.join(game_links["mega_nz"]),
        '|'.join(game_links["fichier1_com"]),
        '|'.join(game_links["gofile_io"]),
        '|'.join(game_links["anonFiles_com"]),
        '|'.join(game_links["rapidgator_net"]),
        '|'.join(game_links["uptobox_com"]),
        '|'.join(game_links["clicknupload_to"]),
        '|'.join(game_links["pixeldrain_com"]),
        '|'.join(game_links["torrent"])))
        conn.commit()
# Download links


# Translate web address to programmatically string
# megaup_net
# mega_nz
# fichier1_com
# gofile_io
# anonFiles_com
# rapidgator_net
# uptobox_com
# clicknupload_to
# pixeldrain_com
# torrent
def website_translate(link: str):
    if link.find("megaup.net") != -1:
        return "megaup_net"
    if link.find("mega.nz") != -1:
        return "mega_nz"
    if link.find("1fichier.com") != -1:
        return "fichier1_com"
    if link.find("gofile.io") != -1:
        return "gofile_io"
    if link.find("anonfiles.com") != -1:
        return "anonFiles_com"
    if link.find("rapidgator.net") != -1:
        return "rapidgator_net"
    if link.find("uptobox.com") != -1:
        return "uptobox_com"
    if link.find("clicknupload.to") != -1:
        return "clicknupload_to"
    if link.find("pixeldrain.com") != -1:
        return "pixeldrain_com"
    if link.find("magnet:?xt") != -1:
        return "torrent"
    raise Exception("link does not have a supported source: {0}".format(link))


    # Link TusFiles
    # link Openload.co
DownloadLinksList = [
    "megaup_net",
    "mega_nz",
    "fichier1_com",
    "gofile_io",
    "anonFiles_com",
    "rapidgator_net",
    "uptobox_com",
    "clicknupload_to",
    "pixeldrain_com",
    "torrent"
]


def all_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)


def igg_games_scrape_game(game: str):
    DownloadLinks = dict.fromkeys(DownloadLinksList, [])
    # Need to read label to get source because it's different.
    start = game.find("https://igg-games")
    end = game.find('">', start)
    d = game[start:end]
    r = Request(d, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(r).read()
    bs = BeautifulSoup(html, "html.parser")
    links = []
    index = 0
    part_int = 1
    # normal links, bluemedia files only
    for link in bs.find_all("a", href=lambda href: href and "https://bluemediafiles.homes/url-generator.php?url=" in href):
        lk = str(link)
        start = lk.find(
            "https://bluemediafiles.homes/url-generator.php?url=")
        end = lk.find('"', start)
        htt = lk[start:end]
        # <a href="https://bluemediafiles.homes/url-generator.php?url=KH1TK0eBXmDmljELeo4C+Bzvk/di79ViuP78lQFtN7JFlyd8S5KXVbQo1OqNmvQpUwXoGXWsOLLwAUGYifbWDA==" rel="noopener" target="_blank">Download HERE</a>
        links.append(htt)
        logging.debug(htt)
    argslist = ((link, DownloadLinks) for link in links)
    with multiprocessing.Pool(len(links)) as pool:
        results = pool.map(scrape_bluemedia, links)
        for l in results:
            if l is None:
                # Web Request Error 404 most likely, just continue.
                continue
            finalLink = str(l)
            ls = DownloadLinks[website_translate(finalLink)]
            if len(ls) == 0:
                DownloadLinks[website_translate(finalLink)] = [finalLink]
            else:
                DownloadLinks[website_translate(finalLink)].append(finalLink)

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #    DownloadLinks = executor.map(scrape_bluemedia_thunk, argslist)

    # torrent link
    for link in bs.find_all("a",  href=lambda href: href and ("pcgamestorrents.com" or "pcgamestorrents.org") in href):
        # https://pcgamestorrents.com
        # http://dl.pcgamestorrents.org
        # Always seems to have "Torrent Link" in text with property.

        # get url from string
        lk = str(link)
        start = lk.find("https")
        temp = lk[start:]
        ends = []
        ends.append(temp.find('" target='))
        ends.append(temp.find('" rel'))
        ends.sort()
        ends = remove_values_from_list(ends, -1)
        # check path of url
        url = urlparse(temp[:ends[0]])
        if url.path == ("/" or ""):
            continue
        logging.debug("Torrent: " + url.geturl())
        DownloadLinks["torrent"] = [url.geturl()]
    return DownloadLinks

# Returns the link from blue media


def scrape_bluemedia_thunk(link: str, DownloadLinks):
    finalLink = str(scrape_bluemedia(link))
    ls = DownloadLinks[website_translate(finalLink)]
    if len(ls) == 0:
        DownloadLinks[website_translate(finalLink)] = [finalLink]
    else:
        DownloadLinks[website_translate(finalLink)].append(finalLink)
    return DownloadLinks


def scrape_bluemedia(link):
    r = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    url = None
    try: 
        html = urlopen(r).read()        
        bs = BeautifulSoup(html, "html.parser")
        for lin in bs.find_all("script"):
            s = str(lin)
            start = s.find('Goroi_n_Create_Button("')
            if start != -1:  # Found it
                end = s.find(")", start)
                if end > start:
                    encode = s[start + len('Goroi_n_Create_Button("'):end - 1]
                    lin = "https://bluemediafiles.com/get-url.php?url=" + \
                        bluemediafiles_decodeKey(encode)
                    req = Request(lin, headers={'User-Agent': 'Mozilla/5.0'})
                    try:
                        url = urlopen(req).geturl()
                    except:
                        return None
                    finally:
                        return url

                else:
                    raise Exception("Error parsing Goroi_n_Create_Button")
    except:
        return None
    finally:
        return url
