from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import math
import numpy as np

def read_article(file_name):
    file = open(file_name,'r')
    filedata= file.readlines()
    print(filedata)
    return filedata

def separate_sentence(filedata):
    sep_sentence = filedata[0].split('. ')
    return sep_sentence

def sep_word(sep_sentence):
    sep_word_in_sentence = []
    for i in sep_sentence:
        sep_word_in_sentence.append(i.split(' '))
    return sep_word_in_sentence

def sep_word_in_sent(sep_word_in_sentence):
    world_list = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']
    imp_word_in_sentence = []
    for sen in sep_word_in_sentence:
        list1= []
        for word in sen:
            if word not in world_list:
                list1.append(word)
        imp_word_in_sentence.append(list1)
    return imp_word_in_sentence

def sentence_similarity(sentence1, sentence2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sentence1 = [word.lower() for word in sentence1]
    sentence2 = [word.lower() for word in sentence2]
 
    all_words = list(set(sentence1 + sentence2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    for w in sentence1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    for w in sentence2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
    
def create_matrix(imp_word_in_sentence):
    matrix = np.zeros((len(imp_word_in_sentence), len(imp_word_in_sentence)))
    return matrix


def create_similarity_matrix(matrix,imp_word_in_sentence,stop_words):
    for i in range(len(imp_word_in_sentence)):
        for j in range(len(imp_word_in_sentence)):
            if i == j:
                continue
        matrix[i][j]= sentence_similarity(imp_word_in_sentence[i],imp_word_in_sentence[j],stop_words)
    return matrix

def rank(similarity_matrix,imp_word_in_sentence):
    sc= []
    for i in range(len(imp_word_in_sentence)):
        sum = 0
        for j in range(len(imp_word_in_sentence)):
            sum = sum + similarity_matrix[i][j]
        sc.append(sum)
    
    score = {}
    for i in sc:
        score.update({sc.index(i):i})

    new = sorted(score.items(), key=lambda x: x[1], reverse=True)

    rank = []
    for i in new:
        rank.append(i[0])

    return rank

def summary_sent(rank_list,per):
    per = per/100
    final_list = []
    final_list  = rank_list[0:math.ceil(len(rank_list) * per)]
    return final_list

def summary(final_list,sep_sentence):
    summary = []
    for i in final_list:
        summary.append((sep_sentence[i]))
    return summary
    

def create_summary(file_name,per):
    filedata = read_article(file_name)
    sep_sentence = separate_sentence(filedata)
    sep_word_in_sentence = sep_word(sep_sentence)
    imp_word_in_sentence = sep_word_in_sent(sep_word_in_sentence)
    matrix = create_matrix(imp_word_in_sentence)
    stop_words = stopwords.words('english')
    similarity_matrix = create_similarity_matrix(matrix,imp_word_in_sentence,stop_words)
    rank_list = rank(similarity_matrix,imp_word_in_sentence)
    final_list = summary_sent(rank_list,per)
    summary_text = summary(final_list,sep_sentence)
    print(summary_text)


create_summary('source.txt', 50)



