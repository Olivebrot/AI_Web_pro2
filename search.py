from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh.scoring import BM25F


class Search:
    def __init__(self, index_dir="indexdir", field_weights=None):
        """
        Initialize the Search class.
        :param index_dir: Directory containing the Whoosh index.
        :param field_weights: Dictionary specifying weights for each field.
        """
        self.index_dir = index_dir
        self.field_weights = field_weights or {"title": 2.0, "headder": 1.5, "content": 1.0}
        self.ix = open_dir(self.index_dir)

    def search_all_fields(self, query_str, limit=10):
        """
        Search across all fields using BM25F with weighted fields.
        :param query_str: The user's search query.
        :param limit: Maximum number of results to return.
        :return: List of search results with scores.
        """
        # Configure BM25F with field weights
        bm25f = BM25F(field_Bs=self.field_weights)

        # Open the searcher
        with self.ix.searcher(weighting=bm25f) as searcher:
            # Parse the query for multiple fields
            parser = MultifieldParser(self.field_weights.keys(), self.ix.schema)
            query = parser.parse(query_str)

            # Perform the search
            results = searcher.search(query, limit=limit)
            
            # Collect and return results
            search_results = []
            for result in results:
                search_results.append({
                    "url": result.get("url"),
                    "title": result.get("title"),
                    "headder": result.get("headder"),
                    "content_snippet": result.highlights("content"),
                    "score": result.score,
                })

            return search_results
