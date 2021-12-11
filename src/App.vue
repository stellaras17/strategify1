<template>
  <div id="q-app">
    <router-view />
  </div>
</template>
<script>
import { mapActions } from 'vuex'

export default {
  methods: {
    ...mapActions('auth', ['handleAuthStateChange']),
    ...mapActions('settings', ['getSettings']),
  },
  mounted() {
    this.handleAuthStateChange(),
    this.getSettings()
  }
}
</script>
