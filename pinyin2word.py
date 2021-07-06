# -*- coding:utf-8 -*-

# ARPAbet元素可能被听成的拼音元素
dictARPAbet2Pinyin = {
    'AA': {'A', 'O'},
    'AE': {'A', 'E', 'AI'},
    'AH': {'A', 'E'},
    'AO': {'A', 'O'},
    'AW': {'A', 'AO'},
    'AY': {'A', 'AI'},
    'B': {'B'},
    'CH': {'Q', 'CH', 'SH', 'X'},
    'D': {'D'},
    'DH': {'TH', 'SH', 'S', 'X'},
    'EH': {'E', 'AI', 'EI'},
    'ER': {'E', 'ER'},
    'EY': {'E', 'EI'},
    'F': {'F'},
    'G': {'G'},
    'HH': {'H'},
    'IH': {'I'},
    'IY': {'I'},
    'JH': {'J'},
    'K': {'K'},
    'L': {'L', 'N', 'R'},
    'M': {'M'},
    'N': {'N', 'L', 'R'},
    'NG': {'NG'},
    'OW': {'O', 'OU', 'E'},
    'OY': {'OY', 'OI', 'OYI'},
    'P': {'P'},
    'R': {'R', 'L', 'N'},
    'S': {'S', 'C'},
    'SH': {'X', 'SH', 'CH', 'Q'},
    'T': {'T'},
    'TH': {'TH', 'SH', 'CH'},
    'UH': {'U', 'W'},
    'UW': {'U', 'W'},
    'V': {'V', 'W', 'F'},
    'W': {'W', 'U'},
    'Y': {'Y'},
    'Z': {'Z', 'S'},
    'ZH': {'J', 'SH', 'X'}
}

# 拼音元素集合
PinyinElement = {
    'A', 'AI', 'AO', 
    'B', 
    'C', 'CH', 
    'D', 
    'E', 'EI', 'ER', 
    'F', 
    'G', 
    'H', 
    'I', 
    'J', 
    'K', 
    'L', 
    'M', 
    'N', 'NG', 
    'O', 'OI', 'OU', 'OY', 'OYI', 
    'P', 
    'Q', 
    'R', 
    'S', 'SH', 
    'T', 'TH', 
    'U', 
    'V', 
    'W', 
    'X', 
    'Y', 
    'Z'
}

# 将输入的拼音拆成多个拼音元素
def split_pinyin(word: str):
    pinyin_list = []
    filtered_word = "".join(list(filter(str.isalpha, word))).upper() # 过滤非字母并转换为大写
    i = 0
    while i < len(filtered_word):
        j = i + 1
        while filtered_word[i:j] in PinyinElement and j <= len(filtered_word):
            j += 1
        j -= 1
        pinyin_list.append(filtered_word[i:j])
        i = j
    return pinyin_list

Searching: bool = True

class ARPAbet():
    def __init__(self, dictLine: str):
        tmplist = dictLine.split('#')[0].split()
        self.word = tmplist[0]
        self.arpabet = tmplist[1:]
        for i in range(len(self.arpabet)):
            if self.arpabet[i][-1].isdigit():
                self.arpabet[i] = self.arpabet[i][:-1]
        self.__levRecord = dict()
    
    def __isEqualArpabetPinyinElem(arpabetElem, pinyinElem):
        return pinyinElem in dictARPAbet2Pinyin[arpabetElem]
    
    # 备忘录方法实现Levenshtein距离计算
    def __lev(self, arpabet, pinyin):
        if (len(arpabet), len(pinyin)) in self.__levRecord:
            return self.__levRecord[(len(arpabet), len(pinyin))]
        if len(arpabet) == 0:
            self.__levRecord[(len(arpabet), len(pinyin))] = len(pinyin)
            return len(pinyin)
        if len(pinyin) == 0:
            self.__levRecord[(len(arpabet), len(pinyin))] = len(arpabet)
            return len(arpabet)
        if ARPAbet.__isEqualArpabetPinyinElem(arpabet[0], pinyin[0]):
            answer = self.__lev(arpabet[1:], pinyin[1:])
            self.__levRecord[(len(arpabet), len(pinyin))] = answer
            return answer
        answer1 = self.__lev(arpabet[1:], pinyin)
        answer2 = self.__lev(arpabet, pinyin[1:])
        answer3 = self.__lev(arpabet[1:], pinyin[1:])
        answer = 1 + min(answer1, answer2, answer3)
        self.__levRecord[(len(arpabet), len(pinyin))] = answer
        return answer

    # 返回arpabet到某个拼音的Levenshtein距离
    def Levenshtein2Pinyin(self, pinyin):
        self.__levRecord = dict()
        return self.__lev(self.arpabet, pinyin)

class ARPAbetDict():
    # 将词典载入内存
    def __init__(self, filepath: str):
        self.dict = []
        f = open(filepath, 'r')
        for line in f.readlines():
            if not line.isspace():
                self.dict.append(ARPAbet(line))
        f.close()
        self.dictLen = len(self.dict)
    
    # 在词典中搜索和拼音发音相近的单词
    def search_pinyin(self, pinyin):
        global Searching
        Searching = True
        count = 0
        resultNum = 0
        for arpabetInstance in self.dict:
            levDistance = arpabetInstance.Levenshtein2Pinyin(pinyin)
            if levDistance / len(pinyin) <= 0.25:
                print("%20s   | " % arpabetInstance.word, end='')
                print("%d |   " % levDistance, end='')
                for elem in arpabetInstance.arpabet:
                    print(elem, end=' ')
                print()
                resultNum += 1
            count += 1
            print("进度：%d/%d，已找到：%d\t\t\t" % (count, self.dictLen, resultNum), end='\r')
            if not Searching:
                break
        print()

import signal
def signal_handler(sig, frame):
    global Searching
    Searching = False

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    d = ARPAbetDict("cmudict.dict")
    print("请输入和单词发音相近的拼音：")
    while True:
        pinyin = split_pinyin(input('> '))
        print(pinyin)
        if len(pinyin) >= 1:
            d.search_pinyin(pinyin)
