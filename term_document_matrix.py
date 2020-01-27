"""

IDE: PyCharm
Project: social-media-bot
Author: Robin
Filename: term_document_matrix.py
Date: 26.01.2020

"""
from collections import defaultdict


class TermDocumentMatrix:
    def __init__(self, spacy_analyzer):
        self.spacy_analyzer = spacy_analyzer
        self.matrix = []
        self.vocab = set()
        self.docs = []

        self.document_frequencies = defaultdict(int)
        self.term_frequencies = defaultdict(int)
        self.max_tf = 0
        self.allow_stopword_only = False

    def get_stats(self):
        stats = dict()
        stats["vocab_len"] = len(self.vocab)
        stats["non_stop_vocab_len"] = 0
        stats["max_sent_len"] = 0
        stats["min_sent_len"] = 0
        stats["media_sent_len"] = 0
        return stats

    def add_doc(self, id, text):
        tokens = [SimpleToken(token.text, token.is_stop) for token in self.spacy_analyzer(text) if
                  token.is_alpha or token.like_url or token.is_digit]
        self.docs.append(id)
        self.vocab.update([token.text for token in tokens])
        self.matrix.append(tokens)

        for token in tokens:
            self.term_frequencies[token.text] += 1
            self.max_tf += 1

        for term_unique in set(tokens):
            self.document_frequencies[term_unique.text] += 1

    def _get_term_freq(self, min_support):
        term_freqs = dict()
        for key in self.document_frequencies.keys():
            if self.document_frequencies[key] >= min_support:
                term_freqs[key] = self.document_frequencies[key]
        return term_freqs

    def get_most_frequent_phrases(self, min_n, max_n, min_support=10):
        return self._get_freq_ngrams(dict(), min_n, max_n, 1, min_support)

    def get_ngram_count(self, ngram_tuple):
        count = 0
        for row in self.matrix:
            match = 0
            for ngram in ngram_tuple:
                if ngram.text in [r.text for r in row]:
                    match += 1
            count += 1 if match == len(ngram_tuple) else 0
        return count

    def build_frequent_ngrams(self, n, min_support):
        ngrams = []
        key_set = set(self._get_term_freq(min_support).keys())
        for row in self.matrix:
            for i in range(n, len(row), n):
                ngram = row[i - n:i]
                stops = [1 for token in ngram if token.is_stop]
                if (self.allow_stopword_only == (len(stops) == len(ngram))) or n == 1:
                    if n == sum([1 for term in ngram if term.text in key_set]):
                        ngrams.append(ngram)
        return ngrams

    def _get_freq_ngrams(self, freq_terms, min_n, max_n, n, min_support):
        if n < min_n:
            return self._get_freq_ngrams(freq_terms, min_n, max_n, min_n, min_support)
        elif min_n <= n <= max_n:
            for ngram_tuple in self.build_frequent_ngrams(n, min_support):
                ngram_count = self.get_ngram_count(ngram_tuple)
                if ngram_count >= min_support:
                    freq_terms[' '.join([token.text for token in ngram_tuple])] = ngram_count
            return self._get_freq_ngrams(freq_terms, min_n, max_n, n + 1, min_support)
        return freq_terms

    def get_document_frequency(self, term, relative=False):
        count = self.document_frequencies[term]
        if relative:
            return count / len(self.docs)
        return count

    def get_term_frequency(self, term, relative=False):
        count = self.term_frequencies[term]

        if relative:
            return count / self.sum_tf
        return count


class SimpleToken:
    def __init__(self, text, is_stop):
        self.text = text
        self.is_stop = is_stop


def filter_top_phrases(phrases, count):
    top_phrases = []
    for key in phrases.keys():
        top_phrases.append((key, phrases[key]))

    top_phrases.sort(key=lambda x: x[1], reverse=True)

    return top_phrases[:min(len(top_phrases), count)]
