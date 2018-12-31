import random
from copy import deepcopy
from typing import Optional

import numpy as np

from .utils import remove_anything_except_punctuation


class MarkovWeightedMatrix:
    def __init__(self, chain_length: int = 2):
        self.map = {}
        self._new_words_added = False
        self._chain_length = 2

    def learn(self, text: str) -> None:
        tokens = text.split()
        for left in range(0,
                          len(tokens),
                          self._chain_length):
            middle = left + self._chain_length
            right = middle + self._chain_length
            first_batch = ' '.join(tokens[left:middle])
            second_batch = ' '.join(tokens[middle:right])
            self._add(first_batch, second_batch)

    def _add(self, current_word: str, next_word: str) -> None:
        """Adds words into weighted markov matrix"""
        self._new_words_added = True
        current_word = remove_anything_except_punctuation(current_word)
        next_word = remove_anything_except_punctuation(next_word)
        if not current_word or not next_word:
            return
        if current_word not in self.map:
            self.map[current_word] = {next_word: 0}
        else:
            current_word_dict = self.map[current_word]
            if next_word not in current_word_dict:
                current_word_dict[next_word] = 0
        self.map[current_word][next_word] += 1

    def update_weighted_matrix(self) -> None:
        self.weighted_map = deepcopy(self.map)
        for connection in self.weighted_map:
            connections = self.weighted_map[connection]
            connections_count = sum(list(connections.values()))
            for key in self.weighted_map[connection]:
                self.weighted_map[connection][key] /= connections_count

    @property
    def weights(self) -> dict:
        if not hasattr(self, 'weighted_map'):
            self.update_weighted_matrix()
        return self.weighted_map

    def get_start_word(self) -> Optional[str]:
        keys = list(self.weights.keys())
        random.shuffle(keys)
        for key in keys:
            first_word = key.split()[0]
            if first_word.capitalize() == first_word and first_word[0].isalpha():
                return key
    
    def _pick_next_word(self, word: str) -> str:
        connections = self.weights[word]
        words = list(connections.keys())
        probabilities = list(connections.values())
        return np.random.choice(words, 1, p=probabilities)[0]

    def generate_sentence(self) -> str:
        current_word = self.get_start_word()
        word_chunks = [current_word]
        while current_word in self.weights:
            current_word = self._pick_next_word(current_word)
            word_chunks.append(current_word)
        return ' '.join(word_chunks)
