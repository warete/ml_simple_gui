import VueRouter from "vue-router";

import MainSteps from "./components/MainSteps";

const routes = [
    {path: '/', component: MainSteps}
];

export default new VueRouter({mode: 'history', routes});
