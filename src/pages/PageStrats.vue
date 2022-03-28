<template>
  <q-page style="width:100%" padding class="bg-info">
    <q-btn dense class="float-right" flat round icon="menu" @click="rightDrawerOpen=!rightDrawerOpen" />

      <top-three />

      <chart/>

      <q-separator class="q-mb-sm q-mt-sm" color="primary"/>

      <p class="text-h6"> Budget: {{coins}}$ </p>
      <div class="row q-mt-xl q-mb-sm text-center">
        <q-btn
          @click="showAddStrat = true"
          color="primary"
          size="16PX"
          label="Add A New Strategy"
        />
      </div>
      
      
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

      <div v-if="!Object.keys(stratsInactive).length && !Object.keys(stratsActive).length" class="headerStyle">
      <span> You have no strategies yet, click the button above to start creating your Strategies!</span>
      </div>

      <div>
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

    
      </div>

      <q-drawer v-model="rightDrawerOpen" side="right" bordered>
      
      <news/>

    </q-drawer>

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
      showAddStrat: false,
      rightDrawerOpen: false,
      chartTicker: 'BTCUSDT'
    }
  },
    computed: {
      ...mapGetters('strats', ['stratsInactive', 'stratsActive', 'coins'])
    },
    components: {
      'strat': require('components/Strats/Strat.vue').default,
      'add-strat': require('components/Strats/AddStrat.vue').default,
      'top-three': require('src/components/TopThree.vue').default,
      'chart': require('src/components/Chart.vue').default,
      'news': require('components/News.vue').default
  
    }
  }
</script>

<style scoped lang="scss">
  .headerStyle {
    font-size: 18px;
    color: #1E2329;
  }
  .button {
    margin-top:500px;
  }
</style>
