<template>
  <q-page padding class="bg-info">
    
    <q-list
      >
      <strat
      v-for="(strat, key) in strats"
      :key="key"
      :strat="strat"
      :id="key"
      class="q-mb-md">
      </strat>

      
    </q-list>
  </q-page>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
    computed: {
      ...mapGetters('strats', ['strats'])
    },
    components: {
      'strat': require('components/Strats/Strat.vue').default
    }
  }
</script>

<style scoped lang="scss">

</style>
