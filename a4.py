# lab05_genetic_search.py

# -----------------------------
# Функция декодирования RLE
# Пример:
# '8ATA3TCGC4TC5ATTGTCAGATGAGAG6AT4A'
# -> обычная строка аминокислот
# -----------------------------
def decode_rle(encoded):
    result = []
    i = 0

    while i < len(encoded):
        ch = encoded[i]

        if ch.isdigit():
            # По условию длина серии не больше 9,
            # значит цифра одна, и за ней следует буква
            count = int(ch)
            if i + 1 < len(encoded):
                letter = encoded[i + 1]
                result.append(letter * count)
                i += 2
            else:
                # На всякий случай: если вдруг цифра в конце
                i += 1
        else:
            # Обычная буква без кодирования
            result.append(ch)
            i += 1

    return ''.join(result)


# -----------------------------
# Чтение файла sequences.txt
# Каждая строка: protein_name \t organism_name \t sequence
# sequence может быть закодирована в RLE
# -----------------------------
def read_sequences(filename):
    proteins = {}

    with open(filename, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            if len(parts) != 3:
                continue  # пропускаем некорректные строки

            protein_name = parts[0].strip()
            organism_name = parts[1].strip()
            encoded_seq = parts[2].strip()

            sequence = decode_rle(encoded_seq)
            proteins[protein_name] = {
                'organism': organism_name,
                'sequence': sequence
            }

    return proteins


# -----------------------------
# Подсчёт отличий двух цепочек
# Сравниваем посимвольно до минимальной длины,
# учитывая, что длины могут различаться.
# По тексту задания предлагают считать различия
# по позициям, поэтому берём только общую длину.
# -----------------------------
def count_difference(seq1, seq2):
    length = min(len(seq1), len(seq2))
    diff = 0

    for i in range(length):
        if seq1[i] != seq2[i]:
            diff += 1

    return diff


# -----------------------------
# Поиск самой частой аминокислоты
# При равенстве частот берём букву,
# которая меньше в алфавитном порядке.
# -----------------------------
def most_common_amino_acid(sequence):
    freq = {}

    for ch in sequence:
        freq[ch] = freq.get(ch, 0) + 1

    # Находим максимальную частоту
    max_count = max(freq.values())

    # Все буквы с такой частотой
    candidates = [ch for ch, cnt in freq.items() if cnt == max_count]

    # Берём "минимальную" по алфавиту
    best_letter = min(candidates)

    return best_letter, max_count


# -----------------------------
# Основная функция обработки команд
# -----------------------------
def process_commands(sequences_file, commands_file, output_file):
    proteins = read_sequences(sequences_file)

    with open(commands_file, encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:

        # Первая строка — твоё имя
        fout.write('Иван Иванов\n')  # <-- ЗДЕСЬ ПОМЕНЯЙ НА СЕБЯ
        # Вторая строка — заголовок
        fout.write('Генетический поиск\n')

        operation_number = 1

        for line in fin:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            command = parts[0].strip()

            # Номер операции вида 001, 002, ...
            op_id = f'{operation_number:03d}'

            if command == 'search' and len(parts) == 2:
                encoded_pattern = parts[1].strip()
                pattern = decode_rle(encoded_pattern)

                # Строка описания операции (без RLE)
                fout.write(f'{op_id} search {pattern}\n')

                found = False
                for protein_name, info in proteins.items():
                    if pattern in info['sequence']:
                        # В выводе пишем организм и белок
                        fout.write(f'{info["organism"]}\t{protein_name}\n')
                        found = True

                if not found:
                    fout.write('NOT FOUND\n')

            elif command == 'diff' and len(parts) == 3:
                protein1 = parts[1].strip()
                protein2 = parts[2].strip()

                fout.write(f'{op_id} diff {protein1} {protein2}\n')

                missing = []
                if protein1 not in proteins:
                    missing.append(protein1)
                if protein2 not in proteins:
                    missing.append(protein2)

                if missing:
                    fout.write('amino-acids difference: MISSING: ')
                    fout.write(', '.join(missing) + '\n')
                else:
                    seq1 = proteins[protein1]['sequence']
                    seq2 = proteins[protein2]['sequence']
                    diff = count_difference(seq1, seq2)
                    fout.write(f'amino-acids difference: {diff}\n')

            elif command == 'mode' and len(parts) == 2:
                protein = parts[1].strip()

                fout.write(f'{op_id} mode {protein}\n')

                if protein not in proteins:
                    fout.write('amino-acid occurs: MISSING: ' + protein + '\n')
                else:
                    seq = proteins[protein]['sequence']
                    letter, count = most_common_amino_acid(seq)
                    fout.write(f'amino-acid occurs: {letter} {count}\n')

            else:
                # На всякий случай — неизвестная или битая команда
                fout.write(f'{op_id} UNKNOWN COMMAND: {line}\n')

            # Разделительная линия между операциями
            fout.write('------------------------------\n')
            operation_number += 1


# Запуск
if __name__ == '__main__':
    process_commands('sequences.txt', 'commands.txt', 'genedata.txt')
