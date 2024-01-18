import multiprocessing
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
import igg_games
from progress.bar import Bar
import pprint
from time import sleep
from tqdm import tqdm
import fitgirl
import concurrent.futures
import logging
from multiprocessing.pool import ThreadPool

if __name__ == '__main__':
    conn = None

    logging.basicConfig(filename='result.log',
                        encoding='utf-8', level=logging.DEBUG)
    try:
        #encode = "pe6NwpaZybKMxVIWuII7/GhwYiMtz8Ygcsb2toFWAKBYzvifFbWbp2gXV9m3MxqhHLJyX8uNlfLtAfIc9JdT9pgf4AGLMwOwqja2v8eodkEmttgDgiuSzPukxMs9L/kGzMbT5ilDBdiubggdmWjeVJi0NjyWrj35VoZZKJLeDeYARU3hPlLyPAFLqiVg+5dGiipi9TzZT2wF/lqoKSh45kWSaQ4U=="
        # print(scrape2.bluemediafiles_decodeKey(encode))
        encode = "mesrUQnEph69gHt/lINXd+qRWByj5OUX2UV4GeOHupcnryMkTXOeCvdDe87uDMlABDJyX8uNlfLtAfIc9JdT9pgf4AGLMwOwqja2v8eodkEmGjdck3ChelKTcX6/QqAbCLaDHUeNDRcHXkjTuyFo0n3oMokSxZ7SVs5/u9/3cF6os4PUS/VasBu27jKXPbIwYCVBNPcM9EVqIDmpftzaxXIQoUYs=="
        print(igg_games.bluemediafiles_decodeKey(encode))
        # bluemediafiles.com/get-url.php?url=EdevaqOMG4g9d9IALluXJBlD7edCOTMrcuOGV2U5yWqdNltg6pnUsmhlTX/qbLDUNRHkTyonooSZSs/93Fo4U/aB2jXbwCBPMEqDptaXQUs=
        conn = sqlite3.connect("database.db")
        print(sqlite3.version)
        sql_file = open("Table.sql")
        sql_as_string = sql_file.read()
        conn.executescript(sql_as_string)
        # FitGirl
        #step = 1
        # for i in tqdm(range(2, 3376,step)):
        #    fitgirl.fitgirl_games(log_file2, conn, i)

        # IGG-Games
        step = 4
        for i in tqdm(range(2, 3376, step)):
            # argslist = ((log_file, im) for im in range(step)) # Share log_file will cause unexcpected behaviour
            
            #processes = []
            #for p in range(step):
            #    temp = p + i
            #    processes.append(multiprocessing.Process(target=igg_games.scrape_igg,args=(temp,), daemon=False))
            #    processes[p].start()
            #for p in range(step):
            #    processes[p].join()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(igg_games.scrape_igg, param + i) for param in range(step)] 
                pages = [f.result() for f in futures]
                for page in pages:
                    igg_games.insert_page_into_db(conn, page)
                
            # igg_games.scrape_igg(log_file,conn,i)

            # with concurrent.futures.ProcessPoolExecutor() as executor:
            #    results = executor.map(scrape2.scrape_igg, argslist)
            #    print("First batch done")
            #scrape2.scrape_igg(log_file, conn, i)

        bar2 = Bar('RePack-Games', max=1000)
        for i in range(2, 1000):  # https://repack-games.com/
            #igg_games.repack_games(log_file2, conn, i)
            bar2.next()
        # https://fitgirl-repacks.site/page/9/
        bar2.finish()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    # Send Table.sql

    # Pull Data and parse
