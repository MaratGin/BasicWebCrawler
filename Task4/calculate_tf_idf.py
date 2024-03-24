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


token_path = "../tokens.txt"
lemmas_path = "../lemmas.txt"
index_path = "../index1.txt"
pages_path = "../saved1"

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

def get_index():
    with open(index_path, 'r') as file:
        lines = file.readlines()
        links = {}
        for line in lines:
            key, value = line.split('-----')
            links[key] = value

        return links



def get_lemmas():
    tokens = []
    with open(lemmas_path, 'r') as file:
        lines = file.readlines()
        lemmas = {}
        for line in lines:
            key, value = line.split(': ')
            sub_tokens = value.split(', ')
            lemmas[key] = sub_tokens
            lemmas[key].pop()
        return lemmas

def calculate_text_length(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def calculate_termin_quantity(termin, text):
    words = text.split()
    count = 0
    for word in words:
        word = word.lower()
        if termin in word:
            count += 1
    return count


def calculate_tokens_tf_idf(page_text, current_page_tokens, number):
        count = calculate_text_length(page_text)
        idf_array = []
        tf_idf_array = []
        for token in current_page_tokens:
            quantity = calculate_termin_quantity(token, page_text)
            tf_value = quantity / count
            idf_count = 0
            for page in tokens.values():
                if token in page:
                    idf_count += 1
            idf = math.log((len(tokens)/idf_count))
            idf_array.append(idf)
            tf_idf_array.append(tf_value*idf)
        with open("tf_idf_tokens/page" + str(number) + ".txt", "a") as myfile:
            iter = 0
            for token in current_page_tokens:
                myfile.write(str(token) + " " + str(idf_array[iter]) + " " + str(tf_idf_array[iter]) + "\n")
                iter += 1

def calculate_lemmas_tf_idf(page_text, current_page_lemmas, number):
    count = calculate_text_length(page_text)
    idf_array = []
    tf_idf_array = []
    for lemma in current_page_lemmas:
        quantity = calculate_termin_quantity(lemma, page_text)
        tf_value = quantity / count
        idf_count = 0
        for page in lemmas.values():
            if lemma in page:
                idf_count += 1
        idf = math.log((len(lemmas) / idf_count))
        idf_array.append(idf)
        tf_idf_array.append(tf_value * idf)
    with open("tf_idf_lemmas/page" + str(number) + ".txt", "a") as myfile:
        iter = 0
        for token in current_page_lemmas:
            myfile.write(str(token) + " " + str(idf_array[iter]) + " " + str(tf_idf_array[iter]) + "\n")
            iter += 1


if __name__ == "__main__":
    links = get_index()
    index = 1
    for filename in os.listdir(pages_path):
        if filename.endswith(".html"):
            with open(pages_path + "/" + filename) as file:
                soup = BeautifulSoup(file.read(), features="html.parser")
                page_text = " ".join(soup.stripped_strings)
                fetched_tokens = tokenization(page_text)
                tokens[index] = fetched_tokens
                page_texts[index] = page_text
                index += 1
            continue
        else:
            continue


    i = 1
    for page in tokens.values():
        calculate_tokens_tf_idf(page_texts[i], page,i)
        i += 1

    page_texts = [None] * 102
    index = 1
    for filename in os.listdir(pages_path):
        if filename.endswith(".html"):
            with open(pages_path + "/" + filename) as file:
                soup = BeautifulSoup(file.read(), features="html.parser")
                page_text = " ".join(soup.stripped_strings)
                fetched_tokens = tokenization(page_text)
                fetched_lemmas = lemmatize(fetched_tokens)
                lemmas[index] = fetched_lemmas
                page_texts[index] = page_text
                index += 1
            continue
        else:
            continue

    i = 1
    for page in lemmas.values():
        calculate_lemmas_tf_idf(page_texts[i], page,i)
        i += 1
