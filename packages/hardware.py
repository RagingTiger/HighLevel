import os


def available_memory():
    # calculate total available memory in gigabytes
    return (os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES'))/(1024.**3)
