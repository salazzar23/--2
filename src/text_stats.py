import sys
from lib.text import normalize, tokenize, count_freq, top_n

TABLE_MODE = True

def print_table(items):
    if not items:
        return
    max_len = max(len(word) for word, _ in items)
    print(f"{'слово'.ljust(max_len)} | частота")
    print("-" * (max_len + 11))
    for word, count in items:
        print(f"{word.ljust(max_len)} | {count}")

def main():
    text = sys.stdin.readline()
    tokens = tokenize(normalize(text))
    freqs = count_freq(tokens)
    top5 = top_n(freqs, 5)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freqs)}")
    print("Топ-5:")

    if TABLE_MODE:
        print_table(top5)
    else:
        for word, count in top5:
            print(f"{word}:{count}")

if __name__ == "__main__":
    main()