from bs4 import BeautifulSoup
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize
import string
import pymorphy3
import re
import math
import task2
from os import listdir, path
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance

token_path = "../tokens.txt"
lemmas_path = "../lemmas.txt"
index_path = "../index1.txt"
pages_path = "../saved1"
tf_idf_path = "../Task4/tf_idf_lemmas"


tokens = {}
lemmas = {}
path = "saved1"
nltk.download('punkt')
nltk.download('stopwords')
stop_words = stopwords.words('russian')
stop_words.extend(['это', 'чтò','всё', 'те', 'Б', 'W', 'У','0','О','у',
                   'sports', 'sportsru', 'ufc', 'букмекер', 'й', "фг",
                   "●" , ",", " ,", "р", "х","б", "пр", "гн","са"])
bad_formatted_words = ['Вальекано', 'плачутжалуютсяскулятныть', 'плачутжалуютсяскулятноют', 'клубкоторый']
stop_words = set(stopwords.words())
spec_chars = string.punctuation + ('«»—…-’©,”●≈つ🤓😁🫨⚽💃🎭😂🤔🤣🏆👀'
                                   '👑–❤✨👌👍🧐□🎅🚨👏🤗🇦🇷❓₽№🤩༼🔥🍺🤝'
                                   '😍😄🤯🤔❓🇧🇷🤔❌🙄💊🅰️💣📹🏻💔🔗😅')
nltk.download('omw-1.4')
page_texts = [None] * 102

morph = pymorphy3.MorphAnalyzer()


def tokenization(started_text):
    # убираем знаки препинания, различные смайлики и символы
    text = "".join([ch for ch in started_text if ch not in spec_chars])
    # убираем числа
    text = "".join([ch for ch in text if ch not in string.digits])
    # получаем токены
    tokens = word_tokenize(text)
    # убираем стоп-слова
    tokens = [word.strip() for word in tokens if word not in stop_words]

    tokens = [word for word in tokens if all(sub not in word for sub in bad_formatted_words)]

    filtered_tokens = []
    for token in tokens:
        # проверяем, что токен не содержит английских символов
        if re.search('[a-zA-Z]+', token) is None:
            # добавляем его в новый массив
            if len(token) > 2:
                filtered_tokens.append(token.lower())

    filtered_tokens = [word.strip() for word in filtered_tokens if word not in stop_words]
    return filtered_tokens

def lemmatize(tokens):
    # находим леммы в списке токенов
    result_lemmas = []
    morph = pymorphy3.MorphAnalyzer()
    for token in tokens:
        morphed = morph.parse(str(token))[0]
        normal = morphed.normal_form
        if normal not in lemmas:
            result_lemmas.append(normal)
    return result_lemmas

def get_tokens():
    tokens = []
    with open(token_path, 'r') as file:
        tokens = [token.strip() for token in file.readlines()]
        return tokens

def get_links():
    with open(index_path, 'r') as file:
        lines = file.readlines()
        links = {}
        for line in lines:
            key, value = line.split('-----')
            value = value.strip()
            key = re.sub(r"\D", "", key)
            links[key] = value
        return links


def vectorize(value, lemmas):
    vector = np.zeros(len(lemmas))
    tokens = tokenization(value)
    for token in tokens:
        morphed = morph.parse(token)[0]
        lemma = morphed.normal_form if morphed.normalized.is_known else token.lower()
        if lemma in lemmas:
            vector[lemmas.index(lemma)] = 1
    return vector

def get_lemmas():
    tokens = []
    with open(lemmas_path, 'r') as file:
        lines = file.readlines()
        lemmas = []
        for line in lines:
            key, value = line.split(': ')
            sub_tokens = value.split(', ')
            lemmas.append(key)

        return lemmas

def get_tf_idf(lemmas_list):
    file_names = listdir(tf_idf_path)
    zero_matrix = np.zeros((len(file_names), len(lemmas_list)))
    for file in file_names:
        if "page" in file:
            file_number = int(re.search('\\d+', file)[0])
            with open(tf_idf_path + '/' + file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i in range(len(lines)):
                    lemma, idf, tf_idf = lines[i].split(' ')
                    tf_idf = tf_idf.strip()
                    zero_matrix[file_number][i] = float(tf_idf)
    return zero_matrix


def vector_search(vector, links, tf_idf):
    distances = dict()
    index = 0
    for page in tf_idf:
        dist = 1 - distance.cosine(vector, page)
        # print(dist)
        if dist > 0 and dist != 1:
            distances[index] = dist
        index += 1
    sorted = sorted(distances.items(), key=lambda item: item[1], reverse=True)

    result = []
    for page_number, score in sorted:
        print("page number- " + str(page_number + 1) + " score= " + str(score))
        if str(page_number + 1) in links:
            result.append(links[str(page_number + 1)])
    return result

def vector_search(vector, links, tf_idf):
    distances = dict()
    index = 0
    for page in tf_idf:
        dist = 1 - distance.cosine(vector, page)
        # print(dist)
        if dist > 0 and dist != 1:
            distances[index] = dist
        index += 1
    sorted_array = sorted(distances.items(), key=lambda item: item[1], reverse=True)

    result = []
    result_index = []
    for page_number, score in sorted_array:
        print("page number- " + str(page_number + 1) + " score= " + str(score))
        if str(page_number + 1) in links:
            result.append(links[str(page_number + 1)])
            result_index.append(page_number + 1)
    return result, result_index

if __name__ == "__main__":
    links = get_links()
    lemmas = get_lemmas()
    tokens = get_tokens()
    tf_idf = get_tf_idf(lemmas)
    while True:
        value = input("Введите запрос ")
        vector = vectorize(value, lemmas)
        result,indexes = vector_search(vector, links, tf_idf)
        if len(result) == 0:
            print("Нет подходящих страниц")
        else:
            print("Результаты поиска:")
            for i in range(len(result)):
                print("Номер страницы- " +str(indexes[i]) + " Ссылка " +str(result[i]))
