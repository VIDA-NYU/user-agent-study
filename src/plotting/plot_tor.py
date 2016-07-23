from pylab import *

# make a square figure and axes
figure(1, figsize=(13,13))
ax = axes([0.1, 0.1, 0.8, 0.8])

# The slices will be ordered and plotted counter-clockwise.
labels = '200/OK', ' 503\nService\nUnavailable', 'Other status codes \n(400, 403, 404, \n       406, 500, 502)'
ok = 78672.0*100/270574
su = 187162.0*100/270574 
other = 100-(ok+su)
fracs = [ok, su, other]
explode=(0, 0.05, 0)
colors = ['yellowgreen', 'lightskyblue', 'lightcoral']
patches, texts, autotexts = pie(fracs, explode=explode, labels=labels,
                    autopct='%1.1f%%', shadow=True, startangle=90, colors=colors)
                # The default startangle is 0, which would start
                # the Frogs slice on the x-axis.  With startangle=90,
                # everything is rotated counter-clockwise by 90 degrees,
                # so the plotting starts on the positive y-axis.
for i in range(len(texts)):
    figure(1, figsize=(6,6))
    texts[i].set_fontsize(35)

for i in range(len(autotexts)):
    autotexts[i].set_fontsize(35)

show()
