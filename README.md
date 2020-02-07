# Sub PJT 3. 딥 러닝 모델을 이용한 챗봇 구현



텍스트 전 처리 기법과 머신러닝 기법을 응용하여 딥 러닝 기반의 챗봇을 구현



![](./img/intro.gif)



### URL

[http://13.125.199.238:5000](http://13.125.199.238:5000/)



### Team

팀명: Think B

팀원: 조호근, 김훈, 양시영, 안현상, 김초희, 이지선



### Project Period

기간: 2019/09/09 ~ 2019/10/11





## 목표



- 질문과 대답으로 이루어진 데이터를 읽고 트레이닝 데이터와 테스트 데이터로 저장하기
- Noise Canceling, Tokenizing 하기
- token 사전 vocabularyData.voc 파일 만들기
- 인코딩, 디코딩용 함수 만들기
- Transformer모델을 이용해 학습하기
- predict.py를 구현하여 새로운 질문에 대답 데이터 출력하기
- 정확도 평가를 위한 BLEU, Rouge Score 구하기
- Python Slack Client를 사용하여 Flask 서버 app.py 구현하기
- Chatbot과 대화할 용도의 Web을 Flask 서버로 구현하기
- Flask를 restful flask로 변경하기

- Vue.js를 이용하여 웹 페이지 구현하기

- Chatbot에 대화 데이터 추가 요청하기





## Learming Data



| Title       | Contents                                         |
| ----------- | ------------------------------------------------ |
| 데이터 이름 | Chatbot data                                     |
| 데이터 용도 | 한국어 챗봇 학습을 목적으로 사용한다.            |
| 데이터 권한 | MIT 라이센스                                     |
| 데이터 출처 | https://github.com/songys/Chatbot_data(송영숙님) |





### WordCloud



- Question Data

![](./img/wordcloud_in.png)



- Answer Data

![](./img/wordcloud_out.png)





## Requirement



```
Flask==0.12.2
Flask-Cors==3.0.8
Flask-RESTful==0.3.7
JPype1==0.7.0
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.0
konlpy==0.5.1
nltk==3.4.3
numpy==1.16.3
openpyxl==2.6.3
pandas==0.24.2
Pillow==6.1.0
Python==3.7.4
scikit-learn==0.20.3
scipy==1.2.1
slackclient==2.1.0
slackeventsapi==2.1.0
tensorboard==1.14.0
tensorflow-estimator==1.14.0
tensorflow-gpu==1.14.0
tqdm==4.36.0
wordcloud==1.5.0
xlrd==1.2.0
```





## Directory Structure



| Base 프로젝트                                                | 설명                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Data_in/<br />      chatbotdata.csv<br />Data_out/<br />      vocabularyData.voc<br />check_point<br />Configs.py<br />Data.py<br />Main.py<br />Model.py<br />Predict.py<br />app.py<br />db_init.py<br />app.db | - 트레이닝 데이터 영역<br />- 트레이닝 데이터 파일<br />- 출력 데이터 영역<br />- 단어 사전 파일<br />- 학습된 모델의 check_point 저장 공간<br />- 모델 설정 소스<br />- 전 처리 및 모델에 주입되는 데이터셋 구성<br />- 학습을 실행하는 소스<br />- tensorflow seq2seq 모델 소스<br />- 학습된 모델로 예측하는 소스<br />- Flask 서버 소스<br />- app.db 파일을 생성하는 소스<br />- SQLite로 생성된 db 파일 |





## Execution Result



### Slack

![](./img/slack.PNG)





### Chatbot - Web

실제 Think B를 실행하는 예시 화면이다.

![](./img/chat.gif)





### Teaching - Web

Think B에게 새로운 대화를 가르치는 과정의 예시입니다. 

![](./img/teaching.gif)