from konlpy.tag import Okt
import pandas as pd
import tensorflow as tf
import enum
import os
import re
from sklearn.model_selection import train_test_split
import numpy as np
from configs import DEFINES

from tqdm import tqdm

PAD = "<PAD>"
STD = "<STD>"
END = "<END>"
UNK = "<UNK>"

PAD_INDEX = 0
STD_INDEX = 1
END_INDEX = 2
UNK_INDEX = 3

MARKER = [PAD, STD, END, UNK]


# Req 1-1-1. 데이터를 읽고 트레이닝 셋과 테스트 셋으로 분리
def load_data():
    db = pd.read_csv("./data_in/ChatBotData.csv")
    train, test = train_test_split(db)
    train_q, train_a = train["Q"], train["A"]
    test_q, test_a = test["Q"], test["A"]
    
    return train_q, train_a, test_q, test_a


# Req 1-1-2. 텍스트 데이터에 정규화를 사용하여 ([~.,!?\"':;)(]) 제거
def prepro_noise_canceling(data):
    noise_filter = re.compile("([~.,!?\"':;)(])")
    non_noise_data_list = []
    
    for d in data:
        non_noise_data = re.sub(noise_filter, "", d)
        non_noise_data_list.append(non_noise_data)

    return non_noise_data_list


# Req 1-1-3. 텍스트 데이터에 토크나이징
def tokenizing_data(data):
    tokens_list = []
    data = prepro_noise_canceling(data)

    for d in data:
        for token in d.split():
            if token:
                tokens_list.append(token)
    return tokens_list


# 형태소 분석
def prepro_like_morphlized(data):
    okt = Okt()
    result_data = []

    for seq in data:
        tokens = okt.morphs(seq)
        morphlized_seq = " ".join(tokens)
        result_data.append(morphlized_seq)

    return result_data


# Req 1-2-1. 토큰화된 트레이닝 데이터를 인코더에 활용할 수 있도록 전 처리
def enc_processing(value, dictionary):
    seq_input_index = []
    seq_len = []

    value = prepro_noise_canceling(value)
    value = prepro_like_morphlized(value)
        
    for seq in value:
        seq_index = []
        
        for word in seq.split():
            if dictionary.get(word) is not None:
                seq_index.append(dictionary[word])
            else:
                seq_index.append(dictionary[UNK])
                
        if len(seq_index) > DEFINES.max_sequence_length:
            seq_index = seq_index[:DEFINES.max_sequence_length]
            
        seq_len.append(len(seq_index))
        seq_index += [dictionary[PAD]] * (DEFINES.max_sequence_length - len(seq_index))
        seq_input_index.append(seq_index)
        
    return np.asarray(seq_input_index), seq_len


# Req 1-2-2. 디코더에 필요한 데이터 전 처리 
def dec_output_processing(value, dictionary):
    seq_output_index = []
    seq_len = []

    value = prepro_noise_canceling(value)

    if DEFINES.tokenize_as_morph:
        value = prepro_like_morphlized(value)
    
    for seq in value:
        seq_index =[]
        
        seq_index = [dictionary[STD]] + [dictionary[word] for word in seq.split()]
                
        if len(seq_index) > DEFINES.max_sequence_length:
            seq_index = seq_index[:DEFINES.max_sequence_length]
            
        seq_len.append(len(seq_index))
        seq_index += [dictionary[PAD]] * (DEFINES.max_sequence_length - len(seq_index))
        seq_output_index.append(seq_index)
    
    return np.asarray(seq_output_index), seq_len


# Req 1-2-3. 디코더에 필요한 데이터 전 처리 
def dec_target_processing(value, dictionary):
    seq_target_index = []

    value = prepro_noise_canceling(value)

    if DEFINES.tokenize_as_morph:
        value = prepro_like_morphlized(value)
    
    for seq in value:
        seq_index = [dictionary[word] for word in seq.split()]
        seq_index = seq_index[:DEFINES.max_sequence_length-1] + [dictionary[END]]
        seq_index += [dictionary[PAD]] * (DEFINES.max_sequence_length - len(seq_index))
        seq_target_index.append(seq_index)
   
    return np.asarray(seq_target_index)


