<template>
  <v-row class="ChatBody" align="center" justify="center">
    <v-col class="innerChat" cols="12" sm="8" md="5">
      <div id="thinkB_chat">
        <Chat 
        :participants="participants"
        :myself="myself"
        :messages="messages"
        :onType="onType"
        :onMessageSubmit="onMessageSubmit"
        :chatTitle="chatTitle"
        :placeholder="placeholder"
        :colors="colors"
        :borderStyle="borderStyle"
        :hideCloseButton="hideCloseButton"
        :closeButtonIconSize="closeButtonIconSize"
        :submitIconSize="submitIconSize"
        :asyncMode="asyncMode"/>
        <v-dialog v-model="dialog" persistent max-width="400">
          <template v-slot:activator="{ on }">
            <v-btn
              fixed
              dark
              fab
              bottom
              right
              color="pink"
              v-on="on"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <div class="text-center">
                <h3>Think B 가르치기</h3>
              </div>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <v-text-field v-model="question" label="이렇게 말하면" required></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field v-model="answer" label="이렇게 대답해요" required></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <div class="flex-grow-1"></div>
              <v-btn color="green darken-1" text @click="cancelData">취소</v-btn>
              <v-btn color="green darken-1" text @click="createData">가르치기</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import { Chat } from 'vue-quick-chat'

export default {
  name: 'Chatbot',
  components: {
    Chat
  },
  data() {
    return {
      dialog: false,
      question: "",
      answer: "",
      participants: [
        {
          name: 'ThinkB',
          id: 1
        }
      ],
      myself: {
        name: 'YOU',
        id: 2
      },
      messages: [
        {
          content: '안녕하세요 ThinkB입니다.', 
          myself: false,
          participantId: 1,
          timestamp: { year: 0, month: 0, day: 0, hour: 0, minute: 0, second: 0, millisecond: 0 },
          uploaded: true
        }
      ],
      chatTitle: 'ThinkB',
      placeholder: 'send your message',
      colors:{
        header:{
          bg: '#558B2F',
          text: '#fff',
        },
        message:{
          myself: {
            bg: '#fff',
            text: '#000'
          },
          others: {
            bg: '#43A047',
            text: '#fff'
          },
          messagesDisplay: {
            bg: '#f7f3f3'
          }
        },
        submitIcon: '#558B2F'
      },
      borderStyle: {
        topLeft: "10px",
        topRight: "10px",
        bottomLeft: "10px",
        bottomRight: "10px",
      },
      hideCloseButton: true,
      submitIconSize: "35px",
      closeButtonIconSize: "20px",
      asyncMode: true
    }
  },
  methods: {
    onType: function(){},
    onMessageSubmit: async function(message){
      message.content = message.content.replace(/\n/g, "")

      if (message.content == "UUDDLRLRBA"){
        this.messages.push(message)
        const axios = require('axios')
        await axios.get('http://13.125.199.238:5000/Declaration')
        .then( res => {
          let datas = res.data.datas
          let N = datas.length
          for (var i = 0; i < N; i++){
            let answer = {
              content: "Q: " + (datas[i][1]) + "\nA: " + (datas[i][2]),
              myself: false,
              participantId: 1,
              timestamp: { year: 0, month: 0, day: 0, hour: 0, minute: 0, second: 0, millisecond: 0 },
              uploaded: true
            }
            this.messages.push(answer)
          }
        }).catch(e => {
          console.log(e)
          this.$swal('문제가 생겼어요!', '다음에 다시 대화해요!', 'error')
        })
        message.uploaded = true

      }else {
        const axios = require('axios')

        let form = new FormData()
        form.append('question', message["content"])

        this.messages.push(message)

        await axios.post('http://13.125.199.238:5000/chat', form)
          .then( res => {
            let answer = {
              content: res["data"]["answer"],
              myself: false,
              participantId: 1,
              timestamp: { year: 0, month: 0, day: 0, hour: 0, minute: 0, second: 0, millisecond: 0 },
              uploaded: true
            }
            this.messages.push(answer)
            message.uploaded = true
          }).catch( err => {
            console.log(err)
            this.$swal('문제가 생겼어요!', '다음에 다시 대화해요!', 'error')
            message.uploaded = true
          })
      }
    },
    createData: async function() {
      if (this.question.length == 0) {
        this.$swal('질문을 입력해주세요!', '어떻게 질문하면 이렇게 대답해야 할까요?', 'error')
        return false
      } else if (this.answer.length == 0) {
        this.$swal('답변을 입력해주세요!', '이 질문엔 어떻게 대답해야 좋을까요?', 'error')
        return false
      } else {
        let form = new FormData()
        form.append('question', this.question)
        form.append('answer', this.answer)

        const axios = require('axios')
        await axios.post('http://13.125.199.238:5000/Declaration', form)
        .then( res => {
          if (res["data"]["flag"]) {
            this.$swal('Think B를 가르쳤어요!', '다음에는 이렇게 대답할게요!', 'success')
          }
          else {
            this.$swal('문제가 생겼어요!', '다음에 다시 알려주세요!', 'error')
          }
        }).catch( err => {
          console.log(err)
          this.$swal('문제가 생겼어요!', '다음에 다시 알려주세요!', 'error')
        })
      }
      this.dialog = false
      this.question = ""
      this.answer = ""
    },
    cancelData: function() {
      this.dialog = false
      this.question = ""
      this.answer = ""
    }
  }
}
</script>

<style>
  #thinkB_chat {
    height: 500px;
  }

  .ChatBody {
    height: 100vh;

    background: lightblue;
    background-image: url('../assets/poodle.png');
    background-repeat: no-repeat;
    background-position: 91% 90%;
    background-size: 250px;
  }
</style>