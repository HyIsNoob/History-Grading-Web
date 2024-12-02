import math
import os
import underthesea
import tfidf
import json
import numpy as np
import logging    # first of all import the module
logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This message will get logged on to a file')
import mysql.connector
import datetime
from underthesea import word_tokenize, pos_tag

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
    model1 = f'models/model_{model_version}_tfidf_tf.json'
    model2 = f'models/model_{model_version}_tfidf_df.json'
    model3 = f'models/model_{model_version}_tfidf_vectors.json'
    model4 = f'models/model_{model_version}_tfidf_worddict.json'

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
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="testhistory"
        )     
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM CAUHOI")
    #
    # 
    # UPDATE CAUHOI SET KEYTRALOI = "" WHERE MACAUHOI = 3
    # INSERT INTO CAUTRALOI (MACAUHOI, CAUTRALOI) VALUES ("3", "TRa loi 1")
    # INSERT INTO CAUHOI (cauhoi, dapan) VALUES ("Cau hoi1", "Dap an1")
    #
    #
    myresult = mycursor.fetchall()
    for x in myresult:
        MACAUHOI = x[0]
        CAUHOI = x[1]
        DAPAN = x[2]
        START = datetime.datetime.now()
        END = 0
        COUNT = 0
        sql1 = "SELECT * FROM CAUTRALOI WHERE MACAUHOI='%s';"
        val = (MACAUHOI,)
        mycursor.execute(sql1, val)
        myresult1 = mycursor.fetchall()
        MAX = mycursor.rowcount
        for y in myresult1:
            CAUTRALOi = y[2]
            MAUCAUTRALOI = y[1]
            input1 = DAPAN
            input2 = CAUTRALOi
            print('\n')
            print("Câu Hỏi: ", end='')
            print(CAUHOI)
            print("Đáp Án: ", end='')
            print(DAPAN)
            print("Câu trả lời học sinh: ", end='')
            print(CAUTRALOi)
            sql2 = "SELECT KEYTRALOI FROM CAUHOI WHERE MACAUHOI = %s"
            val = (MACAUHOI,)
            mycursor.execute(sql2, val) 
            myresult3 = mycursor.fetchall()
            def convertTuple(tup):
                str = ''
                for item in tup:
                    if item == None:
                        pass
                    else:
                        str = str + item
                return str
            def listToString(s): 
                str1 = ""  
                for ele in s: 
                    str1 += ele   
                return str1 
            for z in myresult3:
                a = convertTuple(z)
                list = pos_tag(a)
                maxdem = 0
                dem = 0
                for bac in list:
                    ronglist = []
                    chu = bac[0]
                    loai = bac[1]
                    if loai == "CH" or loai == "C":
                        pass
                    elif loai != "CH" and loai != "C":
                        ronglist.append(bac[0])
                        maxdem += 1
                        pui = listToString(ronglist)
                        so = pui.lower()
                        sanh = input2.lower()
                        if so in sanh:
                            dem += 1
            print('\n')
            input_1 = input1.lower()
            input_2 = input2.lower()
            tfidf_model = MakeModel(0)
            POINT = similarity(tfidf_model, input_1, input_2)*10
            LastPoint = (dem/maxdem)*2 + POINT*0.8
            Key = (dem/maxdem)*2
            UpPointAI = round(POINT, 2)
            UpKey = round(Key, 2)
            UpPoint = round(LastPoint, 2)
            sql = "UPDATE CAUTRALOI SET SCORE = %s, AI_Point = %s, Key_Point = %s WHERE MACAUTRALOI = %s"
            val = (str(UpPoint), str(UpPointAI), str(UpKey), MAUCAUTRALOI,)
            mycursor.execute(sql, val)
            mydb.commit()
            print("Key Đúng: ", end='')
            print(dem, end='')
            print("/", end='')
            print(maxdem, end=' - ')
            print(UpKey)
            print ("DIEM: ", end='')
            print(round(LastPoint, 2), end='')
            COUNT = COUNT + 1
            if (COUNT == MAX):
                END = datetime.datetime.now()
                TIME = (END - START)/MAX
                sql = "UPDATE CAUTRALOI SET TIME = %s WHERE MACAUTRALOI = %s"
                val = (str(TIME), MAUCAUTRALOI)
                mycursor.execute(sql, val)
                mydb.commit()
                print(str(MACAUHOI)+" - Thoi gian cham: "+str(TIME))
