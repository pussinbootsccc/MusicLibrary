from heapq import *

__author__ = "Carol Cha"
__email__ = "rigi.thu@gmail.com"
__version__ = "0.01"

def display_error(message):
    """Display a warning message with color.
    """
    CERR = '\033[91m'
    CEND = '\033[0m'
    print "%s%s%s" % (CERR, message, CEND)

def display_table(data, title, displayNumber=False):
    """Format the given data (list) into a pretty-looking table.
    """
    if not data:
        print "Empty list. Nothing to display."
        return

    if displayNumber:
        data = ["%02d. %s" % (i+1, d) for i, d in enumerate(data)]

    max_len = max(max(map(lambda x:len(x), data)), len(title))

    pad = lambda x: "| " + x + " "*(max_len-len(x)) + " |"

    rows = [pad(d) for d in data]
    double_rule = "-"*len(rows[0]) 
    single_rule = pad("-"*max_len)

    print double_rule
    print pad(title)
    print single_rule
    for row in rows:
        print row
    print double_rule

def heap_find_top_N(entity_count_table, N):
    """Find the N largest entities using a min-heap based on play count.
    """
    # to ensure N does not excceed the number of artists/tracks
    N = min(len(entity_count_table), N)
    # implement minheap to find N largest numbers
    heap = []
    for entity, count in entity_count_table.iteritems():
        if len(heap) < N:
            heappush(heap, (count, entity))
        else:
            heappushpop(heap, (count, entity))
    # return the top N entities in descending order
    res = []
    while heap:
        res.append(heappop(heap)[1])
    return res[::-1]

