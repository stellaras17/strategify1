import Vue from 'vue'
import { uid } from 'quasar'
import { firebaseDb, firebaseAuth } from 'src/boot/firebase'

const state = {
    strats: {},
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
      let userStrats = firebaseDb.ref('hub/')
      
      userStrats.on('child_added', snapshot => {
        let strat = snapshot.val()
        let payload = {
          id: snapshot.key,
          strat: strat
        }
        console.log(payload);
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
      let hubRef = firebaseDb.ref('hub/' + payload.id)
      let post = {
        user: user,
        strat: payload.strat,
        likes: 0
      }
      hubRef.set(post)
    },
    
}

const getters = {

} 

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}