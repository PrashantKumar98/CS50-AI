import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #raise NotImplementedError
    N = len(corpus)
    probality = dict()
    M = len(corpus[page])
    for i in corpus:
        if M != 0:
            if i in corpus[page]:
                probality[i] = (1 - damping_factor) / N + damping_factor / M
            else: probality[i] = (1 - damping_factor) / N
        else:
            probality[i] = 1 / N
    return probality

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError
    page_rank = dict()

    for page in corpus:
        page_rank[page] = 0

    curr_page = random.choice(list(corpus.keys()))

    page_rank[curr_page] += 1

    for i in range(n - 1):
        model = transition_model(corpus, curr_page, damping_factor)
        curr_page = generate_sample(model)
        page_rank[curr_page] += 1

    for page in page_rank:
        page_rank[page] /= n

    return page_rank


def generate_sample(model):

    randomNumber = random.random()

    for page in model:
        if randomNumber <= model[page]:
            return page
        randomNumber -= model[page]

    return None

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

#    raise NotImplementedError


    N = len(corpus)
    intial_rank = 1 / N
    page_rank = dict.fromkeys(corpus,intial_rank)

    #find number of out going links across each node
    # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself)
    numlinks = dict()
    transpose = dict()
    # transpose contains the dictionary in which key is webpage and value is list of webpages that link to this webpage
    for i in corpus:
        if len(corpus[i]) == 0:
            corpus[i] = set(corpus.keys())
        numlinks[i] = len(corpus[i])
        transpose[i] = set()

    for i in corpus:
        for j in corpus[i]:
            transpose[j].add(i)

    #This process should repeat until no PageRank value changes by more than 0.001 between the current rank values and the new rank values.
    while True:
        new_pagerank = dict()
        for i in corpus:
            new_pagerank[i] = (1 - damping_factor) / N
            for j in transpose[i]:
                new_pagerank[i] += damping_factor * page_rank[j] / numlinks[j]

        sum = 0
        flag = True
        for i in corpus:
            error = abs(new_pagerank[i] - page_rank[i])
            if error > 0.001:
                flag = False
            page_rank[i] = new_pagerank[i]
            sum += page_rank[i]
         # sum must be 1
         # print(sum)
        if flag:
            break

    return page_rank

if __name__ == "__main__":
    main()
