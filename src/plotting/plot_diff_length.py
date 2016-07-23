import matplotlib.pyplot as plt

x = []
with open("diff_length.csv") as lines:
    for line in lines:
        values = line.strip("\n").split("\t")
        l = int(values[-1])
        if (l < 4000) & (l > 200):
            x.append(l)   
print len(x)
plt.hist(x, bins=50)
plt.xlabel("Content length difference in byte")
plt.ylabel("Number of urls")
plt.grid(True)
plt.show()
