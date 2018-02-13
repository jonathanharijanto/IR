import logging
from datamodel.search.QiushibaiAvinashkumarKyungwoohyunJonathanharijanto_datamodel import QiushibaiAvinashkumarKyungwoohyunJonathanharijantoLink, OneQiushibaiAvinashkumarKyungwoohyunJonathanharijantoUnProcessedLink, add_server_copy, get_downloaded_content
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter, ServerTriggers
from lxml import html,etree
import re, os
from time import time
from uuid import uuid4

from urlparse import urlparse, parse_qs
from uuid import uuid4
import tldextract

logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"

@Producer(QiushibaiAvinashkumarKyungwoohyunJonathanharijantoLink)
@GetterSetter(OneQiushibaiAvinashkumarKyungwoohyunJonathanharijantoUnProcessedLink)
@ServerTriggers(add_server_copy, get_downloaded_content)
class CrawlerFrame(IApplication):

    def __init__(self, frame):
        self.starttime = time()
        self.app_id = "QiushibaiAvinashkumarKyungwoohyunJonathanharijanto"
        self.frame = frame


    def initialize(self):
        self.count = 0
        l = QiushibaiAvinashkumarKyungwoohyunJonathanharijantoLink("http://www.ics.uci.edu/")
        print l.full_url
        self.frame.add(l)

    def update(self):
        unprocessed_links = self.frame.get(OneQiushibaiAvinashkumarKyungwoohyunJonathanharijantoUnProcessedLink)
        if unprocessed_links:
            link = unprocessed_links[0]
            print "Got a link to download:", link.full_url
            downloaded = link.download()
            links = extract_next_links(downloaded)
            for l in links:
                if is_valid(l):
                    self.frame.add(QiushibaiAvinashkumarKyungwoohyunJonathanharijantoLink(l))

    def shutdown(self):
        print (
            "Time time spent this session: ",
            time() - self.starttime, " seconds.")
    
def extract_next_links(rawDataObj):
    outputLinks = []
    subdomainslist = []
    invalidlinks = 0
    '''
    rawDataObj is an object of type UrlResponse declared at L20-30
    datamodel/search/server_datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded. 
    The frontier takes care of that.
    Suggested library: lxml
    '''
    # Count the # of invalid links
    if rawDataObj.http_code != 200:
        invalidlinks += 1
    elif rawDataObj.http_code == 200:
        # Parse the document from the given input
        root = html.fromstring(rawDataObj.content)
        # Extract the content of a tree (specifically, href)
        urls = root.xpath("//a/@href")
        # ======= Debugging purpose =======
        print "The list of RAW links (extracted directly from content):"
        print urls
        # =================================
        # Go through each url
        for url in urls:
            # Parse into (scheme, netloc, path, params, query, fragment)
            parsed = urlparse(rawDataObj.url)
            # Concatenate the "url"
            if "http" in url or "https" in url:
                outputLinks.append(url)
                # Get the subdomain from a link
                extractedsubdom = tldextract.extract(url).subdomain
                # Remove any subdomain that's empty or just "www"
                if extractedsubdom != '' and extractedsubdom != 'www':
                    # trim the "www" from the subdomain
                    subdomainslist.append(extractedsubdom.replace("www.",''))
            else:
                # Replace any "./path" into "/path"
                if url[0] == '.':
                    url = url.replace(".", "")
                cleanurl = parsed.scheme + '://' + parsed.netloc + url
                outputLinks.append(cleanurl)
                extractedsubdom = tldextract.extract(cleanurl).subdomain
                if extractedsubdom != '' and extractedsubdom != 'www':
                    subdomainslist.append(extractedsubdom.replace("www.",''))
        print "The list of VALID (absolute form) links:"
        print outputLinks
        print "The list of subdomains:"
        print subdomainslist
        print "The number of out links: " + str(len(outputLinks))
    return outputLinks

def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be
    downloaded or not.
    Robot rules and duplication rules are checked separately.
    This is a great place to filter out crawler traps.
    '''
    parsed = urlparse(url)
    if parsed.scheme not in set(["http", "https"]):
        return False
    try:
        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False