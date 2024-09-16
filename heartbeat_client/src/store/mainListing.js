import { getMainListing } from "@/api";

const state = {
    tableData: [],
    currentPage: 1,
    limit: 10,
    totalPage: 1,
}

const mutations = {
    setState(state, payload) {
        state[payload.fieldname] = payload.value;
    },
}

const actions = {
    setTotalPage({ commit }, payload) {
        commit('setState', {fieldname: 'totalPage', value: Math.ceil(payload.sum / payload.limit) })
    },
    setPage({ commit, dispatch }, payload) {
        commit('setState', {fieldname:'currentPage', value: payload.currentPage})
        dispatch('loadData')
    },
    setPageSize({ commit, dispatch }, payload){
        commit('setState', {fieldname:'currentPage', value: 1})
        commit('setState', {fieldname:'limit', value: payload.limit})
        dispatch('loadData')
    },
    async loadData({ state, commit, dispatch }) {
        const filter = {
            'page': state.currentPage,
            'limit': state.limit
        }
        return await getMainListing(filter)
        .then(response => {
            let data = response.data.data
            commit('setState', {fieldname: 'tableData', value: data })
            commit('setState', {fieldname: 'totalSize', value: response.data.total })
            dispatch('setTotalPage', { sum: response.data.total, limit: state.limit})
        })
        .catch(error => {
            console.log('Failed to fetch data', error)
        })
    },
};

export default {
    namespaced: true,
    state, mutations, actions,
}