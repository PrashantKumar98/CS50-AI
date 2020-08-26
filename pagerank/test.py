corpus = {'a':1,'b':2,'c':3,'d':4}
a = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
numlinks = dict()
for i in a:
   # if len(corpus[i]) == 0:
    #a[i] = set(corpus.keys())
    numlinks[i] = len(a[i])

print(numlinks)
