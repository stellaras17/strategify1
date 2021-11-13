import Vue from 'vue'
import { uid } from 'quasar'

const state = {
    strats: {
        'ID1': {
          name:'BTC RSI',
          active: false,
          ticker: 'BTCUSDT',
          amount: 100,
          timeframe: '5m',
          buyConditions: {
            indicator: 'RSI',
            targetValue: 20,
            conditionMet: false
          },
          sellConditions: {
            indicator: 'RSI',
            targetValue: 80,
            conditionMet: false
          }
        },
        'ID2': {
          name:'ETH RSI',
          active: false,
          ticker: 'ETHUSDT',
          amount: 100,
          timeframe: '5m',
          buyConditions: {
            indicator: 'RSI',
            targetValue: 20,
            conditionMet: false
          },
          sellConditions: {
            indicator: 'RSI',
            targetValue: 80,
            conditionMet: false
          }
        },
        'ID3': {
          name:'ZIL RSI',
          active: false,
          ticker: 'ZILUSDT',
          amount: 100,
          timeframe: '5m',
          buyConditions: {
            indicator: 'RSI',
            targetValue: 20,
            conditionMet: false
          },
          sellConditions: {
            indicator: 'SMA',
            targetValue: 60,
            conditionMet: false
          }
        },
    
    }
    
}


const mutations = {
    updateStrat(state, payload){
        Object.assign(state.strats[payload.id], payload.updates)
        //console.log(state.strats[payload.id]);
    },
    updateBuyCons(state, payload){
        Object.assign(state.strats[payload.id].buyConditions, payload.updates)       
    },
    updateSellCons(state, payload){
        Object.assign(state.strats[payload.id].sellConditions, payload.updates)
    },
    deleteStrat(state, id){
      Vue.delete(state.strats, id)
    },
    addStrat(state, payload) {
      Vue.set(state.strats, payload.id, payload.strat)
    }
}

const actions = {
    updateStrat({ commit }, payload) {
      commit('updateStrat', payload)
    },
    updateBuyCons({ commit }, payload) {
      commit('updateBuyCons', payload)
    },
    updateSellCons({ commit }, payload) {
      commit('updateSellCons', payload)
    },
    deleteStrat({ commit }, id) {
      commit('deleteStrat', id)
    },
    addStrat({ commit }, payload) {
      let stratId = uid()
      let newStrat = {
        id: stratId,
        strat: payload.strat
      }
      commit('addStrat', newStrat)
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