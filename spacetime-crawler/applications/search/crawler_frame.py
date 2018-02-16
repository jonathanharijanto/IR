import logging
from datamodel.search.QiushibaiAvinashkumarKyungwoohyunJonathanharijanto_datamodel import QiushibaiAvinashkumarKyungwoohyunJonathanharijantoLink, OneQiushibaiAvinashkumarKyungwoohyunJonathanharijantoUnProcessedLink, add_server_copy, get_downloaded_content
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter, ServerTriggers
from lxml import html,etree
import re, os
from time import time
from uuid import uuid4

from urlparse import urlparse, parse_qs, urljoin
from uuid import uuid4
import tldextract

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(filename='output.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"

PagesCounter = 0
outlinksCounter = 0
sd_dictionary = {}
pagemostoutlinks = ""

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
            logging.info("Got a link to download:" + link.full_url)
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
    global PagesCounter
    global outlinksCounter
    global sd_dictionary
    global pagemostoutlinks

    print "Totally crawled pages: ", PagesCounter
    logging.info("Totally crawled pages: " + str(PagesCounter))

    outputLinks = []
    invalidlinks = 0

    #print "rawDataObj.url = ", rawDataObj.url
    #print "rawDataObj.content", rawDataObj.content
    #print "rawDataObj.error_message = ", rawDataObj.error_message
    #print "rawDataObj.headers = ", rawDataObj.headers
    #print "rawDataObj.http_code = ", rawDataObj.http_code
    #print "rawDataObj.is_redirected = ", rawDataObj.is_redirected
    #print "rawDataObj.final_url = ", rawDataObj.final_url

    #try:
    #    logging.info("rawDataObj.url = " + str(rawDataObj.url))
    #    logging.info("rawDataObj.content = " + str(rawDataObj.content))
    #    logging.info("rawDataObj.error_message = " + str(rawDataObj.error_message))
    #    logging.info("rawDataObj.headers = " + str(rawDataObj.headers))
    #    logging.info("rawDataObj.http_code = " + str(rawDataObj.http_code))
    #    logging.info("rawDataObj.is_redirected = " + str(rawDataObj.is_redirected))
    #    logging.info("rawDataObj.final_url = " + str(rawDataObj.final_url))
    #except TypeError:
    #    print ("TypeError for logging: ", TypeError.message)

    try:
        # If http status code is OK
        if rawDataObj.http_code == 200:

            PagesCounter = PagesCounter + 1

            # Get the subdomain of the url being visited
            subdomain = extract_subdomain(rawDataObj.url)

            # Parse the document from the given input
            root = html.fromstring(rawDataObj.content)
            # Extract the content of a tree (specifically, href)
            urls = root.xpath("/html/body//a/@href")

            print "The list of RAW links (extracted directly from content):"
            print urls

            for url in urls:
                outputLinks.append(urljoin(rawDataObj.url, url))

            print "The list of VALID (absolute form) links:"
            logging.info("The list of VALID (absolute form) links:")
            print '\n'.join(outputLinks)
            logging.info('\n'.join(outputLinks))
            #print "The list of sub domains:"
            #logging.info("The list of sub domains:")
            #print '\n'.join(subdomainlist)
            #logging.info('\n'.join(subdomainlist))

            # ANALYTICS 2 - Find the page with the most outlinks
            if outlinksCounter < len(outputLinks):
                outlinksCounter = len(outputLinks)
                pagemostoutlinks = rawDataObj.url
            print "The number of out links: " + str(len(outputLinks))
            logging.info("The number of out links: " + str(len(outputLinks)))
            print "The most out links (so far): " + str(outlinksCounter)
            print "The page name is: " + pagemostoutlinks
            logging.info("The most out links (so far): " + str(outlinksCounter))
            logging.info("The page name is: " + pagemostoutlinks)

            # ANALYTIC 1 - keep track all the subdomains visited + URLs processed from each subdomains
            if subdomain != '' and subdomain != 'www':
                if subdomain in sd_dictionary:
                    sd_dictionary[subdomain] += len(outputLinks)
                else:
                    sd_dictionary[subdomain] = len(outputLinks)
            print "Dictionary's content: "
            print sd_dictionary
            logging.info("The dictionary content: ", sd_dictionary)

        # If http status code is NOT OK
        else:
            invalidlinks += 1
        # ANALYTICS 3 - Count invalid links from the frontier
        print "The number of INVALID links: " + str(invalidlinks)
        logging.info("The number of INVALID links: " + str(invalidlinks))

        return outputLinks

    except TypeError:
        print ("TypeError : ", TypeError.message)
        return outputLinks

    except Exception as e:
        print ("OtherError : ", e.message)
        return outputLinks


# New (sub)Function to extract subdomain
def extract_subdomain(url):
    if "http://" in url or "https://" in url:
        extract = tldextract.extract(url).subdomain
        return extract.replace("www.", '')
    return


def is_valid(url):

    message = ""

    result = False

    '''
    Function returns True or False based on whether the url has to be
    downloaded or not.
    Robot rules and duplication rules are checked separately.
    This is a great place to filter out crawler traps.

    Reference:
    https://support.archive-it.org/hc/en-us/articles/208332963-Modify-your-crawl-scope-with-a-Regular-Expression#InvalidURLs
    1. Long Invalid URLs
    2. Repeating Directories
    3. Extra Directories
    4. Calendars
    '''

    # Get original url string
    if type(url) == str:
        # Ignore errors even if the string is not proper UTF-8 or has
        # broken marker bytes.
        # Python built-in function unicode() can do this.
        original = unicode(url, "utf-8", errors="ignore")
    else:
        # Assume the value object has proper __unicode__() method
        original = unicode(url)

    message += "Validating url: [" + original + "]"

    parsed = urlparse(url)

    # print "Validating url: [", original, "]"
    # print "Parsed url: ", str(parsed)
    # try:
        # logging.info("Validating url: [" + original + "]")
        # logging.info("Parsed url: " + parsed)
    # except TypeError:
    #    print ("TypeError for logging: ", TypeError.message)

    if parsed.scheme not in set(["http", "https"]):
        # print "[x][http, https]"
        # logging.info("[x][http, https]")
        message += " [x] reason: [http https]"
        result = False

        print message
        logging.info(message)

        return result

    try:
        result = ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4"
                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z"
                + "|psd|dmg|iso|epub|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv"
                + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())\
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4"
                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z"
                + "|psd|dmg|iso|epub|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv"
                + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", original.lower())\
            and not re.match("^.*calendar.*$", parsed.path.lower()) \
            and not re.match("^.*calendar.*$", original.lower()) \
            and not re.match("^.*/[^/]{200,}$", parsed.path) \
            and not re.match("^.*/[^/]{300,}$", original) \
            and not re.match("^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", parsed.path.lower())\
            and not re.match("^.*(/misc|/sites|/all|/themes|/modules|/profiles|/css|/field|/node|/theme){3}.*$", parsed.path.lower())

        # For logging the reasons.
        violation0 = ".ics.uci.edu" in parsed.hostname

        # Based on path
        violation1p = not re.match(".*\.(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4"
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z"
            + "|psd|dmg|iso|epub|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv"
            + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

        # Based on original
        violation1o = not re.match(".*\.(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4"
                                  + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                                  + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z"
                                  + "|psd|dmg|iso|epub|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv"
                                  + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", original.lower())

        # Based on path
        violation2p = not re.match("^.*calendar.*$", parsed.path.lower())

        # Based on original
        violation2o = not re.match("^.*calendar.*$", original.lower())

        # Based on path
        violation3p = not re.match("^.*/[^/]{200,}$", parsed.path)

        # Based on original
        violation3o = not re.match("^.*/[^/]{300,}$", original)

        violation4 = not re.match("^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", parsed.path.lower())

        violation5 = re.match("^.*(/misc|/sites|/all|/themes|/modules|/profiles|/css|/field|/node|/theme){3}.*$", parsed.path.lower())

        if violation0 is False:
            # print "[x][.ics.uci.edu]"
            # logging.info("[x][.ics.uci.edu]")
            message += "[x] reason: [.ics.uci.edu]"
        if violation1p is False:
            # print "[x][path][file suffixes]"
            # logging.info("[x][path][file suffixes]")
            message += "[x] reason: [path][file suffixes]"
        if violation1o is False:
            # print "[x][original][file suffixes]"
            # logging.info("[x][original][file suffixes]")
            message += "[x] reason: [original][file suffixes]"
        if violation2p is False:
            # print "[x][path][Calendars]"
            # logging.info("[x][path][Calendars]")
            message += "[x] reason: [path][Calendars]"
        if violation2o is False:
            # print "[x][original][Calendars]"
            # logging.info("[x][original][Calendars]")
            message += "[x] reason: [original][Calendars]"
        if violation3p is False:
            # print "[x][path][Long Invalid URLs]"
            # logging.info("[x][path][Long Invalid URLs]")
            message += "[x] reason: [path][Long Invalid URLs]"
        if violation3o is False:
            # print "[x][original][Long Invalid URLs]"
            # logging.info("[x][original][Long Invalid URLs]")
            message += "[x] reason: [original][Long Invalid URLs]"
        if violation4 is False:
            # print "[x][Repeating Directories]"
            # logging.info("[x][Repeating Directories]")
            message += "[x] reason: [Repeating Directories]"
        if violation5 is False:
            # print "[x][Extra Directories]"
            # logging.info("[x][Extra Directories]")
            message += "[x] reason: [Extra Directories]"

        if result is True:
            # print "[o] valid! "
            # logging.info("[o] valid! ")
            message += "[o] valid!"

        print message
        logging.info(message)

        return result

    except TypeError:
        print ("TypeError for ", parsed)
        print ("TypeError: ", TypeError.message)
        logging.error("TypeError: ", TypeError.message)
        return False
    except Exception as e:
        print ("OtherError: ", e.message)
        logging.error("OtherError: ", e.message)
        return False
