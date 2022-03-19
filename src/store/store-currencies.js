import Vue from 'vue'
import { uid } from 'quasar'
import { firebaseDb, firebaseAuth } from 'src/boot/firebase'

const state = {
    currencies: {
        /* ID1: {
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
        }, */
    }
}


const mutations = {
    addCurrency(state, payload) {
        Vue.set(state.currencies, payload.id, payload.currency)
      },
    updateCurrency(state, payload){
        Object.assign(state.currencies[payload.id], payload.updates)
      },
}

const actions = {
    addCurrency({ dispatch, commit }, payload) {
        let orderId = uid()
        let newCurrency = {
            id: orderId,
            order: payload
        }
        console.log(newCurrency);
        commit('addCurrency', newCurrency)
        //dispatch('dbAddStrat', newStrat)
      },
      dbReadData({commit}) {
        let user = firebaseAuth.currentUser.uid
        let userCurrencies = firebaseDb.ref('crypto/' + user)
        
        
        userCurrencies.on('child_added', snapshot => {
          let currency = snapshot.val()
          let payload = {
            id: snapshot.key,
            currency: currency
          }
          commit('addCurrency', payload)
        })

        userCurrencies.on('child_changed', snapshot => {
            let currency = snapshot.val()
            let payload = {
              id: snapshot.key,
              updates: currency
            }
            commit('updateCurrency', payload)
          })
  
      },
}

const getters = {
    currencies: (state) => {
        return state.currencies
    } 
} 

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}