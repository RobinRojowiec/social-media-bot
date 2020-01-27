"""

IDE: PyCharm
Project: social-media-bot
Author: Robin
Filename: term_document_matrix.py
Date: 26.01.2020

"""
from collections import defaultdict

import numpy as np
from scipy.spatial.distance import cosine


class TermDocumentMatrix:
    def __init__(self, ):
        self.matrix = []
        self.vocab = set()
        self.docs = set()

        self.term_term_matrix = None
        self.doc_doc_matrix = None

    def add_doc(self, id, terms):
        self.docs.add(id)
        self.matrix.add(terms)
        self.vocab.add(terms)

    def _get_term_freq(self, min_support):
        term_freqs = defaultdict(int)
        for term in self.vocab:
            for row in self.matrix:
                if term in row:
                    term_freqs[term] += 1
            if term_freqs[term] < min_support:
                del term_freqs[term]
        return term_freqs

    def get_most_frequent_phrases(self, min_n, max_n, min_support=5):
        most_freq_terms = self._get_term_freq(min_support)
        most_freq_terms.update(self._get_freq_ngrams(most_freq_terms, min_n, max_n, 1, min_support))
        return most_freq_terms

    def get_ngram_count(self, ngram_tuple):
        count = 0
        for row in self.matrix:
            match = 0
            for ngram in ngram_tuple:
                if ngram in row.keys():
                    match += 1
            count += 1 if match == len(ngram_tuple) else 0
        return count

    def build_ngrams(self, terms, n):
        pass

    def _get_freq_ngrams(self, freq_terms, min_n, max_n, n, min_support=5):
        if n >= min_n and n <= max_n:
            for ngram_tuple in self.build_ngrams(freq_terms.keys(), n):
                ngram_count = self.get_ngram_count(ngram_tuple)

            return self._get_freq_ngrams(freq_terms, min_n, max_n, n + 1, min_support)
        return freq_terms

    def get_document_frequency(self, term, relative=False):
        count = 0
        index = self.term_index(term)
        for doc in self.matrix:
            count += doc[index]

        if relative:
            return count / len(self.docs)
        return count

    def get_similarity(self, doc, doc2):
        doc_index, doc2_index = self.doc_index(doc), self.doc_index(doc2)
        return cosine(np.asarray(self.matrix[doc_index]), np.asarray(self.matrix[doc2_index]))

    def finalize(self):
        self._build_term_term_matrix()

    def _build_term_term_matrix(self):
        self.term_term_matrix = [[0 for _ in range(len(self.vocab))] for _ in range(len(self.vocab))]
        for doc in self.docs:
            doc_index = self.doc_index(doc)
            for term in self.vocab:
                term_index = self.term_index(term)
                for term2 in self.vocab:
                    term2_index = self.term_index(term2)

                    if self.matrix[doc_index][term_index] and self.matrix[doc_index][term2_index]:
                        self.term_term_matrix[term_index][term2_index] += 1
