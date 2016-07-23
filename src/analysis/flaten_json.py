'''
This script converts status.json file to csv format
Header of the csv output:

[url] [user-agent] [status_code|None] [content_length|None] [subtopic] [exception|None]
Arguments:
    [json_filename] [csv_filename]

'''

import sys
import json

def json2csv(infile, outfile):
    out = open(outfile, "w")
    with open(infile) as lines:
        for line in lines:
            try:
                json_data = json.loads(line)
                if "status_code" in json_data:
                    status_code = json_data["status_code"]
                else:
                    status_code = "None"
                content_length = "None"
                if "header" in json_data:
                    if "Content-Length" in json_data["header"]:
                        content_length = json_data["header"]["Content-Length"]
                    if "content-length" in json_data["header"]:
                        content_length = json_data["header"]["content-length"]
                if "exception" in json_data:
                    exception = json_data["exception"]
                else:
                    exception = "None"
                line = json_data["url"] + "\t" \
                     + json_data["user-agent"] + "\t" \
                     + status_code + "\t" \
                     + str(content_length) + "\t" \
                     + json_data["url_meta"]["subtopic"] + "\t" \
                     + exception + "\n"
                out.write(line.encode("utf-8"))
            except Exception as e:
                print str(e)
                continue
    out.close()

if __name__=="__main__":
    json_file = sys.argv[1]
    output_file = sys.argv[2]
    json2csv(json_file, output_file) 
