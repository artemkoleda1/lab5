def shorten_text(text):

    while '(' in text and ')' in text:
        left = text.rfind('(')
        right = text.find(')', left)
        if right == -1:
            break

        text = text.replace(text[left:right + 1], '')


    text = ' '.join(text.split())
    return text



source = 'Падал (куда он там падал) прошлогодний (значит очень старый) снег (а почему не дождь) () (()).'
result = shorten_text(source)
print(result)
