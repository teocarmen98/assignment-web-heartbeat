import Vue from 'vue';
import Vuex from 'vuex';

import mainListing from "./mainListing";
import detail from "./detail";

Vue.use(Vuex);

const store = new Vuex.Store({
    modules: {
        mainListing,
        detail,
    },
});

export default store;