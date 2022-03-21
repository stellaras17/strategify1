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
    dbReadData({commit}) {
      let userStrats = firebaseDb.ref('hub/')
      
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
      let usernameRef = firebaseDb.ref('users/' + user + '/username')
      var username = ''
      var hub
      usernameRef.on('value', function(snapshot) {
          username = snapshot.val()
      });
      let hubRef = firebaseDb.ref('hub')
      hubRef.on('value', function(snapshot) {
          hub = snapshot.val()
      });
      var hubKeys = []
      Object.keys(hub).forEach(element => {
        hubKeys.push(element)
      });
      let postRef =  firebaseDb.ref('hub/' + payload.id )
      if(!hubKeys.includes(payload.id)){
        let post = {
          user: user,
          username: username,
          strat: payload.strat,
          likes: 0
        }
        postRef.set(post)
      }
      else {
        alert('Strategy already on the hub!')
      }
    },
    
}

const getters = {
  strats: state => {
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