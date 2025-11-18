def make_abbreviation(text):
    words = text.split()
    letters = []

    for word in words:
        if len(word) >= 3:
            letters.append(word[0].upper())

    return ''.join(letters)



print(make_abbreviation('New York City'))  # NYC
print(make_abbreviation('Yanka Kupala State University of Grodno'))  # YKSUG
