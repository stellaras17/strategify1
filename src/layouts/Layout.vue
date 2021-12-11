<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated>
      <q-toolbar>

        <q-toolbar-title class="text-secondary absolute-center">
          Strategify
        </q-toolbar-title>

        <q-btn
          v-if="loggedIn"
          color="secondary"
          icon-right="account_circle"
          label="LOG OUT" 
          class="absolute-right"
          flat
          @click="logOutUser"
          />

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
import { mapState, mapActions } from 'vuex'

export default {
  data () {
    return {
      leftDrawerOpen: false,
      
    }
  },
  computed: {
    ...mapState('auth', ['loggedIn'])
  },
  methods: {
    ...mapActions('auth', ['logOutUser'])
  }
}
</script>

