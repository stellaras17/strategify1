import { firebaseAuth } from 'boot/firebase.js'
import { LocalStorage } from 'quasar'

const state = {
    loggedIn: false,
    userem: ''
}


const mutations = {
    changeLoggedIn(state, value){
        state.loggedIn = value
    },
    setUserEmail(state, value){
        state.userem = value
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
    loginUser({commit}, payload) {
        firebaseAuth.signInWithEmailAndPassword(payload.email, payload.password)
        .then(response => {
            console.log(response);
        })
        .then(
           commit('setUserEmail', payload.email)
        )
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
                commit('setUserEmail', user.email)
                LocalStorage.set('loggedIn', true)
                this.$router.push('/').catch(err => {})
                dispatch('users/dbReadData', null, { root: true }).then(console.log('dispatched'))
                dispatch('strats/dbReadData', null, { root: true })
                dispatch('orders/dbReadData', null, { root: true })
                dispatch('currencies/dbReadData', null, { root: true })
                dispatch('hub/dbReadData', null, { root: true })
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
    getUser: state => {
        let user = state.userEmail
        return user;
    }
} 

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}