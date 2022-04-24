import { firebaseAuth, firebaseDb } from 'boot/firebase.js'

const state = {
    username: '',
    profURL: null
}


const mutations = {
    updateUsername(state, value){
        state.username = value
    
    },
    updateProfURL(state, value){
        state.profURL = value
    }
}

const actions = {
    dbReadData({commit}) {
        let user = firebaseAuth.currentUser.uid
        let userProf = firebaseDb.ref('users/' + user +'/username')

        userProf.on('value', snapshot => {
            let update = snapshot.val()
            
            commit('updateUsername', update)
          })

        userProf.on('child_added', snapshot => {
            let update = snapshot.val()
            
            commit('updateUsername', update)
          })
  
        userProf.on('child_changed', snapshot => {
          let update = snapshot.val()
          commit('updateUsername', update)
        })
    },
}

const getters = {
    username: state => {
        return state.usermame
    },
    profURL: state => {
        return state.profURL
    },
} 

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}