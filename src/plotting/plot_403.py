import numpy as np
import matplotlib.pyplot as plt
import pandas
def autolabel(rects, n):
# attach some text labels
    name = [str(i) + "%" for i in n]
    for ii,rect in enumerate(rects):
        height = rect.get_height()
        #plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%s'% (name[ii]),
                                 #ha='center', va='bottom')
        width = rect.get_width()
        plt.text(width + 0.08 , rect.get_y() + 0.06, '%s'% (name[ii]))
 
def read_data():
    topics = []
    conflicts = [] #percentage of confict URLs
    codes = [] #percentage of 403 returning URLs
    with open("sorted_403.csv") as lines:
        for line in lines:
            values = line.strip("\n").split("\t")
            topic = values[0]
            conflict = float(values[1])
            code = float(values[2])
            topics.append(topic)
            conflicts.append(conflict)
            codes.append(code)
    return topics, conflicts, codes

def plot_1():
    # Example data
    topics, conflicts, codes = read_data()
    y_pos = np.arange(len(topics))
    
    width = 0.4
    ind = np.arange(len(topics))

    fig, ax = plt.subplots()
    r1 = ax.barh(ind, conflicts, width, color='#d8b365', label='Conflict URL Percentage')
    r2 = ax.barh(ind + width, codes, width, color='#2b8cbe', label='403 URL Percentage')
    ax.set_xlim([0,10])
    autolabel(r1, conflicts)
    autolabel(r2, codes)

    ax.set(yticks=ind + width, yticklabels=topics, ylim=[2*width - 1, len(topics)])
    ax.legend(loc='lower right', shadow=True, prop = {'size':10})


    #plt.barh(y_pos, percentage, align='center', alpha=0.4, color='#2b8cbe')
    #plt.barh(y_pos, percentage, align='center', alpha=0.4, color='#2c7fb8')
    #plt.xlabel('Percentage (%)')
    #plt.title('Topic distributions of 403-returned URLs')
    plt.grid(True)  
    #autolabel(rects)
    plt.tight_layout()
    plt.show()
    #plt.savefig('403.pdf', bbox_inches='tight')

def plot_test():
    df = pandas.DataFrame(dict(graph=['Item one', 'Item two', 'Item three'],
                                                          n=[3, 5, 2], m=[6, 1, 3])) 
    
    ind = np.arange(len(df))
    width = 0.4
    
    fig, ax = plt.subplots()
    ax.barh(ind, df.n, width, color='red', label='N')
    ax.barh(ind + width, df.m, width, color='green', label='M')
    
    ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
    ax.legend()

    plt.show()

#plot_test()
plot_1()
