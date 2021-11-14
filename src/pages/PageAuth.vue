<template>
  <q-page padding class="bg-info">
      <q-card class="tabsStyle">
        <q-tabs
          v-model="tab"
          dense
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="justify"
          narrow-indicator
        >
          <q-tab name="Login" label="Log in" />
          <q-tab name="Register" label="Register" />
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="tab" animated >
          <q-tab-panel name="Login">
            <login-register :tab="tab" />
          </q-tab-panel>

          <q-tab-panel name="Register">
            <login-register :tab="tab" />
          </q-tab-panel>

        </q-tab-panels>
      </q-card>
  </q-page>
</template>

<script>
export default {
    data () {
        return {
            tab: 'Login'
        }
  },
  components: {
      'login-register': require('src/components/Authentication/LoginRegister.vue').default
  }
}
</script>

<style lang="scss" scoped>
    .tabsStyle {
        max-width: 800px;
        margin: 0 auto;
    }
</style>