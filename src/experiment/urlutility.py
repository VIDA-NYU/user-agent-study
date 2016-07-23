import urllib2

'''
@author: Kien Pham (kienpt.vie@gmail.com)
@date: 02/19/2016
'''

class URLUtility:
    @staticmethod
    def decode(url):
        decoded_url = urllib2.unquote(url)
        return decoded_url

    @staticmethod
    def encode(url):
        return urllib2.quote(url).replace("/", "%2F")

    @staticmethod
    def normalize(url):
        '''
        Normalize urls to this format: http://www.website.domain (in lower cases) 

        Args:
            url - an input url 
        Returns:
            norm_url - a normalized url with lower cases. Format: http://www.website.domain 
        '''
        #Extract network location
        norm_url = url.lower()
        if len(norm_url) > 8:
            if norm_url[:7] == 'http://':
                norm_url = norm_url[7:]
            elif norm_url[:8] == 'https://':
                norm_url = norm_url[8:]

        #Remove www from network location
        if len(norm_url) > 4:
            if norm_url[:4] == 'www.':
                norm_url = norm_url[4:]

        norm_url = "http://www." + norm_url
        return norm_url

def test():
    u = 'nYu.edu'
    print "URL: " + u
    u = URLUtility.normalize(u)
    print "After normalization: " + u
    u = URLUtility.encode(u)
    print "After encoding: " + u
    u = URLUtility.decode(u)
    print "After decoding: " + u

#if __name__=="__main__":
#    test()
