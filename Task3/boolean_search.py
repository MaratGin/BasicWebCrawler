import re

path = "../saved1"
tokens = []
invetred_list = {}
operands = ['and', 'or', 'not']

web_pages = []
def get_inverted_index():
    pages = []
    inverted_list = {}
    with open("inverted_index.txt", 'r') as file:
        for line in file.readlines():
            values = line.strip().split(" ")
            token, pages = values[0], values[1:]
            inverted_list[token] = set(pages)
    return inverted_list

def new_boolean_search(query):
    stack = []
    for token in query:
        # print(token)
        if token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1 - 1] != '(':
                stack = evaluate(stack)
            val = stack.pop()
            stack.pop()
            stack.append(val)
        elif token.lower() in ['and', 'or', 'not']:
            stack.append(token.lower())
        else:
            if token in invetred_list:
                stack.append(invetred_list[token])
            else:
                stack.append([])
    while len(stack) > 1:
        stack = evaluate(stack)
    if len(stack[0]) == 0:
        return 'нет подходящего множества'
    return stack.pop()

def evaluate(stack):
    result = []
    while stack and isinstance(stack[-1], set):
        result.append(stack.pop())
    # stack.pop()
    if stack:
        operator = stack.pop()
        if operator == 'and':
            result.append(result.pop().intersection(stack.pop()))
        elif operator == 'or':
            result.append(result.pop().union(stack.pop()))
        elif operator == 'not':
            result.append(result.pop().difference(stack.pop()))
    return stack + result

def split_string(input_string):
    # Используем регулярное выражение для разделения строки по пробелам и сохранения скобок
    elements = re.findall(r'[\w]+|[\(\)]', input_string)
    return elements

if __name__ == "__main__":
    invetred_list = get_inverted_index()
    print("Введите запрос")
    string = str(input())
    # Примеры использования
    # ((месси and тейт) OR (обе and авария)) OR кевин
    # месси or тейт and авария
    # ((месси and тейт) OR (обе and авария)) NOT кевин
    # ((месси or тейт) and авария)
    final_string = split_string(string)
    print("полученные страницы:")
    print(new_boolean_search(final_string))