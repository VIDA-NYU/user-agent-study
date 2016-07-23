import requests
import sys
from multiprocessing import Process, Queue
import urllib2
import traceback
import time
import os
import socket
#import urllib3
import os.path
from os import listdir
import shutil
import json
from urlutility import URLUtility
from config import Config

'''
@author: Kien Pham (kien.pham@nyu.edu or kienpt.vie@gmail.com)
The script sends requests to urls listed in in_file
'''

#How to crawl with TOR: http://sacharya.com/crawling-anonymously-with-tor-in-python/ 

requests.packages.urllib3.disable_warnings()

def headers2str(h):
    ret = ""
    if 'content-length' in h:
        ret += h['content-length']
    if 'set-cookie' in h:
        ret += "\t" + h['set-cookie']
    if 'date' in h:
        ret += h['date']
    ret = ret.strip("\t")

def save_response(url, encoded_url, status_code, exception, res_headers, agent, url_obj, f):
    try:
        item = {}
        item["url"] = url
        item["encoded_url"] = encoded_url
        item["user-agent"] = agent
        item["url_meta"] = url_obj["url_meta"] 
        if status_code:
            item['status_code'] = status_code
        if res_headers:
            #Note that res_headers can not be serialized to json so we need to convert it first
            h = {}
            for key in res_headers:
                try:
                    h[key] = res_headers[key].encode('utf-8')
                except:
                    h[key] = res_headers[key].decode('cp1252')
                    h[key] = h[key].encode('utf-8')
            item['header'] = h
        if exception:
            item['exception'] = exception
        json.dump(item, f)
        f.write("\n")
    except:
        print "EXCEPTION in save_response, " + url
        traceback.print_exc()

def save_content_one_file(content_file):
    def save_content(url, res):
        data = {}
        data["url"] = url
        text = res.text.encode('utf-8')
        data["text"] = text
        json.dump(data, content_file)
        content_file.write("\n")
    return save_content

def save_content_multi_file(html_dir):
    def save_content(url, res):
        html_filename = html_dir + "/" + URLUtility.encode(url) + ".html"
        html_file = open(html_filename, "w")
        text = res.text.encode('utf-8')
        html_file.write(text)
        html_file.close()
    return save_content

def crawlprocess(url_objects, start, html_dir, status_dir, agent):
    status_file = open(status_dir + "/status_temp_" + str(start) + ".json", "w")
    content_file = None
    if Config.DATA_FORMAT == "ONE_FILE":
        content_file = open(html_dir  + "/html_" + str(start) + ".json", "a+")
        save_content = save_content_one_file(content_file)
    elif Config.DATA_FORMAT == "MULTI_FILE":
        save_content = save_content_multi_file(html_dir)

    for i in range(start, len(url_objects), Config.PROCESS_NUMBER):
        url_obj = url_objects[i]
        url = url_obj["url"] 
        try:
            if Config.USE_TOR:
                res = requests.get(url, headers=Config.HEADERS[agent], proxies=TOR_PROXY, verify=False, timeout=5)
            else:
                res = requests.get(url, headers=Config.HEADERS[agent], verify=False, timeout=5)
            if Config.SAVE_HTML:
                save_content(url, res)
            save_response(url, URLUtility.encode(url), str(res.status_code), None, res.headers, agent, url_obj, status_file)
        except requests.ConnectionError:
            #In the event of a network problem (e.g. DNS failure, refused connection, etc)
            save_response(url, URLUtility.encode(url), None, "ConnectionError", None, agent, url_obj, status_file)
        except requests.HTTPError:
            #In the rare event of an invalid HTTP response
            save_response(url, URLUtility.encode(url), None, "HTTPError", None, agent, url_obj, status_file)
        except requests.Timeout:
            save_response(url, URLUtility.encode(url), None, "Timeout", None, agent, url_obj, status_file)
        except requests.TooManyRedirects:
            save_response(url, URLUtility.encode(url), None, "TooManyRedirects", None, agent, url_obj, status_file)
        except Exception:
            save_response(url, URLUtility.encode(url), None, "OtherExceptions", None, agent, url_obj, status_file)
    status_file.close()
    if content_file:
        content_file.close()

def aggregate(status_dir, status_file):
    #Read all files in status_dir and write their content to status_file
    out = open(status_file, "w")
    files = listdir(status_dir)
    for f in files:
        with open(status_dir + "/" + f) as lines:
            for line in lines:
                out.write(line)
    out.close()

def merge(status_dir, status_file):
    #Merge non-exception line in status_file and all files in status_dir
    count = 0
    buff_status = []
    with open(status_file) as lines:
        for line in lines:
            try:
                json_data = json.loads(line)
                if "exception" in json_data:
                    count += 1
                else:
                    buff_status.append(line)
            except:
                continue
    print "Number of Exceptions before recrawl: " + str(count)

    count = 0
    out = open(status_file, "w")
    for line in buff_status:
        out.write(line)
    files = listdir(status_dir)
    for f in files:
        with open(status_dir + "/" + f) as lines:
            for line in lines:
                try:
                    json_data = json.loads(line)
                    if "exception" in json_data:
                        count += 1
                    out.write(line)
                except:
                    continue
    print "Number of Exceptions after recrawl: " + str(count)
    out.close()   

