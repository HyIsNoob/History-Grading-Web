import math
import os
import underthesea
from . import tfidf
import json
import numpy as np

def similarity(model, input_1, input_2):
    def normalize(word_dict):
            dict_max = -1
            # print()pyth
            # print("Word dict: ")
            for Word in word_dict:
                #print(word_dict[Word])
                if dict_max < word_dict[Word]:
                    dict_max = word_dict[Word]
            for Word in word_dict:
                word_dict[Word] = word_dict[Word]/dict_max
            return word_dict 

    def compute_tf(StringIn_1, StringIn_2):
        word_token_1 = underthesea.word_tokenize(StringIn_1)
        word_token_2 = underthesea.word_tokenize(StringIn_2)

        input_tf_1 = {}
        input_tf_2 = {}

        for word in word_token_1:
            if (word in model.WordDict and word not in AvoidChar):
                input_tf_1[word] = model.WordDict[word]
                input_tf_2[word] = model.WordDict[word]
            elif(word not in AvoidChar):
                input_tf_1[word] = 0
                input_tf_2[word] = 0

        for word in word_token_2:
            if (word in model.WordDict and word not in AvoidChar):
                input_tf_1[word] = model.WordDict[word]
                input_tf_2[word] = model.WordDict[word]
            elif(word not in AvoidChar):
                input_tf_1[word] = 0
                input_tf_2[word] = 0

        for word in word_token_1:
            if (word not in AvoidChar):
                input_tf_1[word] += 1
            
        for word in word_token_2:
            if(word not in AvoidChar):
                input_tf_2[word] += 1
           

        input_tf_2 = normalize(input_tf_2)
        input_tf_1 = normalize(input_tf_1)

        return input_tf_1, input_tf_2
    
    def compute_df(StringIn_1, StringIn_2):
        CheckExist = {}
        input_df = {}
        word_token = underthesea.word_tokenize(StringIn_1)
        for Word in word_token:
            if Word in model.df and Word not in AvoidChar:
                #print(f"insert word {Word}")
                input_df[Word] = model.df[Word] + 1
                CheckExist[Word] = True
            elif (Word not in CheckExist) and Word not in AvoidChar:
                #print(f"increase word {Word}")
                input_df[Word] = 1
                CheckExist[Word] = True

        CheckExist = {}
        word_token = underthesea.word_tokenize(StringIn_2)
        for Word in word_token:
            if (Word in input_df):
                input_df[Word] += 1
                CheckExist[Word] = True
            elif (Word in model.df):
                input_df[Word] = model.df[Word] + 1
                CheckExist[Word] = True
            else:
                input_df[Word] = 1
                CheckExist[Word] = True

        return input_df

    def compute_tf_idf(tf_dict, df_dict):
        tf_idf = df_dict.copy()
        for Word in tf_dict:
            tf_idf[Word] = math.log2((len(model.tf_idf)+1)/df_dict[Word]) * tf_dict[Word]
        return tf_idf

    def cosine_similarity(tfidf_dict_1, tfidf_dict_2):
        vector_1 = np.array([tfidf_dict_1[Word] for Word in tfidf_dict_1])
        vector_2 = np.array([tfidf_dict_2[Word] for Word in tfidf_dict_2])

        # print(vector_1)
        # print()
        # print(vector_2)

        cosine = np.dot(vector_1, vector_2)/(np.linalg.norm(vector_1) * np.linalg.norm(vector_2))
        
        return cosine

    AvoidChar = ['và', 'thì', 'với', 'nhưng', 'do', 'tại', 'ngày', 'bởi', 'thường', 'người', 'các', 'những',
             'mà', 'có', 'được', 'không', 'trong', 'rất', 'là', 'của', 'từ', 'cho', 'một', 'đến', 'tới', 'anh',
             'mấy', 'ông', 'em', 'tôi', 'cô', 'dì', 'chú', 'bác', 'con'
            ]
    add_word = []
    WordDict = model.WordDict.copy()
    input_1_tf, input_2_tf = compute_tf(input_1, input_2)
    #print(f"TF_1 length:{len(input_1_tf)}")
    #print(f"TF_2 length:{len(input_2_tf)}")
    input_df = compute_df(input_1, input_2)
    #print(f"DF:{input_df}")
    #print(f"DF_2 length:{len(input_2_df)}")
    tf_idf_1 = compute_tf_idf(input_1_tf, input_df)
    #print(f"TFIDF_1: {tf_idf_1}")
    tf_idf_2 = compute_tf_idf(input_2_tf, input_df)
    #print(f"TFIDF_2 {tf_idf_2}")
    cos_sim = cosine_similarity(tf_idf_1, tf_idf_2)

    return cos_sim


def MakeModel(model_version):
    model1 = f'baitap/models/model_{model_version}_tfidf_tf.json'
    model2 = f'baitap/models/model_{model_version}_tfidf_df.json'
    model3 = f'baitap/models/model_{model_version}_tfidf_vectors.json'
    model4 = f'baitap/models/model_{model_version}_tfidf_worddict.json'

    tf_file = open(model1,'r', encoding = "utf8")
    tf = json.loads(tf_file.read())
    df_file = open(model2,'r', encoding = "utf8")
    df = json.loads(df_file.read())
    tfidf_file = open(model3,'r', encoding = "utf8")
    tfidf_vector = json.loads(tfidf_file.read())
    worddict_file = open(model4,'r', encoding = "utf8")
    worddict = json.loads(worddict_file.read())

    tfidf_model = tfidf.trained_model(tf, df, tfidf_vector, worddict)

    return tfidf_model

if __name__ == "__main__":
    input_1 = open("baitap/example/doc_1.txt", "r").read().lower()
    input_2 = open("baitap/example/doc_2.txt", "r").read().lower()
    tfidf_model = MakeModel(0)

    for i in range(2):
        print()

    print(f"Điểm: {similarity(tfidf_model, input_1, input_2)*10}")
