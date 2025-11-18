def shorten_text(text):

    while '(' in text and ')' in text:
        left = text.rfind('(')
        right = text.find(')', left)
        if right == -1:
            break

        text = text.replace(text[left:right + 1], '')