#def crawl(in_file, out_dir, q):
def crawl(in_file, html_dir, status_dir, agent):
    urls = set()
    url_objects = []
    with open(in_file) as lines:
        for line in lines:
            values = line.strip("\n").split("\t")
            url_object = {"url_meta":{}}
            if len(values) == 4:
                url_object["url_meta"]["topic"] = values[0]
                url_object["url_meta"]["site"] = values[1]
                url = URLUtility.normalize(values[2])
                url_object["url"] = url 
                url_object["url_meta"]["subtopic"] = values[3]

            else:
                url = URLUtility.normalize(values[0])
                url_object["url"] = url 
            if url not in urls:
                urls.add(url)
                url_objects.append(url_object)              
    jobs = []
    for i in range(Config.PROCESS_NUMBER):
        p = Process(target = crawlprocess, args = (url_objects, i, html_dir, status_dir, agent))
        jobs.append(p)
        p.start()
    for p in jobs:
        p.join()

def recrawl(status_file, html_dir, status_dir, agent):
    #Read the status_file, recrawl the website that causes exception
    url_objects = []
    with open(status_file) as lines:
        for line in lines:
            try:
                json_data = json.loads(line)
                url_object = {}
                if "exception" in json_data:
                    url_object["url"] = json_data["url"]
                    url_object["url_meta"] = json_data["url_meta"]
                    url_objects.append(url_object)
            except:
                print "recrawl exception"
                traceback.print_exc()
                continue
    
    jobs = []
    for i in range(Config.PROCESS_NUMBER):
        p = Process(target = crawlprocess, args = (url_objects, i, html_dir, status_dir, agent))
        jobs.append(p)
        p.start()
    for p in jobs:
        p.join()   

def custom_recrawl(status_file, supplement_status_file, html_dir, status_dir, agent):
    #Read the status_file, recrawl the website that causes exception

    downloaded_urls = set()
    with open(status_file) as lines:
        for line in lines:
            try:
                json_data = json.loads(line)
                if "exception" in json_data:
                    continue
                downloaded_urls.add(json_data['url'])
            except:
                print "recrawl exception"
                traceback.print_exc()
                continue
 
    url_objects = []
    with open(supplement_status_file) as lines:
        for line in lines:
            try:
                values = line.strip("\n").split("\t")
                url = URLUtility.normalize(values[2])
                if url not in downloaded_urls:
                    url_object = {"url_meta":{}}
                    url_object["url_meta"]["topic"] = values[0]
                    url_object["url_meta"]["site"] = values[1]
                    url_object["url_meta"]["subtopic"] = values[3]
                    url_object["url"] = url 
                    url_objects.append(url_object)
            except:
                print "custom recrawl exception"
                traceback.print_exc()
                continue
    print "Number of urls to download: " + str(len(url_objects))
    jobs = []
    for i in range(Config.PROCESS_NUMBER):
        p = Process(target = crawlprocess, args = (url_objects, i, html_dir, status_dir, agent))
        jobs.append(p)
        p.start()
    for p in jobs:
        p.join()   

if __name__=="__main__":
    if len(sys.argv) < 5:
        print "Wrong argument"
        print "[url_file] [html_output_dir] [status_output_file] [agent] [crawlmode] [useTor] [saveHTML] [supplement_status_file]"
        print "agent: [google, browser, ache, nutch, bing, empty]"
        print "crawlmode: [first, recrawl, custom_recrawl]; default: first"
        print "useTor: [yes, no]; default: no"
        print "saveHTML: [yes, no]; default: no"
        sys.exit(0)

    #READING PARAMETERS
    in_file = sys.argv[1]     #input
    html_dir = sys.argv[2]    #output
    status_file = sys.argv[3] #output
    agent = sys.argv[4]
    if len(sys.argv) >= 6:
        crawl_mode = sys.argv[5]
    else:
        crawl_mode = "first" #default

    if len(sys.argv) >=7: 
        if sys.argv[6] == "yes":
            Config.USE_TOR = True

    if len(sys.argv) >= 8:
        if sys.argv[7] == "yes":
            Config.SAVE_HTML = True

    if agent not in Config.HEADERS:
        print "agent is wrong, it must be " + str(Config.HEADERS.keys())
        sys.exit(0)

    status_dir = "status_temp"#temporary directory, it will be deleted 
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    
    if not os.path.exists(status_dir):
        os.makedirs(status_dir)

    start = time.time()
    if crawl_mode == "first":
        crawl(in_file, html_dir, status_dir, agent)
        aggregate(status_dir, status_file) #aggregate all files in status_dir to single file

    elif crawl_mode == "recrawl":
        recrawl(status_file, html_dir, status_dir, agent)
        merge(status_dir, status_file) #Remove all exception in status_file, update all files in status_dir to status_file. status_file is both input and output

    elif crawl_mode == "custom_recrawl":
        supplement_status_file = sys.argv[8]
        custom_recrawl(status_file, supplement_status_file, html_dir, status_dir, agent)
        merge(status_dir, status_file) #Remove all exception in status_file, update all files in status_dir to status_file. status_file is both input and output


    shutil.rmtree(status_dir, ignore_errors=True) #Delete the temporary directory after aggregation
    end = time.time()
    print end-start
