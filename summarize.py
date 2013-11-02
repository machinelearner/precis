#! /usr/bin/env python

import sys
from precis.core import MultiDocumentCorpus

def run():

    if len(sys.argv) < 2 :
        print """Usage : ./summarize.py <Content Root Path>"""
        return -1

    content_root_path = sys.argv[1]
    documents = MultiDocumentCorpus(content_root_path).multi_document()
    documents.summarize_and_print()

if __name__ == "__main__" :
            run()
