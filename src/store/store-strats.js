const state = {
    strats: {
        'ID1': {
          name:'BTC RSI',
          active: false,
          ticker: 'BTCUSDT',
          amount: 100,
          timeframe: '5m',
          buyConditions: {'ID111':{
            indicator: 'RSI',
            aob: 'below',
            targetValue: 20,
            conditionMet: false
          }},
          sellConditions: {'ID121':{
            indicator: 'RSI',
            aob: 'above',
            targetValue: 80,
            conditionMet: false
          } }
        },
        'ID2': {
          name:'ETH RSI',
          active: false,
          ticker: 'ETHUSDT',
          amount: 100,
          timeframe: '5m',
          buyConditions: {'ID211':{
            indicator: 'RSI',
            aob: 'below',
            targetValue: 20,
            conditionMet: false
          }},
          sellConditions: {'ID221':{
            indicator: 'RSI',
            aob: 'above',
            targetValue: 80,
            conditionMet: false
          }}
        },
        'ID3': {
          name:'ZIL RSI',
          active: false,
          ticker: 'ZILUSDT',
          amount: 100,
          timeframe: '5m',
          buyConditions: {'ID311':{
            indicator: 'RSI',
            aob: 'below',
            targetValue: 20,
            conditionMet: false
          }},
          sellConditions: {'ID321':{
            indicator: 'RSI',
            aob: 'above',
            targetValue: 80,
            conditionMet: false
          }}
        },
    
    }
    
}


const mutations = {
    updateStrat(state, payload){
        Object.assign(state.strats[payload.id], payload.updates)
    }
}

const actions = {
    updateStrat({ commit }, payload) {
        commit('updateStrat', payload)
    }
}

const getters = {
    strats: (state) => {
        return state.strats
    }
} 

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}