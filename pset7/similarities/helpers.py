from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    first = a.split("\n")
    second = b.split("\n")
    return(set(first) & set(second))


def sentences(a, b):
    """Return sentences in both a and b"""
    first = sent_tokenize(a, language='english')
    second = sent_tokenize(b, language='english')
    return(set(first) & set(second))


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    first = [a[i:i + n] for i in range(0, len(a) + 1 - n)]
    second = [b[i:i + n] for i in range(0, len(b) + 1 - n)]
    return(set(first) & set(second))