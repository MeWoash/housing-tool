from html_parser.parser import parse
from common.time_manager import timeit
# from web_scraper import web_scraper

@timeit
def html_parser_main():
    parse()

html_parser_main()