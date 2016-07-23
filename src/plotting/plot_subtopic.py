"""
Simple demo of a horizontal bar chart.
"""
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

def autolabel(rects, n):
# attach some text labels
    name = [str(i) + "%" for i in n]
    for ii,rect in enumerate(rects):
        height = rect.get_height()
        print height
        #plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%s'% (name[ii]),
                                 #ha='center', va='bottom')
        width = rect.get_width()
        plt.text(width + 0.4, rect.get_y() + 0.15, '%s'% (name[ii]))
                                 

def plot_1():
    # Example data
    topics = ('All topics', 'Australia', 'Restaurants', 'Photography', 'Hotels and Motels', \
               'Chats and Forums', 'Religion', 'Christianity', 'Photographers', 'Weblogs', 'Private')
    y_pos = np.arange(len(topics))
    percentage = [5.12, 7.02, 7.16, 7.58, 8.64, 8.67, 8.93, 8.98, 9.12, 12.74, 13.00]
    
    #plt.barh(y_pos, percentage, align='center', alpha=0.4, color='#2b8cbe')
    #plt.barh(y_pos, percentage, align='center', alpha=0.4, color='#2c7fb8')
    fig, ax = plt.subplots()
    rects = ax.barh(y_pos, percentage, align='center', alpha=0.5, color='blue')
    ax.set_xlim([0,15])
    plt.yticks(y_pos, topics)
    plt.xlabel('Percentage (%)')
    #plt.title('Topic distributions of 403-returned URLs')
    plt.grid(True)  
    autolabel(rects, percentage)
    plt.tight_layout()
    plt.show()
    #plt.savefig('403.pdf', bbox_inches='tight')

def plot_2():
    #figure(1, figsize=(13,13))
    percentage = [5.12, 7.02, 7.16, 7.58, 8.64, 8.67, 8.93, 8.98, 9.12, 12.74, 13.00]
    y_pos = np.arange(len(percentage))
    barh(y_pos,percentage, align='center', alpha=0.5)
    topics = ('All topics', 'Australia', 'Restaurants', 'Photography', 'Hotels and Motels', \
               'Chats and Forums', 'Religion', 'Christianity', 'Photographers', 'Weblogs', 'Private')
    yticks(y_pos, topics)
    xlabel('Percentage')
    title('Topic distributions of 403-returned URLs')
    grid(True)
    
    show()

plot_1()