# input과 output dictionary를 만드는 함수
def in_out_dict(input, output, target):
    features = {"input": input, "output": output}
    return features, target


# 학습에 들어가 배치 데이터를 만드는 함수
def train_input_fn(train_input_enc, train_output_dec, train_target_dec, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((train_input_enc, train_output_dec, train_target_dec))
    dataset = dataset.shuffle(buffer_size=len(train_input_enc))

    assert batch_size is not None, "train batchSize must not be None"
    
    dataset = dataset.batch(batch_size, drop_remainder=True)
    dataset = dataset.map(in_out_dict)
    dataset = dataset.repeat()
    iterator = dataset.make_one_shot_iterator()

    return iterator.get_next()


# 평가에 들어가 배치 데이터를 만드는 함수
def eval_input_fn(eval_input_enc, eval_output_dec, eval_target_dec, batch_size):
    dataset = tf.data.Dataset.from_tensor_slices((eval_input_enc, eval_output_dec, eval_target_dec))
    dataset = dataset.shuffle(buffer_size=len(eval_input_enc))

    assert batch_size is not None, "eval batchSize must not be None"

    dataset = dataset.batch(batch_size, drop_remainder=True)
    dataset = dataset.map(in_out_dict)
    dataset = dataset.repeat(1)
    iterator = dataset.make_one_shot_iterator()

    return iterator.get_next()


# Req 1-3-3. 예측용 단어 인덱스를 문장으로 변환
def pred2string(value, dictionary):
    string_list = []
    
    for v in value:
        for index in v["indexs"]:
            string_list.append(dictionary[index])
    
    answer = ""
    
    for word in string_list:
        if word not in PAD and word not in END:
            answer += word
            answer += " "
            
    return answer


def pred_next_string(value, dictionary):
    string_list = []
    is_finished = False
    
    for v in value:
        for index in v["indexs"]:
            string_list.append(dictionary[index])
    
    answer = ""
    
    for word in string_list:
        if word == END:
            is_finished = True
            break

        if word != PAD and word != END:
            answer += word
            answer += " "
            
    return answer, is_finished


def model_pred(value, dictionary):
    string_list = []

    for index in value["indexs"][0]:
        string_list.append(dictionary[index])

    answer = ""

    for word in string_list:
        if word == END:
            break

        if word != PAD and word != END:
            answer += word
            answer += " "
            
    return answer


# Req 1-3-1. 단어 사전 파일 vocabularyData.voc를 생성하고 단어와 인덱스 관계를 출력
def load_voc():
    voc_list = []

    if (not (os.path.exists(DEFINES.vocabulary_path))):
        data_df = pd.read_csv(DEFINES.data_path, encoding="utf-8")
        question, answer = data_df["Q"], data_df["A"]

        question = prepro_noise_canceling(question)
        answer = prepro_noise_canceling(answer)

        question = prepro_like_morphlized(question)

        if DEFINES.tokenize_as_morph:
            answer = prepro_like_morphlized(answer)

        data = []
        data.extend(question)
        data.extend(answer)

        words = tokenizing_data(data)
        
        words = list(set(words))
        
        words[:0] = MARKER
        
        # 사전 파일을 생성 
        with open(DEFINES.vocabulary_path, 'w', encoding='utf-8') as voc_file:
            for word in words:
                voc_file.write(word + "\n")
           
    # 사전 파일에서 단어(토큰)을 가져와 voc_list에 저장
    with open(DEFINES.vocabulary_path, 'r', encoding='utf-8') as voc_file:
        for line in voc_file:
            voc_list.append(line.strip())

    char2idx, idx2char = make_voc(voc_list)

    return char2idx, idx2char, len(char2idx)


# Req 1-3-2. 사전 리스트를 받아 인덱스와 토큰의 dictionary를 생성
def make_voc(voc_list):
    word_to_idx = {word: idx for idx, word in enumerate(voc_list)}
    idx_to_word = {idx: word for idx, word in enumerate(voc_list)}
    return word_to_idx, idx_to_word

    
def main(self):
    char2idx, idx2char, voc_length = load_voc()
    return char2idx, idx2char, voc_length

if __name__ == '__main__':
    tf.app.run(main)
