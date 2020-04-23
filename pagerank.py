import os
import random
import re
import sys
import copy

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
    a= list(corpus[page])
    n=len(a)
    res={}
    b=set()
    m=len(corpus)
    for x in a:
        res[x]= float(float(damping_factor) / float(n))
        b.add(x)
    if n==0:
        for x in corpus:
            res[x]=float(float(1)/float(m))
    else:
        for x in corpus:
            if x not in b:
                res[x]=float(float(1-damping_factor)/float(m-n))

    return res


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    res={}
    for x in corpus:
        res[x]=0

    start= random.choice(list(corpus.keys()))
    res[start]+=1
    now= copy.deepcopy(start)
    for i in range(n-1):
        gett= transition_model(corpus,now,damping_factor)
        {k: v for k, v in sorted(gett.items(), key=lambda item: item[1])}
        num=random.random()
        total=0
        for k, v in gett.items():
            total += v
            if num <= total:
                now=k
                break
        res[now]+=1

    for x in res:
        res[x]=float(float(res[x])/float(n))

    return res

   # raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
 #   raise NotImplementedError
    invcorpus={}
    for x in corpus:
        invcorpus[x]=set()
    for x,v in corpus.items():
        for y in v:
            invcorpus[y].add(x)

    prev={}
    now={}
    for x in corpus:
        prev[x]=float(float(1)/float(len(corpus)))
    n=len(corpus)

    while True:
        can=False
        for x in corpus:
            now[x]= float(float(1-damping_factor)/float(n))
            rem=0
            for y in invcorpus[x]:
                if len(corpus[y])==0:
                    rem = rem + float(float(prev[y])/float(n))
                else:
                    rem = rem + float(float(prev[y])/float(len(corpus[y])))
            now[x]= now[x] + float(damping_factor*rem)
            if abs(float(now[x]-prev[x]))>float(0.001):

                can=True

        if can==False:
            break

        for x in prev:
            prev[x]=now[x]

    return now


if __name__ == "__main__":
    main()
