# Генетический поиск: sequences.txt + commands.txt -> genedata.txt

def decode_rle(seq):
    """
    Декодирование RLE-строки.
    Пример: '8A' -> 'AAAAAAAA', 'A3TC' -> 'ATTC'.
    Считаем, что число всегда одна цифра (1..9).
    """
    result = []
    i = 0
    while i < len(seq):
        ch = seq[i]
        if ch.isdigit():
            # цифра, значит повтор следующего символа
            count = int(ch)
            if i + 1 < len(seq):
                next_ch = seq[i + 1]
                result.append(next_ch * count)
            i += 2
        else:
            # обычный символ без кодирования
            result.append(ch)
            i += 1
    return ''.join(result)


def load_sequences(filename):
    """
    Читаем файл sequences.txt и возвращаем словарь:
    {название_белка: (организм, раскодированная_цепочка)}
    """
    sequences = {}
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) != 3:
                continue  # пропускаем странные строки
            protein, organism, seq = parts
            seq = decode_rle(seq.strip())
            sequences[protein] = (organism, seq)
    return sequences


def search_operation(out, sequences, pattern_rle):
    pattern = decode_rle(pattern_rle.strip())
    found = False
    for protein, (organism, seq) in sequences.items():
        if pattern in seq:
            out.write(f"{organism}\t{protein}\n")
            found = True
    if not found:
        out.write("NOT FOUND\n")


def diff_operation(out, sequences, protein1, protein2):
    out.write("amino-acids difference:\n")

    missing = []
    if protein1 not in sequences:
        missing.append(protein1)
    if protein2 not in sequences:
        missing.append(protein2)

    if missing:
        out.write("MISSING: " + ", ".join(missing) + "\n")
        return

    seq1 = sequences[protein1][1]
    seq2 = sequences[protein2][1]

    # Считаем различия, учитывая разную длину
    max_len = max(len(seq1), len(seq2))
    diff_count = 0
    for i in range(max_len):
        c1 = seq1[i] if i < len(seq1) else None
        c2 = seq2[i] if i < len(seq2) else None
        if c1 != c2:
            diff_count += 1

    out.write(str(diff_count) + "\n")


def mode_operation(out, sequences, protein):
    out.write("amino-acid occurs:\n")

    if protein not in sequences:
        out.write("MISSING: " + protein + "\n")
        return

    seq = sequences[protein][1]
    counts = {}
    for ch in seq:
        counts[ch] = counts.get(ch, 0) + 1

    # Ищем букву с максимальной частотой, при равенстве — по алфавиту
    max_count = max(counts.values())
    best_letters = [ch for ch, cnt in counts.items() if cnt == max_count]
    best_letter = sorted(best_letters)[0]

    out.write(f"{best_letter} {max_count}\n")


def main():
    sequences = load_sequences("sequences.txt")

    with open("commands.txt", encoding="utf-8") as cmd_file, \
         open("genedata.txt", "w", encoding="utf-8") as out:

        # Замените строку ниже на своё имя
        out.write("Имя Фамилия\n")
        out.write("Генетический поиск\n")

        op_number = 1

        for line in cmd_file:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            operation = parts[0]

            # Номер операции, например 001 search
            out.write(f"{op_number:03d} {operation}\n")

            if operation == "search" and len(parts) >= 2:
                search_operation(out, sequences, parts[1])

            elif operation == "diff" and len(parts) >= 3:
                protein1 = parts[1].strip()
                protein2 = parts[2].strip()
                diff_operation(out, sequences, protein1, protein2)

            elif operation == "mode" and len(parts) >= 2:
                protein = parts[1].strip()
                mode_operation(out, sequences, protein)

            else:
                # На всякий случай, если формат команды неправильный
                out.write("INVALID COMMAND\n")

            # Разделитель между операциями
            out.write("-" * 20 + "\n")

            op_number += 1


if __name__ == "__main__":
    main()
