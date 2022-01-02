import { LocalStorage, uid } from "quasar";
import Vue from 'vue'

const state = {
    orders: {
        ID1: {
            type:"BUY",
            strat: "BTC RSI",
            amount:100,
            ticker: "BTCUSDT",
            time: 1641147007704,
        },
        ID2: {
            type:"SELL",
            strat: "ETH RSI",
            amount:100,
            ticker: "ETHUSDT",
            time: 1641147070116,
        },
        ID3: {
            type:"BUY",
            strat: "BTC RSI",
            amount:100,
            ticker: "BTCUSDT",
            time: 1641147007704,
        },
        ID4: {
            type:"SELL",
            strat: "ETH RSI",
            amount:100,
            ticker: "ETHUSDT",
            time: 1641147070116,
        },
    }
}


const mutations = {
    addOrder(state, payload) {
        Vue.set(state.orders, payload.id, payload.order)
      },
}

const actions = {
    addOrder({ dispatch, commit }, payload) {
        let orderId = uid()
        let newOrder = {
            id: orderId,
            order: payload
        }
        console.log(newOrder);
        commit('addOrder', newOrder)
        //dispatch('dbAddStrat', newStrat)
      },
}

const getters = {
    orders: (state) => {
        return state.orders
    } 
} 

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}