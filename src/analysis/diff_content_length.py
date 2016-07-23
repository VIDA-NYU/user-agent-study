'''

'''
import sys

def diff_length(infile, outfile, agents):
    out = open(outfile, "w")
    with open(infile) as lines:
        for line in lines:
            values = line.strip("\n").split("\t")
            url = values[0]
            topic = values[1]
            _max = _min = int(values[2]) #Default is first value (~first agent)
            idx = 0
            max_idx = min_idx = 0 #Default is first agent (~first value)
            for v in values[2:]:
                length = int(v)
                if length > _max:
                    _max = length
                    max_idx = idx
                if length < _min:
                    _min = length
                    min_idx = idx
                idx += 1
            if (min_idx != -1) & (max_idx != -1):
                d = _max - _min
                if _max == 0:
                    continue
                ratio = d/float(_max)
                ratio = '{0:.5f}'.format(ratio)
                out.write(url + "\t" + topic + "\t" + str(d) + "\t" + str(ratio) + "\t" + agents[min_idx] + "\t" + str(_min) + "\t" + agents[max_idx] + "\t" + str(_max) + "\n")
    out.close()

def stat(filenames, outfile):
    '''
    Args: 
        - filenames: A list of status file names
    Returns:
        - outfile: output file in csv format, each line = [url] [subtopic] [length_1] ... [length_n]
    '''
    m = {} #url maps to list of content length
    code = {} # url maps to list of status code
    topic = {}
    for f in filenames:
        print f
        with open(f) as lines:
            for line in lines:
                values = line.strip("\n").split("\t")
                url = values[0]
                status_code = values[2]
                length = values[3]
                if length == "None":
                    continue
                try:
                    length = int(length)
                except:
                    print length
                    continue
                t = values[4]
                if status_code == "200":
                    topic[url] = t
                    if url in m:
                        m[url].append(length)
                        code[url] += 1
                    else:
                        m[url] = [length]
                        code[url] = 1

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
                    out.write(url + "\t" + topic[url] + l_str + "\n")
                    break
  
    out.close()


if __name__=="__main__":
    agents = ["ache", "bing", "google", "nutch", "empty", "browser"]
    filenames = [] #list of status files
    path = sys.argv[1]
    for agent in agents:
        filename = path + "/" + agent + ".json.csv"
        filenames.append(filename)
    file1 = "urls_200_length.csv" #contains urls that respond 200 status to all user-agents

    #stat(filenames, file1)

    file2 = "diff_length.csv"
    diff_length(file1, file2, agents)
