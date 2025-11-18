import re
#Модуль re даёт доступ к функциям вроде re.split, re.findall, re.search, re.sub и другим,
#которые позволяют описывать шаблон не обычной строкой, а специальным мини‑языком регулярных выражений.

def print_sentences(text):
    # Убираем пробелы по краям
    text = text.strip()

    # Здесь регулярное выражение r'(?<=[.?!])\s+' означает «место,
    # где сразу после одного из символов . ? ! идёт один или более пробельных символов»
    # Разбиваем по пробелам, идущим после . ? или !
    # \s+ — один или больше пробельных символов
    sentences = re.split(r'(?<=[.?!])\s+', text)

    # Чистим пустые строки и лишние пробелы
    sentences = [s.strip() for s in sentences if s.strip()]

    for s in sentences:
        print(s)

    print('Предложений в тексте:', len(sentences))



text = 'He jests at scars. That never felt a wound!        Hello, friend!    Are you OK?'
print_sentences(text)
