import os
import csv
import re
from snownlp import SnowNLP
import jieba
import collections

data_dir = "data"
txt_dir = os.path.join(data_dir, "txt")
zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
type_list = ["分享图片", "微博视频", "网页链接", "微博正文", "头像委托","微博任务红包"]
sensitive_words = ["警察", "警官", "政务", "公安", "政府", "伊斯兰", "团中央", "共产党", "国务院", "毒品", "委书记",
                   "民宗委", "派出所","涉警","武警","解放军","毛主席"]

jieba.load_userdict("./local_dict.csv")

def weibo_check(weibo):
    # 空内容
    if not len(weibo) or len(weibo) < 3:
        return False
    # 无中文
    if not zh_pattern.search(weibo):
        return False
    # 内容类型过滤:
    for word in type_list:
        if word in weibo:
            return False
    # 敏感词过滤
    for word in sensitive_words:
        if word in weibo:
            return False
    return True


def weibo_export(force=True):
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if not os.path.exists(txt_dir):
        os.mkdir(txt_dir)
    f_list = [os.path.join(item[0], item[2][0]) for item in os.walk("weibo") if len(item[2])]
    ids = {}
    names = []
    # buffer for users with fewer blogs
    buffer = []
    count = 0
    for f_path in f_list:
        user_id = re.sub("\.csv", "", os.path.split(f_path)[-1])
        names.append(os.path.split(f_path)[-2])
        if not os.path.exists(os.path.join(txt_dir, user_id + ".txt")) or force:
            ids[user_id] = f_path
    for user_id, f_path in ids.items():
        with open(f_path, encoding="utf8") as csv_file:
            weibos = [re.sub(" +", " ", content[2]) for content in list(csv.reader(csv_file))[1:] if
                      weibo_check(content[2])]
            count += len(weibos)
            if len(weibos) > 500:
                with open(os.path.join(txt_dir, user_id + ".txt"), "w", encoding="utf8") as f:
                    f.write("\n".join(weibos))
            else:
                buffer = buffer + weibos
    buffer = list(set(buffer))
    with open(os.path.join(txt_dir, "others.txt"), "w", encoding="utf8") as f:
        f.write("\n".join(buffer))
    print(count)
    # print(names)


def tokenizer(text, type=1):
    if type == 1:
        return jieba.cut(text)
    elif type == 2:
        s = SnowNLP(text)
        return s.words


def word_range_generate(size=10000, force=False):
    fname = os.path.join(data_dir, "wr_" + str(size) + ".csv")
    if os.path.exists(fname) and not force:
        with open(fname, encoding="utf8") as csv_file:
            reader = csv.reader(csv_file)
            word_dict = dict(reader)
            return word_dict
    words = collections.Counter()
    f_list = [os.path.join(txt_dir, item) for item in list(os.walk(txt_dir))[0][2] if len(item)]
    for txt in f_list:
        with open(txt, encoding="utf8") as f:
            weibos = list(f)
            print("Processing " + txt + " length: " + str(len(weibos)))
            buffer = []
            for weibo in weibos:
                buffer += tokenizer(weibo)
            for word in buffer:
                words[word] += 1
    dict_words=dict(words)
    with open(os.path.join(data_dir, "wr_full.csv"),'w', newline="", encoding="utf8") as f:
        writer = csv.writer(f)
        for key, value in dict_words.items():
            writer.writerow([key, value])
    with open(fname,'w', newline="", encoding="utf8") as f:
        writer = csv.writer(f)
        dict_words=dict(words.most_common(size))
        for key, value in dict_words.items():
            writer.writerow([key, value])



if __name__ == '__main__':
    # weibo_export(force=True)
    word_range_generate()
