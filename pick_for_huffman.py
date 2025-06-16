from collections import defaultdict

def find_frequent_substrings(text, min_len=2, max_len=3, top_n=10):
    freq_map = defaultdict(int)

    # Count all substrings of given lengths
    for length in range(min_len, max_len + 1):
        for i in range(len(text) - length + 1):
            substr = text[i:i + length]
            freq_map[substr] += 1

    # Remove substrings that occur only once
    filtered = {k: v for k, v in freq_map.items() if v > 1}

    # Sort by frequency descending
    sorted_subs = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))

    # Return top N
    return sorted_subs[:top_n]

# Example usage
if __name__ == "__main__":
    with open("sample_files/VeryShortSimpleString.txt", "r", encoding="utf-8") as file:
        text = file.read()

    top_substrings = find_frequent_substrings(text, min_len=2, max_len=5, top_n=10)
    print("Most frequent substrings:")
    for substr, freq in top_substrings:
        print(f"{repr(substr)} → {freq} times")
