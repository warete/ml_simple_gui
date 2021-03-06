import Vue from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router';
import VueAxios from 'vue-axios';
import axios from 'axios';

import store from './store';
import router from "./router";

Vue.use(VueRouter);

Vue.use(VueAxios, axios);

Vue.config.productionTip = false;

new Vue({
    vuetify,
    store,
    router,
    render: h => h(App)
}).$mount('#app');
