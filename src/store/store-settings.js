import { LocalStorage } from "quasar";

const state = {
    settings: {
        tickerForChart: 'BTCUSDT'
    }
}


const mutations = {
    setTickerForChart(state, value){
        state.settings.tickerForChart=value;
    },
    getSettings(state,value){
        Object.assign(state.settings, value);
    }

}

const actions = {
    setTickerForChart({commit, dispatch},value){
        commit('setTickerForChart', value)
        dispatch('saveSettings')
    },
    saveSettings({state}){
        LocalStorage.set('settings', state.settings)
    },
    getSettings({commit}) {
        let settings = LocalStorage.getItem('settings')
        if(settings) {
            commit('getSettings', settings)
        }
    }
}

const getters = {
    settings: state => {
        return state.settings
    }
} 

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}