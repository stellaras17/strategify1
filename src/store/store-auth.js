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
    registerUser({}, payload) {
        firebaseAuth.createUserWithEmailAndPassword(payload.email, payload.password)
        .then(response => {
            console.log(response);
        })
        .catch(error => {
            alert(error);
        })
    },
    loginUser({}, payload) {
        firebaseAuth.signInWithEmailAndPassword(payload.email, payload.password)
        .then(response => {
            console.log(response);
        })
        .catch(error => {
            alert(error);
        })
    },
    logOutUser(){
        firebaseAuth.signOut()
    },
    handleAuthStateChange({commit}) {
        firebaseAuth.onAuthStateChanged(user => {
            if(user) {
                commit('changeLoggedIn', true)
                LocalStorage.set('loggedIn', true)
                this.$router.push('/').catch(err => {})
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