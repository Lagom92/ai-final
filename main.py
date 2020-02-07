import tensorflow as tf
import model as ml
import data
import numpy as np
import os
import sys

from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
from rouge import Rouge

from configs import DEFINES

DATA_OUT_PATH = './data_out/'


# Req. 1-5-1. bleu score 계산 함수
def bleu_compute(hyps, refs):
    chencherry = SmoothingFunction()
    scores = sentence_bleu(refs, hyps, smoothing_function=chencherry.method1)
    return scores


# Req. 1-5-2. rouge score 계산 함수
def rouge_compute(hyps, refs):
    rouge = Rouge()
    scores = rouge.get_scores(hyps, refs, avg=True)
    return scores


# Serving 기능을 위하여 serving 함수를 구성한다.
def serving_input_receiver_fn():
    receiver_tensor = {
        'input': tf.compat.v1.placeholder(dtype=tf.int32, shape=(1, DEFINES.max_sequence_length)),
        'output': tf.compat.v1.placeholder(dtype=tf.int32, shape=(1, DEFINES.max_sequence_length)),
        'target': tf.compat.v1.placeholder(dtype=tf.int32, shape=(1, DEFINES.max_sequence_length))
    }
    features = {
        key: tensor for key, tensor in receiver_tensor.items()
    }

    return tf.compat.v1.estimator.export.ServingInputReceiver(features, receiver_tensor)


# Req. 1-5-3. main 함수 구성
def main(self):
    data_out_path = os.path.join(os.getcwd(), DATA_OUT_PATH)
    os.makedirs(data_out_path, exist_ok=True)

    char2idx, idx2char, vocabulary_length = data.load_voc()
    train_q, train_a, test_q, test_a = data.load_data()

    train_input_enc, _ = data.enc_processing(train_q, char2idx)
    train_output_dec, _ = data.dec_output_processing(train_a, char2idx)
    train_target_dec = data.dec_target_processing(train_a, char2idx)

    eval_input_enc, _ = data.enc_processing(test_q, char2idx)
    eval_output_dec, _ = data.dec_output_processing(test_a, char2idx)
    eval_target_dec = data.dec_target_processing(test_a, char2idx)

    check_point_path = os.path.join(os.getcwd(), DEFINES.check_point_path)
    save_model_path = os.path.join(os.getcwd(), DEFINES.save_model_path)
    os.makedirs(check_point_path, exist_ok=True)
    os.makedirs(save_model_path, exist_ok=True)

    # 에스티메이터 구성한다.
    classifier = tf.estimator.Estimator(
        model_fn=ml.Model,  # 모델 등록한다.
        model_dir=DEFINES.check_point_path,  # 체크포인트 위치 등록한다.
        params={  # 모델 쪽으로 파라메터 전달한다.
            'model_hidden_size': DEFINES.model_hidden_size,  # 가중치 크기 설정한다.
            'ffn_hidden_size': DEFINES.ffn_hidden_size,
            'attention_head_size': DEFINES.attention_head_size,
            'learning_rate': DEFINES.learning_rate,  # 학습율 설정한다.
            'vocabulary_length': vocabulary_length,  # 딕셔너리 크기를 설정한다.
            'embedding_size': DEFINES.embedding_size,  # 임베딩 크기를 설정한다.
            'layer_size': DEFINES.layer_size,
            'max_sequence_length': DEFINES.max_sequence_length,
            'tokenize_as_morph': DEFINES.tokenize_as_morph,
            'serving': DEFINES.serving # 모델 저장 및 serving 유무를 설정한다.
        })

    # 학습 실행
    classifier.train(input_fn=lambda: data.train_input_fn(
        train_input_enc, train_output_dec, train_target_dec, DEFINES.batch_size), steps=DEFINES.train_steps)

    # 모델 저장
    if DEFINES.serving == True:
        classifier.export_saved_model(export_dir_base=DEFINES.save_model_path, serving_input_receiver_fn=serving_input_receiver_fn)

    # 평가 실행
    eval_result = classifier.evaluate(input_fn=lambda: data.eval_input_fn(
        eval_input_enc, eval_output_dec, eval_target_dec, DEFINES.batch_size))
    print('\nEVAL set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

    # 테스트
    predic_input_enc, _ = data.enc_processing(["가끔 궁금해"], char2idx)
    predic_output_dec, _ = data.dec_output_processing([""], char2idx)
    predic_target_dec = data.dec_target_processing([""], char2idx)

    predictions = classifier.predict(input_fn=lambda:data.eval_input_fn(predic_input_enc, predic_output_dec, predic_target_dec, 1))

    answer, _ = data.pred_next_string(predictions, idx2char)

    # 예측한 값을 인지 할 수 있도록
    # 텍스트로 변경하는 부분이다.
    print("answer: ", answer)
    print("Bleu score: ", bleu_compute("그 사람도 그럴 거예요.", answer))
    print("Rouge score: ", rouge_compute("그 사람도 그럴 거예요.", answer))

if __name__ == '__main__':
    tf.app.run(main)
