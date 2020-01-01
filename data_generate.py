import os
import csv
import re

data_dir = "data"
zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
type_list = ["分享图片", "微博视频", "网页链接","微博正文","头像委托"]
sensitive_words = ["警察", "政务", "公安", "政府", "伊斯兰","团中央","共产党","国务院","毒品","委书记","民宗委","派出所"]


def weibo_check(weibo):
    # 空内容
    if not len(weibo):
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


def weibo_export(force=False):
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    f_list = [os.path.join(item[0], item[2][0]) for item in os.walk("weibo") if len(item[2])]
    ids = {}
    names=[]
    count = 0
    for f_path in f_list:
        user_id = re.sub("\.csv", "", os.path.split(f_path)[-1])
        names.append(os.path.split(f_path)[-2])
        if not os.path.exists(os.path.join(data_dir, user_id + ".txt")) or force:
            ids[user_id] = f_path
    for user_id, f_path in ids.items():
        with open(f_path, encoding="utf8") as csv_file:
            weibos = [content[2] for content in list(csv.reader(csv_file))[1:] if weibo_check(content[2])]
            for i in range(0,7):
                print(weibos[i])
            count += len(weibos)
            # with open(os.path.join(data_dir,user_id+".txt"),"w",encoding="utf8"):

    print(count)
    print(names)


if __name__ == '__main__':
    weibo_export()
