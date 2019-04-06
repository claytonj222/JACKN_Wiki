import random


def seedRNG(i):
    random.seed(i)


def determineValueForRedirect(pages):
    value = random.randint(0, len(pages) - 1)
    return value


def determinePageForRedirect(pages, value):
    page = pages[value]
    return page.url




