class Config:
    nutch_header = {'user-gent': 'Nutch'}
    ache_header = {'user-agent': 'ACHE'}
    google_header = {'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    browser_header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'}
    bing_header = {'user-agent': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
    empty_header = {'user-agent': ''}
    HEADERS ={'google':google_header, 'browser':browser_header, 'ache':ache_header, 'nutch':nutch_header, 'bing':bing_header, 'empty':empty_header}
    
    TOR_PROXY = {"http":"http://127.0.0.1:8118"} #This is used for crawling with TOR

    PROCESS_NUMBER = 64

    USE_TOR = False

    DATA_FORMAT = "ONE_FILE"
    #DATA_FORMAT = "MULTI_FILE"

    SAVE_HTML = True
