import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import os
from flask import Flask, request, jsonify

class SearchEngine:
    def __init__(self, index_dir="index"):
        from whoosh.index import open_dir
        self.index_dir = index_dir
        self.index = open_dir(index_dir)

    def search(self, query_str):
        from whoosh.qparser import QueryParser
        with self.index.searcher() as searcher:
            query = QueryParser("content", self.index.schema).parse(query_str)
            results = searcher.search(query)
            return [(result['title'], result['url']) for result in results]