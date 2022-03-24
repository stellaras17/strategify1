<template>
  <!-- <q-card class="newStratCard bg-info">
    <form @submit.prevent="submitForm">
        <q-card-section class="row">
          <div class="text-h6">User details</div>
          <q-space/>
          <q-btn
            v-close-popup
            dense
            flat
            round
            color="primary"
            icon="close" />
        </q-card-section>

      <div class="col ">

        <q-card-section class="q-pt-none">
          <q-input
            autofocus
            class="bg-white"
            outlined
            v-model="usernameToSubmit"
            label="Username: "
            :rules="[val => !!val || 'Username cannot be empty']"
            ref="username"
            hint="*" />
        </q-card-section> 

      </div>
        <q-card-actions align="right">
          <q-btn class="q-ma-xs buttonstyle" type="submit" label="SAVE" color="primary"  />
        </q-card-actions>
      </form>
      </q-card> -->
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
      usernameToSubmit: null,
      
    }
  },
  methods: {
    ...mapActions('strats', ['addStrat']),
    ...mapActions('users', ['getUsername',]),
    submitStrat() {
      this.setUsername()
      
    },
    prompt () {
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
  mounted() {
    this.usernameToSubmit = this.username
    this.setUsername()
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