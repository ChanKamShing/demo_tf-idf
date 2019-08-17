import os
import math

file_path = './allfiles'

# 生成停用词字典
stop_set = set()
with open("./stop_list.txt",'r',encoding='utf-8') as f:
    for word in f.readlines():
        stop_set.add(word.strip())
        # stop_set.add(word)    #strip()除了去掉空格，还去掉制表符，如\t， \n等

# print(stop_set)

doc_words = dict() # 创造{doc_name: {word_set}}格式数据
doc_num = 0    #统计文章数量

#获取doc和对应的每篇文章的词频TF
for filename in os.listdir(file_path):
    with open(os.path.join(file_path,filename),'r',encoding='utf-8') as f:
        # print(f.readlines())
        # 统计后的word_freq的key是每一个词，key是不会有重复的
        word_freq = dict()
        sum_cnt = 0
        max_tf = 0  #统计出现次数最多的词的次数
        # readlines()是一个List[AnyStr]对象，每一个元素就是一行
        for line in f.readlines():
            # 将每一行进行去空格，并根据' '切分
            words = line.strip().split(' ')
            # print(words)
            for word in words:
                if len(word.strip())<1 or word.strip() in stop_set:
                    # 该词为空，或者在停用词列表里面，直接跳过
                    continue
                if word_freq.get(word,-1) == -1:
                    word_freq[word] = 1
                else:
                    word_freq[word] += 1
                if max_tf<word_freq[word]:
                    max_tf = word_freq[word]
                sum_cnt+=1
        # print(word_freq)

        #占比方式处理
        for word in word_freq.keys():
            # word_freq[word] /= sum_cnt
            word_freq[word] /= max_tf
            # if word_freq[word] == 1:
            #     print("value:",word)
        # print(word_freq)

        doc_words[filename] = word_freq
        doc_num += 1
        break

# print(doc_words)

# 统计每个词的doc_freq(df)，其key组成的集合构成词库
doc_freq = dict()

# 遍历doc_words
for doc in doc_words.keys():
    # 再基于单个文件，遍历所有的key，即遍历每个词，
    # word属于doc_word[doc]的key，即只存在一个，统计结果即代表拥有word这个词的文章数
    for word in doc_words[doc].keys():
        if doc_freq.get(word,-1)==-1:
            doc_freq[word] = 1
        else:
            doc_freq[word]+=1
    # print(doc_freq)
    # break

# 计算idf
for word in doc_freq.keys():
    # 计算后的deoc_freq[word]的value为idf
    doc_freq[word] = math.log(doc_num/float(doc_freq[word]+1),10)

# 计算df*idf
for doc in doc_words.keys():
    for word in doc_words[doc].keys():
        doc_words[doc][word] *= doc_freq[word]
    # print(doc_words)
    # break
# for doc in doc_words.keys():
#     for item in doc_words[doc].items():
#         print(type(item))
#         print("x:",item[0],"y:",item[1])
#         break
#     break
# print(sorted(doc_words['3business.seg.cln.txt'].items(), key=lambda x: x[1], reverse=False)[:10])