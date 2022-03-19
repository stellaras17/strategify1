<template>
  <q-layout view="hHh lpR fff">
    <q-header elevated>
      <q-toolbar>

        <q-chip>
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
          {{username}}
        </q-chip>

        <q-toolbar-title class="text-secondary absolute-center">
          Strategify
        </q-toolbar-title>

        <div class="row absolute-right">
        <q-btn
          v-if="loggedIn"
          color="secondary"
          icon-right="account_circle"
          label="LOG OUT" 
          
          flat
          @click="logOutUser"
          />

          

        </div>
      
      </q-toolbar>
      
    </q-header>
    

    <q-drawer
      v-if="loggedIn"
      :width="250"
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item-label
          header
          class="text-primary"
        >
          Navigation
        </q-item-label>
        <q-item
          to="/"
          clickable
          exact
          active-class="text-secondary"
        >
          <q-item-section
            avatar
          >
            <q-icon name = "analytics" />
          </q-item-section>

          <q-item-section>
            <q-item-label>My Strategies</q-item-label>
          </q-item-section>
        </q-item>

        <q-item
          to="/currencies"
          clickable
          exact
          active-class="text-secondary"
        >
          <q-item-section
            avatar
          >
            <q-icon name = "monetization_on" />
          </q-item-section>

          <q-item-section>
            <q-item-label>Crypto Wallet</q-item-label>
          </q-item-section>
        </q-item>

        <q-item
          to="/orders"
          clickable
          exact
          active-class="text-secondary"
        >
          <q-item-section
            avatar
          >
            <q-icon name = "book" />
          </q-item-section>

          <q-item-section>
            <q-item-label>Orders</q-item-label>
          </q-item-section>
        </q-item>

        <q-item
          to="/settings"
          clickable
          exact
          active-class="text-secondary"
        >
          <q-item-section
            avatar
          >
            <q-icon name = "settings" />
          </q-item-section>

          <q-item-section>
            <q-item-label>Settings</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    
    

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { LocalStorage } from 'quasar'
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
  data () {
    return {
      leftDrawerOpen: false,
      userEmail: ''
    }
  },
  computed: {
    ...mapState('auth', ['loggedIn']),
    ...mapState('users', ['username']),

  },
  methods: {
    ...mapActions('auth', ['logOutUser']),
    /* setUserEmail() {
      let email = LocalStorage.getItem('userEmail')
      this.userEmail = email
    } */
  },
  mounted() {
    /* if(this.loggedIn){
      this.setUserEmail()
    } */
  }
}
</script>

