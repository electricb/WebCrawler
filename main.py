import threading
from queue import Queue

from crawler import Crawler
from domain import *
from setup import *

SITE_NAME = 'memset'
HOMEPAGE = 'https://www.memset.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = SITE_NAME + '/pageQueue.txt'
CRAWLED_FILE = SITE_NAME + '/pagesCrawled.txt'
# Just picking 1 for now. More research needed to determine restrictions of threads
NUMBER_OF_THREADS = 1

queue = Queue()
Crawler(SITE_NAME, HOMEPAGE, DOMAIN_NAME)

# ------------------------------------------------------------#
def create_workers():
    """Spider threads will die when main exits"""

    for worker in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=work)
        thread.daemon = True
        thread.start()

# ------------------------------------------------------------#
def work():
    """Do the next job in the queue"""

    while True:
        URL = queue.get()
        Crawler.crawl_page(threading.current_thread().name, URL)
        queue.task_done()

# ------------------------------------------------------------#
def create_jobs():
    """Each queued link is a new job"""

    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

# ------------------------------------------------------------#
def crawl():
    """Check if there are items in the queue and if so, crawl them"""
    queuedLinks = file_to_set(QUEUE_FILE)

    if queuedLinks:
        print('{0} links in the queue'.format(len(queuedLinks)))
        create_jobs()

# ------------------------------------------------------------#
def build_site_map():
    set_output(SITE_NAME , HOMEPAGE)


create_workers()
crawl()
build_site_map()
