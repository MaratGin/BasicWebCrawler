from bs4 import BeautifulSoup
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize
import string
import pymorphy3
import re

path = "../saved1"
tokens = []
invetred_list = {}
def generate_inverted_text():
    page_number = 1
    for filename in os.listdir(path):
        if filename.endswith(".html"):
            with open(path + "/" + filename) as file:
                soup = BeautifulSoup(file.read(), features="html.parser")
                page_text = " ".join(soup.stripped_strings)
                page_text = page_text.lower()
                for token in tokens:
                    if token in page_text:
                        if token in invetred_list:
                            invetred_list[token].add(page_number)
                        else:
                            invetred_list[token] = {page_number}
            page_number = page_number + 1
        else:
            continue


def get_tokens():
    tokens = []
    with open("../tokens.txt", 'r') as file:
        tokens = [token.strip() for token in file.readlines()]
        return tokens

def save_inverted_text():
    with open("inverted_index.txt", "a") as myfile:
        for token, pages in invetred_list.items():
            myfile.write(token +" ")
            for page in pages:
                myfile.write(str(page) + " ")
            myfile.write("\n")


if __name__ == "__main__":
    tokens = get_tokens()
    generate_inverted_text()
    save_inverted_text()