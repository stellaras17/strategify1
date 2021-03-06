import Vue from 'vue'
import { uid } from 'quasar'
import { firebaseDb, firebaseAuth } from 'src/boot/firebase'

const state = {
    strats: {},
    coins: 0,
}


const mutations = {
    updateStrat(state, payload){
      Object.assign(state.strats[payload.id], payload.updates)
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
    },
    initiateCoins(state, value){
      state.coins=value;
    }
}

const actions = {
    updateStrat({ dispatch }, payload) {
      dispatch('dbUpdateStrat', payload)
    },
    updateBuyCons({ dispatch }, payload) {
      dispatch('dbUpdateBuyCons', payload)
    },
    updateSellCons({ dispatch }, payload) {
      dispatch('dbUpdateSellCons', payload)
    },
    deleteStrat({ dispatch }, id) {
      dispatch('dbDeleteStrat', id)
    },
    addStrat({ dispatch }, payload) {
      let stratId = uid()
      let newStrat = {
        id: stratId,
        strat: payload.strat
      }
      dispatch('dbAddStrat', newStrat)
    },
    dbReadData({commit}) {
      let user = firebaseAuth.currentUser.uid
      let userStrats = firebaseDb.ref('strats/' + user)
      
      userStrats.on('child_added', snapshot => {
        let strat = snapshot.val()
        let payload = {
          id: snapshot.key,
          strat: strat
        }
        commit('addStrat', payload)
      })

      userStrats.on('child_changed', snapshot => {
        let strat = snapshot.val()
        let payload = {
          id: snapshot.key,
          updates: strat
        }
        commit('updateStrat', payload)
      })

      userStrats.on('child_removed', snapshot => {
        commit('deleteStrat', snapshot.key)
      })
    },
    dbAddStrat({}, payload) {
      let user = firebaseAuth.currentUser.uid
      let stratRef = firebaseDb.ref('strats/'+ user + '/' + payload.id)
      stratRef.set(payload.strat)
    },
    dbUpdateStrat({}, payload) {
      let user = firebaseAuth.currentUser.uid
      let stratRef = firebaseDb.ref('strats/'+ user + '/' + payload.id)
      stratRef.update(payload.updates)
    },
    dbUpdateBuyCons({}, payload) {
      let user = firebaseAuth.currentUser.uid
      let stratRef = firebaseDb.ref('strats/'+ user + '/' + payload.id + '/buyConditions')
      stratRef.update(payload.updates)
    },
    dbUpdateSellCons({}, payload) {
      let user = firebaseAuth.currentUser.uid
      let stratRef = firebaseDb.ref('strats/'+ user + '/' + payload.id + '/sellConditions')
      stratRef.update(payload.updates)
    },
    dbDeleteStrat({}, stratId) {
      let user = firebaseAuth.currentUser.uid
      let stratRef = firebaseDb.ref('strats/'+ user + '/' + stratId)
      stratRef.remove()
    },
    initiateCoins({commit}) {
      let user = firebaseAuth.currentUser.uid
      let coinsRef = firebaseDb.ref('coins/'+ user )
      coinsRef.on('value', (snapshot) => {
        const data = snapshot.val();
        commit('initiateCoins', data)
      });
    },
    initiateCoinsNewUser({dispatch}) {
      let user = firebaseAuth.currentUser
       try {
        if(user==null){
          setTimeout(dispatch,1000,'initiateCoinsNewUser')
        } else { 
          let userID = firebaseAuth.currentUser.uid
          let coinsRef = firebaseDb.ref('coins/'+ userID )
          let cryptoRef = firebaseDb.ref('crypto/'+ userID )
          coinsRef.set(1000)
          cryptoRef.set({
            'BTC':0.5,
            'ETH':1,
            'BNB':1,
            'ZIL': 1000
          })
         }
      }
      catch(err) {
        alert(err.message)
      } 
    }
}

const getters = {
    stratsInactive: (state) => {
      let strats = {}
      Object.keys(state.strats).forEach(function(key) {
        let strat = state.strats[key]
        if (!strat.active) {
          strats[key] = strat
        }
      })
      return strats
    },
    stratsActive: (state) => {
      let strats = {}
      Object.keys(state.strats).forEach(function(key) {
        let strat = state.strats[key]
        if (strat.active) {
          strats[key] = strat
        }
      })
      return strats
    },
    coins: (state) => {
      return state.coins
    }
} 

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}