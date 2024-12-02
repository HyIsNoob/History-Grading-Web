import math
import underthesea
import os
import json
import time


class Tfidf:
    def __init__(self):
        self.Input = []
        self.WordDict = {}
        self.size = 0
        self.AvoidChar = ['và', 'thì', 'với', 'nhưng', 'do', 'tại', 'ngày', 'bởi', 'thường', 'người', 'các', 'những',
             'mà', 'có', 'được', 'không', 'trong', 'rất', 'là', 'của', 'từ', 'cho', 'một', 'đến', 'tới', 'anh',
             'mấy', 'ông', 'em', 'tôi', 'cô', 'dì', 'chú', 'bác', 'con'
            ]


    def Vectorize(self, InputDir):
        self.tf = []
        self.df = {}
        self.Vectors = []

        def normalize(word_dict):
            dict_max = -1
            for Word in word_dict:
                if dict_max < word_dict[Word]:
                    dict_max = word_dict[Word]
            for Word in word_dict:
                word_dict[Word] = word_dict[Word]/dict_max
            return word_dict

        # MAKE DF AND WORD DICT
        for FileName in os.listdir(InputDir):
            CheckExist = {}
            txt_file = open(f"{InputDir}/{FileName}", "r")
            text_sentence = txt_file.read()
            self.Input.append(text_sentence.lower())
            WordToken = underthesea.word_tokenize(text_sentence)
            for Word in WordToken:
                if (len(Word) > 1 and Word not in self.AvoidChar):
                    if (Word not in self.WordDict):
                        self.WordDict[Word] = 0

                    if (Word not in self.df):
                        self.df[Word] = 1
                    elif (Word not in CheckExist):
                        self.df[Word] += 1
                        CheckExist[Word] = True
            print(f"Done collecting words of file {FileName}")
        print("Done collecting all words")

        # MAKE TF
        DocIndex = 0
        for text_sentence in self.Input:
            WordToken = underthesea.word_tokenize(text_sentence)
            self.tf.append(self.WordDict.copy())
            for Word in WordToken:
                if (len(Word) > 1 and Word in self.WordDict):
                    self.tf[DocIndex][Word] += 1
            self.tf[DocIndex] = normalize(self.tf[DocIndex])
            DocIndex += 1
            print(f"Done tf of {DocIndex-1}")

        # MAKE TFIDF
        for i in range(len(self.tf)):
            tfidf_dict = {}
            for Word in self.tf[i]:
                tfidf_dict[Word] = math.log2(len(self.Input)/self.df[Word]) * self.tf[i][Word]
            self.Vectors.append(tfidf_dict)
            print(f"Done tfidf of {i-1}")
            print(f"Sum of {i-1}: {sum(tfidf_dict.values())}")

        return self.Vectors


class trained_model:
    def __init__(self, tf, df, tf_idf, WordDict):
        self.tf = tf.copy()
        self.df = df.copy()
        self.tf_idf = tf_idf.copy()
        self.WordDict = WordDict.copy()


if __name__ == "__main__":
    tfidf = Tfidf()
    print("Start training...")
    main_vector = tfidf.Vectorize("history_train")
    print('Done training...')
    print("Please wait for exit...")
    #print(tfidf.tf)

    timestr = time.strftime("%Y%m%d-%H%M%S")

    listdir_len = int(len(os.listdir("models"))/4)

    with open(f"models/model_{listdir_len}_tfidf_vectors.json", "w") as ModelFile:
        json.dump(main_vector, ModelFile)
    with open(f"models/model_{listdir_len}_tfidf_tf.json", "w") as ModelFile:
        json.dump(tfidf.tf, ModelFile)
    with open(f"models/model_{listdir_len}_tfidf_df.json", "w") as ModelFile:
        json.dump(tfidf.df, ModelFile)
    with open(f"models/model_{listdir_len}_tfidf_worddict.json", "w") as ModelFile:
        json.dump(tfidf.WordDict, ModelFile)

    print("Exit...")