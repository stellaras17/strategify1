<template>
      <q-chip v-if="username" clickable @click="prompt">
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
          {{username}}
        </q-chip>
      <q-chip v-else>
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
          Loading...
        </q-chip>

</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
import { firebaseAuth, firebaseDb } from 'boot/firebase.js'

export default {
  data() {
    return {
      username: '',
    }
  },
/*   computed: {
    ...mapGetters('users', ['username']),
  }, */
  methods: {
    ...mapActions('strats', ['addStrat']),
    async prompt() {
        await this.getUsername
        this.$q.dialog({
        title: 'User',
        message: 'Username:',
        prompt: {
            model: this.username,
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
      allUsernamesRef.on('value', snapshot => {
          allUsernames = snapshot.val()
      });
      usernameRef.on('value', snapshot => {
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
      allUsernamesRef.on('value', snapshot => {
          allUsernames = snapshot.val()
      });
      if(Object.keys(allUsernames).includes(username)){
        return false
      }
      else {
        return true
      }
    },
    async getUsername() {
        let user = firebaseAuth.currentUser.uid
        let userProf = firebaseDb.ref('users/' + user +'/username')

        userProf.on('value', snapshot => {
            let update = snapshot.val()
            this.username=update
          })

        userProf.on('child_added', snapshot => {
            let update = snapshot.val()
            this.username=update
          })
  
        userProf.on('child_changed', snapshot => {
          let update = snapshot.val()
          this.username=update
        })
    },
    
  },
  
  async mounted() {
    await this.getUsername() 
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