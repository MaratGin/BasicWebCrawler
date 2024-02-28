from bs4 import BeautifulSoup
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize
import string
import pymorphy3
import re

tokens = []
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
text_pages = []

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
    morph = pymorphy3.MorphAnalyzer()
    for token in tokens:
        morphed = morph.parse(str(token))[0]
        normal = morphed.normal_form
        if normal in lemmas:
            lemmas[normal].add(token)
        else:
            if normal == token:
                lemmas[normal] = {token}
            else:
                lemmas[normal] = {normal}
                lemmas[normal].add(token)

def save_tokens():
    # сохраняем токены в текстовом файле
    with open("tokens.txt", "a") as myfile:
        for token in tokens:
            myfile.write(token + "\n")


def save_lemmas():
    # сохраняем леммы в текстовом файле
    with open("lemmas.txt", "a") as myfile:
        for lemma, tokens_list in lemmas.items():
            myfile.write(lemma +": ")
            for token in tokens_list:
                myfile.write(str(token) + ", ")
            myfile.write("\n")

if __name__ == "__main__":
    for filename in os.listdir(path):
        if filename.endswith(".html"):
            with open(path + "/" + filename) as file:
                soup = BeautifulSoup(file.read(), features="html.parser")
                page_text = " ".join(soup.stripped_strings)
                fetched_tokens = tokenization(page_text)
                tokens.extend(fetched_tokens)
            continue
        else:
            continue
    tokens = list(set(tokens))
    lemmatize(tokens)
    save_tokens()
    save_lemmas()
