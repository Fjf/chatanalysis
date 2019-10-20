from collections import defaultdict
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt


class Message(object):
    def __init__(self, line):
        data = line.split(" - ", 1)
        if len(data) < 2:
            raise ValueError("This is not a chat message.")

        message_data = data[1].split(": ")

        if len(message_data) < 2:
            raise ValueError("This is not a valid chat message.")

        self.time = datetime.strptime(data[0], "%y-%m-%d %H:%M")
        self.sender = message_data[0]
        self.message = message_data[1]


def parse_text(input_file):
    data = []
    with open(input_file, "r", errors='ignore', encoding="utf-8") as f:
        for line in f:
            try:
                message = Message(line)
                data.append(message)
            except ValueError:
                pass
    return data


def analyse_word_frequencies(data):
    word_freq_d = defaultdict(int)
    word_freq_f = defaultdict(int)
    for d in data:
        # Select correct dictionary to store data
        if d.sender == "Duncan":
            freq = word_freq_d
        else:
            freq = word_freq_f

        for word in d.message.split():
            freq[word.lower()] += 1

    word_freq_d = sorted(word_freq_d.items(), key=lambda k_v: k_v[1], reverse=True)
    word_freq_f = sorted(word_freq_f.items(), key=lambda k_v: k_v[1], reverse=True)
    return word_freq_d, word_freq_f


def analyse_time_frequencies(data):
    granularity = 3
    time_freq_d = np.zeros(24 * granularity)
    time_freq_f = np.zeros(24 * granularity)
    for d in data:
        # Select correct dictionary to store data
        if d.sender == "Duncan":
            time = time_freq_d
        else:
            time = time_freq_f

        time[d.time.hour * granularity + d.time.minute // (60 // granularity)] += 1

    return time_freq_d, time_freq_f


def main():
    input_file = "chatlog.txt"

    data = parse_text(input_file)

    word_frequency_d, word_frequency_f = analyse_word_frequencies(data)
    times_d, times_f = analyse_time_frequencies(data)

    word_count_d = len([d for d in data if d.sender == "Duncan"])
    word_count_f = len([d for d in data if d.sender == "Fabienne Détant"])

    fig, ax = plt.subplots(1, 1)

    ax.plot(np.linspace(0, 24, len(times_d)), times_d / word_count_d)
    ax.plot(np.linspace(0, 24, len(times_f)), times_f / word_count_f, alpha=0.5)
    ax.set_xticks(np.arange(0, 24))
    fig.show()

    # print([d for d in word_frequency_d if "vakantie" in d[0]])
    # print([d for d in word_frequency_f if "vakantie" in d[0]])

    d_words = np.array(word_frequency_d[:100])
    f_words = np.array(word_frequency_f[:100])

    plt.barh(f_words[:, 0], np.array(f_words[:, 1], dtype=int) / word_count_f)
    plt.barh(d_words[:, 0], np.array(d_words[:, 1], dtype=int) / word_count_d, alpha=0.5)
    plt.show()


if __name__ == "__main__":
    main()
