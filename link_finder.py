from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):

    # ------------------------------------------------------------#
    def __init__(self, baseURL, pageURL, ):
        """Constructor to call inherited constructor then assign class objects"""

        super().__init__()
        self.baseURL = baseURL
        self.pageURL = pageURL
        self.links = set()
        self.data = set()

    # ------------------------------------------------------------#
    def handle_starttag(self, tag, attrs):
        """Identify start tag for link 'href' and add link to links object.

        Use baseURL where relative URLs are encountered.
        """

        if tag == 'a':
            for attribute, value in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.baseURL, value)
                    self.links.add(url)

    # ------------------------------------------------------------#
    def page_links(self, ):
        """Return links object."""
        return self.links

    # ------------------------------------------------------------#
    def return_data(self, ):
        return self.data

    # ------------------------------------------------------------#
    def error(self, message):
        pass
