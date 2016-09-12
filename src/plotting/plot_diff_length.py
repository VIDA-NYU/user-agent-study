import matplotlib.pyplot as plt
import sys

def plot(filename):
    '''
    Inputs:
        - filename: a csv file that has the headers below:
        [url] [length difference = [max_len - min_len] [min_agent] [min_len] [max_agent] [max_len]
    '''
    x = []
    with open(filename) as lines:
        for line in lines:
            values = line.strip("\n").split("\t")
            length = int(values[1])
            if (length < 4000) & (length > 200):
                x.append(length)   
    print len(x)
    plt.hist(x, bins=50)
    plt.xlabel("Content length difference in number of characters")
    plt.ylabel("Number of urls")
    plt.grid(True)
    plt.show()

if __name__=="__main__":
    filename = sys.argv[1]
    plot(filename)
