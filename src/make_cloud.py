import jieba
import mysql.connector
from wordcloud import WordCloud
from PIL import Image
import numpy as np

jieba.load_userdict("./dict.txt")

""" 取得连接对象 """
conn = mysql.connector.connect(user='', password='', database='', host="", port=1111,
                               charset="utf8")

cu = conn.cursor()

words_text = ""

start = 0
limit = 1000

while True:
    sql = "SELECT comm FROM playoff  WHERE title = 'western_final' LIMIT %s, %s; " % (start, limit)
    print("执行的sql : %s" % sql)
    cu.execute(sql)
    comments = cu.fetchall()
    for comm in comments:
        seg_list = jieba.cut(comm[0])
        words_text += ",".join(seg_list)
    if len(comments) < limit:
        # 没有下一页
        break
    start += limit

# 查看了相关的中文停词 发现词语也十分少 所以自己定义可能的停词选项
stops = {'今天', '多姆', '这场', '一个', '就是', '真的',
         '什么', '这么', '肯定', '不要', '最后', '还是', '不能', '出来', '可以', '继续',
         '开始', '是不是', '不行', '多少', '捂脸', '不会', '那么', '就是', '没有',
         '为什么', '已经', '有点', '现在', '真是', '自己', '了勇士', '啊火箭', '这种', '大家', '回来', '了', '一点', '这个', '时候', '看看', '可能', '不好',
         '一定', '几个', '下去', '但是', '不用', '这是', '机会', '怎么', '知道', '觉得', '感觉', '起来', '不了', '分钟', '确实', '他们', '这样', '不是',
         '应该', '我们',
         '那个', '不是', '一下'
         }
cloud_mask = np.array(Image.open("nba_logo.jpg"))
wc = WordCloud(
    mask=cloud_mask,
    background_color="white",  # 背景颜色
    max_words=500,  # 显示最大词数
    font_path=r"C:\Windows\Fonts\STXINGKA.TTF",  # 使用字体
    min_font_size=16,
    max_font_size=50,
    width=650,  # 图幅宽度,
    height=358,
    stopwords=stops
)
wc.generate(words_text)
wc.to_file("western_final.png")
