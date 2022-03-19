import { firebaseAuth, firebaseDb } from 'boot/firebase.js'
import { LocalStorage } from 'quasar'

const state = {
    username: '',
    profURL: ''
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
        let userProf = firebaseDb.ref('users/' + user)

        userProf.on('child_added', snapshot => {
            let update = snapshot.val()
            let payload = {
              id: snapshot.key,
              update: update
            }
            if(payload.id == 'profURL'){
                commit('updateProfURL', payload.update)
            }
            if(payload.id == 'username'){
                commit('updateUsername', payload.update)
            }

          })
  
        userProf.on('child_changed', snapshot => {
          let user = snapshot.val()
          let payload = {
            id: snapshot.key,
            updates: user
          }
          if(payload.id == 'profURL'){
            commit('updateProfURL', payload.update)
            }
          if(payload.id == 'username'){
                commit('updateUsername', payload.update)
            }

        })
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