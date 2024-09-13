import { getDetail, createDetail, updateDetail, deleteDetail } from "@/api";

const state = {
    id: '',
    detailData: {},
    editMode: false,
    createMode: false,
    newData: {},
    errorMessage: '',
}

const mutations = {
    setState(state, payload) {
        state[payload.fieldname] = payload.value;
    },
};

const actions = {
    setEditMode({ commit }, value) {
        commit('setState', {fieldname: 'editMode', value})
    },
    setCreateMode({ commit }, value) {
        commit('setState', {fieldname: 'createMode', value})
    },
    setId({ commit }, value) {
        commit('setState', {fieldname: 'id', value})
    },
    setError({ commit }, value) {
        commit('setState', {fieldname: 'errorMessage', value})
    },
    updateNewValue({ commit }, payload) {
        commit('setState', {fieldname: 'newData', value: {...state.newData, ...payload}})
    },
    clearData({ commit }, payload){
        commit('setState', {fieldname: payload, value: {}})
    },
    clearError({ commit }) {
        commit('setState', {fieldname: 'errorMessage', value: ''})
    },
    async setData({ state, commit }){
        if(state.id) {
            return await getDetail(state.id)
            .then(response => {
                const data = response.data
                commit('setState', {fieldname: 'detailData', value: data})
            })
            .catch(error => {
                console.log('Failed to fetch detail', error)
            })
        } else {
            commit('setState', {fieldname: 'detailData', value: {}})
        }
    },
    async submitData({ state, commit, dispatch }) {
        if(state.createMode) {
            // for create
            return await createDetail(state.newData)
            .then(() => {
                dispatch('mainListing/loadData', null, { root: true })
            })
            .catch(error => {
                let errorMessage = error?.response?.data?.error || "Something error"
                dispatch('setError', errorMessage)
            })
            .finally(() => {
                commit('setState', {fieldname: 'createMode', value: false})
                dispatch('clearData', 'detailData')
                dispatch('clearData', 'newData')
            })
        } else {
            // for update
            return await updateDetail(state.id, state.newData)
            .then(() => {
                dispatch('mainListing/loadData', null, { root: true })
            })
            .catch(error => {
                let errorMessage = error?.response?.data?.error || "Something error"
                dispatch('setError', errorMessage)
            })
            .finally(() => {
                commit('setState', {fieldname: 'editMode', value: false})
                dispatch('clearData', 'detailData')
                dispatch('clearData', 'newData')
            })
        }
    },
    async deleteData({ dispatch }, id) {
        return await deleteDetail(id)
            .then(() => {
                dispatch('mainListing/loadData', null, { root: true })
            })
            .catch(error => {
                console.log('Failed to fetch detail', error)
            })
    }
};

export default {
    namespaced: true,
    state, mutations, actions
}