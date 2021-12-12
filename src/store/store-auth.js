import { firebaseAuth } from 'boot/firebase.js'
import { LocalStorage } from 'quasar'

const state = {
    loggedIn: false
}


const mutations = {
    changeLoggedIn(state, value){
        state.loggedIn = value
    }
}

const actions = {
    registerUser({dispatch}, payload) {
        firebaseAuth.createUserWithEmailAndPassword(payload.email, payload.password)
        .then(response => {
            console.log(response);
        })
        .then(
            dispatch('strats/initiateCoinsNewUser', null, { root: true })
        )
        .catch(error => {
            alert(error.message);
        })
    },
    loginUser({}, payload) {
        firebaseAuth.signInWithEmailAndPassword(payload.email, payload.password)
        .then(response => {
            console.log(response);
        })
        .catch(error => {
            alert(error.message);
        })
    },
    logOutUser(){
        firebaseAuth.signOut()
        location.reload();
    },
    handleAuthStateChange({commit, dispatch}) {
        firebaseAuth.onAuthStateChanged(user => {
            if(user) {
                commit('changeLoggedIn', true)
                LocalStorage.set('loggedIn', true)
                this.$router.push('/').catch(err => {})
                dispatch('strats/dbReadData', null, { root: true })
                dispatch('strats/initiateCoins', null, { root: true })
            }
            else {
                commit('changeLoggedIn', false)
                LocalStorage.set('loggedIn', false)
                this.$router.replace('/auth').catch(err => {})
            }
        })
    }
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