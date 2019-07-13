from urllib.request import urlopen
from link_finder import LinkFinder
from setup import *


class Crawler:
    """Crawler class can be instanced to allow for multiple Crawlers to crawl the site.

    Class level variables are declared so that each instance can access the same sets of queued and crawled pages
    and wont keep crawling the same pages over and over again.
    for queue, crawled and external using sets allows no duplicates."""

    siteDirectory = ''
    baseURL = ''
    domainName = ''
    queueFile = ''
    crawledFile = ''
    externalFile = ''
    queue = set()
    crawled = set()
    external = {}

    # ------------------------------------------------------------#
    def __init__(self, siteDirectory, baseURL, domainName, ):
        """Set class  variables form inputs of instance."""
    
        Crawler.siteDirectory = siteDirectory
        Crawler.baseURL = baseURL
        Crawler.domainName = domainName
        Crawler.queueFile = Crawler.siteDirectory + '/pageQueue.txt'
        Crawler.crawledFile = Crawler.siteDirectory + '/pagesCrawled.txt'
        Crawler.externalFile = Crawler.siteDirectory + '/externalPages.txt'
    
        self.prepare()
        self.crawl_page('Prime Crawler', Crawler.baseURL)

    # ------------------------------------------------------------#
    @staticmethod
    def prepare():
        """Set up starting directory and initial files"""

        create_site_folder(Crawler.siteDirectory)
        create_site_data_files(Crawler.siteDirectory, Crawler.baseURL)

    # ------------------------------------------------------------#
    @staticmethod
    def crawl_page(threadName, pageURL):
        """Crawl the page as long as page URL is not in class crawled set.

        If it is a new page URL then:
            Attempt to add its links to the queue using gather_links function.
            Remove the current page URL from queue.
            Add current page URL to crawled set.
            Update stored files with sets to 'bank' results.
        """

        if pageURL not in Crawler.crawled and robots_check(Crawler.baseURL, pageURL):
            print('{0} now crawling {1}'.format(threadName, pageURL))
            print('Queue {0} | Crawled {1}'.format(len(Crawler.queue), len(Crawler.crawled)))
            Crawler.add_links_to_queue(Crawler.gather_links(pageURL), pageURL)
            Crawler.queue.remove(pageURL)
            Crawler.crawled.add(pageURL)
        else:
            Crawler.queue.remove(pageURL)
        Crawler.update_files()

    # ------------------------------------------------------------#
    @staticmethod
    def gather_links(pageURL):
        """Check to see if page is valid URL and then decode to string for use by LinkHunter class.

         hunter will trawl through the string HTML and create a set of links using feed."""
        HTMLString = ''

        try:
            response = urlopen(pageURL)
            if 'text/html' in response.getheader('Content-Type'):
                HTMLBytes = response.read()
                # Tried to use UTF-8 but kept failing. ISO-8859-1 seems to work okay.
                HTMLString = HTMLBytes.decode('ISO-8859-1')
            finder = LinkFinder(Crawler.baseURL, pageURL)
            finder.feed(HTMLString)

        # Basic except clause for now.
        except Exception as e:
            print('Error {}: cannot crawl page'.format(e))
            return set()
        return finder.page_links()

    # ------------------------------------------------------------#
    @staticmethod
    def add_links_to_queue(links, pageURL):
        """cycle through links found on page.

        Store new links on queue
        Store external links in dictionary
        """

        try:
            Crawler.external[pageURL]
        except KeyError:
            Crawler.external[pageURL] = []

        for URL in links:
            if URL in Crawler.queue or Crawler.crawled:
                continue
            elif Crawler.domainName not in URL:
                #External link
                Crawler.external[pageURL].append(URL)
            else:
                Crawler.queue.add(URL)

    # ------------------------------------------------------------#
    @staticmethod
    def update_files():
        """Back-up/Update crawled and queue files with latest update for other threads"""
        set_to_file(Crawler.queue, Crawler.queueFile)
        set_to_file(Crawler.crawled, Crawler.crawledFile)
        external_to_file(Crawler.external, Crawler.externalFile)

