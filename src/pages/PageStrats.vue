<template>
  <q-page padding class="bg-info">
    
    <q-list
      seperated>
      <strat
      v-for="(strat, key) in strats"
      :key="key"
      :strat="strat"
      :id="key"
      class="q-mb-md">

      <q-separator />
      
      </strat>

      
    </q-list>

    <div class="fixed-bottom q-mb-xl text-center">
      <q-btn
        @click="showAddStrat = true"
        round
        color="primary"
        size="24PX"
        icon="add"
      />
    </div>

  <q-dialog v-model="showAddStrat">
      <add-strat />
    </q-dialog>

  </q-page>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      showAddStrat: false
    }
  },
    computed: {
      ...mapGetters('strats', ['strats'])
    },
    components: {
      'strat': require('components/Strats/Strat.vue').default,
      'add-strat': require('components/Strats/AddStrat.vue').default
    }
  }
</script>

<style scoped lang="scss">

</style>
