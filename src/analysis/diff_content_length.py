'''

'''
import sys
import json
import traceback
import os

def diff_length(urls_200, ual, outfile):
    '''
    Return:
        - outfile: a csv file whose the headers are:
        [url] [length difference = max_len -min_len] [min_agent] [min_len] [max_agent] [max_len]
    '''
    print "Computing the content length difference"
    out = open(outfile, "w")
    for url in urls_200:
        try:
            max_len = 0
            min_len = 999999
            max_agent= None
            min_agent = None
            agent2len = ual[url]
            for agent in agent2len:
                if agent2len[agent] > max_len:
                    max_len = agent2len[agent]
                    max_agent = agent
                if agent2len[agent] < min_len:
                    min_len = agent2len[agent]
                    min_agent = agent
            if max_len > min_len:
                ratio = (max_len - min_len)/float(max_len)
                ratio = '{0:.5f}'.format(ratio)
                out.write(url + "\t" + str(max_len-min_len) + \
                                "\t" + min_agent + \
                                "\t" + str(min_len) + \
                                "\t" + max_agent + \
                                "\t" + str(max_len) + "\n")
                
        except:
            traceback.print_exc()
            continue

    out.close()

def get_urls_200(status_files):
    '''
    Return all urls that respond 200 to all user-agents
    '''
    print "Getting urls that respond 200 to all user-agents"
    counter = {} #counting number of successful requests of each url
    N = len(status_files) #number of user-agents
    for agent in status_files:
        status_file = status_files[agent]
        print "Loading " + status_file
        with open(status_file) as lines:
            for line in lines:
                try:
                    obj = json.loads(line)
                    if 'status_code' in obj:
                        status_code = obj['status_code']
                        if status_code == '200':
                            url = obj['url']
                            if url in counter:
                                counter[url] += 1
                            else:
		                        counter[url] = 1
                except:
                    print obj.keys()
                    traceback.print_exc()
                    continue
    urls = set([])
    for url in counter:
    	if counter[url] == N:
			urls.add(url) 
    print "Number of urls: " + str(len(urls))
    return urls

def read_content_length_from_status(statusfiles, outfile):
    '''
    Get content-length of crawled data via response header
    Args: 
        - statusfiles: mapping between user-agent and status files 
    Returns:
        - outfile: output file in csv format, each line = [url] [subtopic] [length_1] ... [length_n]
    '''
    m = {} #url maps to list of content length
    code = {} # url maps to list of status code
    #topic = {}
    for f in statusfiles:
        print f
        with open(f) as lines:
            for line in lines:
                try:
                    obj = json.loads(line)
                    url = obj['url']
                    status_code = obj
                    length = int(obj['header']['content-length'])
                    #topic = obj['topic']
                    if status_code == "200":
                        #topic[url] = t
                        if url in m:
                            m[url].append(length)
                            code[url] += 1
                        else:
                            m[url] = [length]
                            code[url] = 1
                except:
                    traceback.print_exc()
                    continue

    urls = set()#url that return 200 to all user-agents
    n = len(filenames)
    for url in code:
        if code[url] == n:
            urls.add(url)
    print "Number of urls that return 200 to all user-agents: " + str(len(urls))
    out = open(outfile, "w")
    for url in m:
        if url in urls: #only select urls that returns OK to all user-agents
            l = m[url]
            l0 = l[0]
            for length in l[1:]:
                if length != l0: #only keep item that have difference in length
                    l_str = ""
                    for s in l:
                        l_str += "\t" + str(s)
                    #out.write(url + "\t" + topic[url] + l_str + "\n")
                    out.write(url + "\t" +  l_str + "\n")
                    break
  
    out.close()


def read_content_length_from_html(htmldirs):
    '''
    Return: 
        - ual: mapping between url, user-agent and content-length
            {url:{agent:length}}
    '''
    print "Reading html files"
    ual = {} 
    for agent in htmldirs:
        htmldir = htmldirs[agent]
        print "Loading " + htmldir
        files = os.listdir(htmldir)
        for f in files:
            f = htmldir + "/" + f
            with open(f) as lines:
                for line in lines:
                    try:
                        obj = json.loads(line)
                        length = len(obj['text'])                    
                        url = obj['url']
                        if url in ual:
                            ual[url][agent] = length
                        else:
                            ual[url] = {agent:length}
                    except:
                        traceback.print_exc()
                        continue
    print 'Finished reading content length from html. Number of urls: ' + str(len(ual))
    return ual

if __name__=="__main__":
    agents = ["ache", "bing", "google", "nutch", "empty", "browser"]
    status_files = {}
    html_dirs = {}
    path = sys.argv[1]
    outfile = sys.argv[2]
    for agent in agents:
        status_files[agent] = path + "/status_" + agent + ".json"
        html_dirs[agent] = path + "/html_" + agent
    
    ual = read_content_length_from_html(html_dirs)
    urls_200 = get_urls_200(status_files)
    diff_length(urls_200, ual, outfile)
