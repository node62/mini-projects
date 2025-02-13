import random
import urllib.request

"""
Markov Chain Sentence Maker

This script uses Markov chains to make random sentences from some input text.
A Markov chain works by looking at word patterns (n-grams) in the text and guessing
the next word based on what it sees. It makes a dictionary of word groups
and uses that to create new sentences that feel like the original text.

"""

def get_text_from_web(link):
    with urllib.request.urlopen(link) as resp:
        return resp.read().decode('utf-8')

def make_word_chain(big_text, word_group_size=2):
    chain_dict = {}
    word_list = big_text.split()

    for i in range(len(word_list) - word_group_size):
        word_pair = tuple(word_list[i:i + word_group_size])
        word_after = word_list[i + word_group_size]
        if word_pair not in chain_dict:
            chain_dict[word_pair] = []
        chain_dict[word_pair].append(word_after)

    return chain_dict

def make_sentence(word_dict, group_size=2, sent_length=50):
    start_words = random.choice(list(word_dict.keys()))
    sentence_words = list(start_words)

    for _ in range(sent_length - group_size):
        key_words = tuple(sentence_words[-group_size:])
        if key_words in word_dict:
            next_word = random.choice(word_dict[key_words])
            sentence_words.append(next_word)
        else:
            break

    return " ".join(sentence_words)

if __name__ == "__main__":
    web_link = "http://paulo-jorente.de/text/alice_oz.txt"
    raw_text = get_text_from_web(web_link)
    group_size = 2
    sentence_size = int(input("Output length: "))
    word_chain = make_word_chain(raw_text, group_size)
    print("Output: ", make_sentence(word_chain, group_size, sentence_size))
