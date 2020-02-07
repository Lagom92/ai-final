<template>
  <v-app>
    <v-content class="view">
      <!-- 라우터 -->
      <v-flex fill-height aacontainer class="IntroBody">
        <router-view></router-view>
        <div id="btndiv">
          <button class="downbtn">Think B랑 대화하러 가기</button>
        </div>
        <a class="downa"><span></span></a>
      </v-flex>
      <v-flex class="Chatbot">
        <Chatbot></Chatbot>
      </v-flex>
      <!-- 라우터 -->
    </v-content>
  </v-app>
</template>

<script>
import Chatbot from "./components/Chatbot";
import $ from "jquery";

export default {
  name: 'App',
  components: {
    Chatbot
  },
  data() {
    return {
    }
  }
}

$(document).ready(function() {
  $('.IntroBody').on('mousewheel', function(e){
    if( e.originalEvent.wheelDeltaY < 0 ){
      $('.IntroBody, .Chatbot').addClass('scrolled');
      return false;
    }
  })
})

$(document).ready(function() {
  $('.Chatbot').on('mousewheel', function(e){
    if ( 
      e.target.classList[0] != undefined &&
      e.target.classList[0] != 'contaier-message-display' && 
      e.target.classList[0] != 'message-container' && 
      e.target.classList[0] != 'message-timestamp' &&
      e.target.classList[0] != 'message-username' &&
      e.target.classList[0] != 'message-loading' &&
      e.target.classList[0] != 'message-text' &&
      e.target.classList[0] != 'icon-sent'
      ) {
      if( e.originalEvent.wheelDeltaY > 0 ){
        $('.IntroBody, .Chatbot').removeClass('scrolled');
      }
    }
  })
})

$(document).ready(function() {
  $('.downbtn, .downa').click(function() {
    $('.IntroBody, .Chatbot').addClass('scrolled');
  })
})

</script>

<style>
.view {
  height: 100vh;
}

.IntroBody {
    height: 100vh;
    width: 100%;
    overflow: hidden;
    position: fixed;
    top: 0;
    z-index: 9;

    background-color:#ffe55f !important;
    background-image: url('./assets/pupper.gif');
    background-repeat: no-repeat;
    background-position: 91% 93%;
    background-size: 300px;

    animation-name: poodle;
    animation-duration: 4s;
    animation-duration: leaner;
    animation-direction: alternate;
    animation-fill-mode: forwards;

	  transition: all 1.6s cubic-bezier(0.86, 0, 0.07, 1);
    transform: translate3d(0, 0, 0) scale(1);
}

@-webkit-keyframes poodle {
    0%   {background-position: 3% 93%;}
    100% {background-position: 91% 93%;}
}

.IntroBody.scrolled {
	transform: translate3d(0, -100%, 0) scale(.75);
	opacity: 0;
}

.Chatbot{
  position: relative;
	transition: all 1.6s cubic-bezier(0.86, 0, 0.07, 1);
	transform: translate3d(0, 0, 0) scale(.75);
	opacity: 0;
}
.Chatbot.scrolled{
	transform: translate3d(0, 0, 0) scale(1);	
	opacity: 1;
}

#btndiv {
  text-align: center;
}

.downbtn {
  background: #ffe55f;
  color: #fff !important;
  border: none;
  position: relative;
  height: 50px;
  font-size: 1.4em !important;
  font-weight: bold !important;
  padding: 0 2em;
  cursor: pointer;
  transition: 800ms ease all;
  outline: none;
}
.downbtn:hover{
  background: #ffe55f;
  color: rgba(0, 0, 0, 0.5) !important;
}
.downbtn:before,.downbtn:after{
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  height: 3px;
  width: 0;
  background: rgba(0, 0, 0, 0.5);
  transition: 400ms ease all;
}
.downbtn:after{
  right: inherit;
  top: inherit;
  left: 0;
  bottom: 0;
}
.downbtn:hover:before,.downbtn:hover:after{
  width: 100%;
  transition: 800ms ease all;
}

.downa {
  padding-top: 70px;
}
.downa span {
  position: absolute;
  top: 55vh;
  left: 50%;
  width: 24px;
  height: 24px;
  margin-left: -12px;
  border-left: 5px solid #fff;
  border-bottom: 5px solid #fff;
  -webkit-transform: rotate(-45deg);
  transform: rotate(-45deg);
  -webkit-animation: sdb 1.5s infinite;
  animation: sdb 1.5s infinite;
  box-sizing: border-box;
}
@-webkit-keyframes sdb {
  0% {
    -webkit-transform: rotate(-45deg) translate(0, 0);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    -webkit-transform: rotate(-45deg) translate(-20px, 20px);
    opacity: 0;
  }
}
@keyframes sdb {
  0% {
    transform: rotate(-45deg) translate(0, 0);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: rotate(-45deg) translate(-20px, 20px);
    opacity: 0;
  }
}
</style>