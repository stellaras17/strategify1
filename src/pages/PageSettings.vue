<template>
  <q-page class="bg-info q-pa-md">
    <q-list bordered padding>
      <q-item-label header>Settings</q-item-label>

      <q-item tag="label" v-ripple>
        <q-item-section>
          <q-item-label>Show Chart</q-item-label>
        </q-item-section>
        <q-item-section avatar>
          <div class="q-gutter-sm">
            <q-toggle v-model="showChart" />
          </div>
        </q-item-section>
      </q-item>

      <q-item
        tag="label"
        :class="!settings.showChart ? 'disabled' : ''">
        <q-item-section>
          <q-item-label>Ticker to show chart on home page</q-item-label>
        </q-item-section>
        <q-item-section avatar>
          <div class="q-gutter-sm">
            <q-radio v-model="tickerForChart" val="BTCUSDT" label="BTCUSDT" />
            <q-radio v-model="tickerForChart" val="BNBUSDT" label="BNBUSDT" />
            <q-radio v-model="tickerForChart" val="ETHUSDT" label="ETHUSDT" />
          </div>
        </q-item-section>
      </q-item>

    </q-list>
  </q-page>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'

export default {
  data() {
    return {
      
    }
  },
  computed: {
    ...mapGetters('settings', ['settings']),
    tickerForChart: {
      get() {
        return this.settings.tickerForChart
      },
      set(value) {
        this.setTickerForChart(value)
      }
    },
    showChart: {
      get() {
        return this.settings.showChart
      },
      set(value) {
        this.setShowChart(value)
      }
    }
  },
  methods: {
    ...mapActions('settings', ['setTickerForChart', 'setShowChart'])
  }
}
</script>

<style lang="scss" scoped>
.selectWidth {
  width: 150px;
 }
</style>