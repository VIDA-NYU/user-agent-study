'''
Count number of exceptions for each crawl

Arguments:
    [crawl_status_file_1] [crawl_status_file_2] ... [crawl_status_file_n]

Note: Input must be csv and follows this format:
[url] [user-agent] [status_code|None] [content_length|None] [subtopic] [exception|None]
'''
import sys
import json

def count(filenames):
    for f in filenames:
        count = {}
        with open(f) as lines:
            for line in lines:
                obj = json.loads(line)
                if 'exception' in obj:
                    if obj['exception'] in count:
                        count[obj['exception']] += 1
                    else:
                        count[obj['exception']] = 1
        output = f
        for key in count:
            output += "\t" + key + ":" + str(count[key])
        print output

if __name__=="__main__":
    count(sys.argv[1:])
