<template>
  <q-page padding class="bg-info">

    <div v-if="Object.keys(stratsActive).length" >
    <span class="headerStyle"> Active Strategies</span>
    <q-separator class="q-mb-sm" color="primary"/>
    </div>
    <q-list
      seperated>
      <strat
      v-for="(strat, key) in stratsActive"
      :key="key"
      :strat="strat"
      :id="key"
      class="q-mb-md">
      </strat>
    </q-list>

    <div v-if="Object.keys(stratsInactive).length" class="headerStyle">
    <span> Inactive Strategies</span>
    <q-separator class="q-mb-sm" color="primary"/>
    </div>
    <q-list
      seperated>
      <strat
      v-for="(strat, key) in stratsInactive"
      :key="key"
      :strat="strat"
      :id="key"
      class="q-mb-md">
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
      <add-strat @close="showAddStrat = false" />
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
      ...mapGetters('strats', ['stratsInactive', 'stratsActive'])
    },
    components: {
      'strat': require('components/Strats/Strat.vue').default,
      'add-strat': require('components/Strats/AddStrat.vue').default
    }
  }
</script>

<style scoped lang="scss">
  .headerStyle {
    font-size: 18px;
    color: #1E2329;
  }
</style>
