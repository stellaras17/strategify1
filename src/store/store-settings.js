import { LocalStorage } from "quasar";

const state = {
    settings: {
        showChart:true,
        tickerForChart: 'BTCUSDT'
    }
}


const mutations = {
    getSettings(state,value){
        Object.assign(state.settings, value);
    },
    setTickerForChart(state, value){
        state.settings.tickerForChart=value;
    },
    setShowChart(state,value){
        state.settings.showChart=value;
    }

}

const actions = {
    setShowChart({commit, dispatch},value){
        commit('setShowChart', value)
        dispatch('saveSettings')
    },
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