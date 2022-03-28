<template>
      <q-chip clickable @click="prompt">
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
          {{username}}
        </q-chip>

</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import { firebaseAuth, firebaseDb } from 'boot/firebase.js'

export default {
  data() {
    return {
      usernameToSubmit: '',
    }
  },
  methods: {
    ...mapActions('strats', ['addStrat']),
    submitStrat() {
      this.setUsername()
    },
    prompt() {
        this.$q.dialog({
        title: 'User',
        message: 'Username:',
        prompt: {
            model: this.usernameToSubmit,
            isValid: val => this.checkAvailability(val) && val != '' && val!= null && val!=undefined,
            type: 'text' // optional
        },
        cancel: true,
        persistent: true
        }).onOk(data => {
          //console.log('>>>> OK, received', data, data)
          this.setUsername(data)
        })
    },
    setUsername(data) {
      let user = firebaseAuth.currentUser.uid
      let usernameRef = firebaseDb.ref('users/' + user + '/username')
      let allUsernamesRef = firebaseDb.ref('usernames')
      var allUsernames
      var currentUsername
      allUsernamesRef.on('value', function(snapshot) {
          allUsernames = snapshot.val()
      });
      usernameRef.on('value', function(snapshot) {
          currentUsername = snapshot.val()
      });
      if(!this.checkAvailability(data)){
        alert('this username is already in use')
      }
      else {
        let usernameRefAll = firebaseDb.ref('usernames/' + currentUsername)
        usernameRefAll.remove()
        usernameRefAll = firebaseDb.ref('usernames/' + data)
        usernameRefAll.set(user)
        usernameRef.set(data)
        this.$emit('close')
      }
    },
    checkAvailability(username) {
      let allUsernamesRef = firebaseDb.ref('usernames')
      var allUsernames
      allUsernamesRef.on('value', function(snapshot) {
          allUsernames = snapshot.val()
      });
      if(Object.keys(allUsernames).includes(username)){
        return false
      }
      else {
        return true
      }
    }
    
  },
  computed: {
    ...mapState('users', ['username']),
  },
  created() {
    this.usernameToSubmit = this.username 
  }
}
</script>

<style lang="scss" scoped>
 .newStratCard {
  width: 650px;
 }
 .selectWidth {
  width: 150px;
 }
 .buttonstyle{
   width: 100px;
   height: 45px;
 }
</style>