<template>
  <q-page padding class="bg-info">
    
    <q-list
      bordered
      v-for="strat in strats"
      :key="strat.id"
      class="q-mb-lg">
      <q-banner class="bg-primary text-secondary ">
         {{ strat.name}}
        </q-banner>

      <q-item class="bg-white">
        <div class="col ">
          <div class="row q-mb-lg q-ml-sm">

            <q-item-section>
              <q-item-label>Ticker: {{ strat.ticker }}</q-item-label>
            </q-item-section>

            <q-item-section>
              <q-item-label>Timeframe: {{ strat.timeframe }}</q-item-label>
            </q-item-section>

            <q-item-section>
              <q-item-label>Amount: {{ strat.amount }}</q-item-label>
            </q-item-section>

            <q-item-section >
              <q-checkbox v-model="strat.active" label="Active" />
            </q-item-section>
          
          </div>

          <div class="row q-mb-md">
            <div class="col bg-info q-ma-sm">
              <q-item-section class="bg-green-5 ">
                <q-item-label class="text-center text-weight-bolder" >BUY @</q-item-label>
              </q-item-section>

              <q-item-section >
                <q-list
                v-for="buyCon in strat.buyConditions"
                :key="buyCon.id"
                >
                <q-item >
                  <q-item-section>
                    <q-item-label>Indicator: {{ buyCon.indicator }}</q-item-label>
                  </q-item-section>

                  <q-item-section>
                    <q-item-label>{{ buyCon.aob }} {{ buyCon.targetValue }}</q-item-label>
                  </q-item-section>

                </q-item>
              </q-list>
              </q-item-section>
            </div>

            <div class="col bg-info q-ma-sm">
              <q-item-section class="bg-red-5 ">
                <q-item-label class="text-center text-weight-bolder" >SELL @</q-item-label>
              </q-item-section>

              <q-item-section >
                    <q-list
                    v-for="sellCon in strat.sellConditions"
                    :key="sellCon.id"
                    >
                    <q-item >
                      <q-item-section>
                        <q-item-label>Indicator: {{ sellCon.indicator }}</q-item-label>
                      </q-item-section>

                      <q-item-section>
                        <q-item-label>{{ sellCon.aob }} {{ sellCon.targetValue }}</q-item-label>
                      </q-item-section>

                    </q-item>
                  </q-list>
                </q-item-section>
            </div>
          </div>

          
          
        </div>

      </q-item>

      
    </q-list>
  </q-page>
</template>

<script>
export default {
  data() {
    return{
      strats: [
        {
          id: 1,
          name:'BTC RSI',
          active: false,
          ticker: 'BTCUSDT',
          amount: 100,
          timeframe: '5m',
          buyConditions: [{
            id:111,
            indicator: 'RSI',
            aob: 'below',
            targetValue: 20,
            conditionMet: false
          }],
          sellConditions: [{
            id:112,
            indicator: 'RSI',
            aob: 'above',
            targetValue: 80,
            conditionMet: false
          }]
        },
        {
          id: 2,
          name:'ETH RSI',
          active: false,
          ticker: 'ETHUSDT',
          amount: 100,
          timeframe: '5m',
          buyConditions: [{
            id:121,
            indicator: 'RSI',
            aob: 'below',
            targetValue: 20,
            conditionMet: false
          }],
          sellConditions: [{
            id:122,
            indicator: 'RSI',
            aob: 'above',
            targetValue: 80,
            conditionMet: false
          }]
        },
        {
          id: 3,
          name:'ZIL RSI',
          active: false,
          ticker: 'ZILUSDT',
          amount: 100,
          timeframe: '5m',
          buyConditions: [{
            id:131,
            indicator: 'RSI',
            aob: 'below',
            targetValue: 20,
            conditionMet: false
          }],
          sellConditions: [{
            id:132,
            indicator: 'RSI',
            aob: 'above',
            targetValue: 80,
            conditionMet: false
          }]
        },

      ]
    }
  }
}
</script>

<style scoped lang="scss">

</style>
