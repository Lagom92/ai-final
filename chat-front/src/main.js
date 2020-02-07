import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueSweetalert2 from 'vue-sweetalert2';

Vue.use(VueSweetalert2);

import 'expose-loader?$!expose-loader?jQuery!jquery'

import router from './router';

Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
