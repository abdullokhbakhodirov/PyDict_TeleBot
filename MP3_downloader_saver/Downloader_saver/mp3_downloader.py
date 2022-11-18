import json
import math
import os
import threading
from threading import Thread
import requests

MP3_FILENAME_EXTENSION = '.mp3'
DIR_PATH = '../../MP3_downloader_saver/'
DATA_FILE = 'C:/Users/abdul/PycharmProjects/PyDict_TeleBot/MP3_downloader_saver/'
list_f = ['data1.json', 'data2.json', 'data3.json', 'data4.json', 'data5.json']


def download_mp3(word, url, dir_path):
    filename = os.path.join(dir_path, word + MP3_FILENAME_EXTENSION)
    with open(filename, 'wb') as file:
        file.write(requests.get(url).content)
        file.close()


def split_dict_evenly(m_dict, segment_count):
    if segment_count == 1:
        return [m_dict]

    segment_length = math.ceil(len(m_dict) / segment_count)
    keys = list(m_dict.keys())
    key_groups = [keys[segment_length * i: segment_length * (i + 1)] for i in range(segment_count)]
    return [{key: m_dict[key] for key in group} for group in key_groups]


# a single downloader thread
class DownloadWorker(Thread):
    # 'pairs' is a dictionary
    def __init__(self, pk, pairs, dir_path, statistics):
        Thread.__init__(self)
        self.pk = pk
        self.pairs = pairs
        self.dir_path = dir_path
        self.statistics = statistics

    def run(self):

        word = self.pairs[0]
        url = self.pairs[1]
        current = self.statistics.increase_current()
        print('(' + str(current) + '/' + str(self.statistics.total) + ') ' + word)
        try:
            download_mp3(word, url, self.dir_path)
            return True
        except:
            return False


class Statistics:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.total_lock = threading.Lock()
        self.current_lock = threading.Lock()

    def increase_current(self):
        self.current_lock.acquire()
        self.current += 1
        value = self.current
        self.current_lock.release()
        return value

    def decrease_total(self):
        self.total_lock.acquire()
        self.total -= 1
        value = self.total
        self.total_lock.release()
        return value


def main(word):
    if not os.path.exists(DIR_PATH):
        os.makedirs(DIR_PATH)
    for d in list_f:
        with open(DATA_FILE+d, 'r') as file:
            data = json.loads(file.read())
        statistics = Statistics(len(data))
        data_segments = word
        for j in data:
            if j == data_segments:
                worker = DownloadWorker(1, [data_segments, data[j]], DIR_PATH, statistics)
                worker.start()
                if not worker:
                    return False


def delete(word):
    location = "C:/Users/abdul/PycharmProjects/PyDict_TeleBot/MP3_downloader_saver/"
    path = os.path.join(location, word)
    os.remove(path)
