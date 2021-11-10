<template>
  <q-card class="newStratCard bg-info">
    <form @submit.prevent="submitForm">
        <q-card-section class="row">
          <div class="text-h6">Create new Strategy</div>
          <q-space/>
          <q-btn
            v-close-popup
            dense
            flat
            round
            color="primary"
            icon="close" />
        </q-card-section>

      <div class="col ">

        <q-card-section class="q-pt-none">
          <q-input
            autofocus
            class="bg-white"
            outlined
            v-model="stratToSubmit.name"
            label="Strategy Name"
            :rules="[val => val != '' || 'Strategy needs a name']"
            ref="name"
            hint="*" />
        </q-card-section> 

      <div class="row q-mb-lg">

        <q-card-section class="q-pt-none">
         <q-select
            outlined
            class="selectWidth bg-white"
            v-model="stratToSubmit.ticker"
            :options="tickerOptions"
            label="Ticker"
            :rules="[val => val != '' || 'Required']"
            ref="ticker"
            hint="*" />
        </q-card-section>
          
        <q-card-section class="q-pt-none">
         <q-select
            outlined
            class="selectWidth bg-white"
            v-model="stratToSubmit.timeframe"
            :options="timeframeOptions"
            label="Timeframe" 
            :rules="[val => val != '' || 'Required']"
            ref="timeframe"
            hint="*"/>
        </q-card-section>
          
        <q-card-section class="q-pt-none">
          <q-input
            outlined
            type="number"
            class="selectWidth bg-white"
            v-model="stratToSubmit.amount"
            label="Amount" 
            :rules="[val => val > 0 || 'Required']"
            ref="amount"
            hint="*"/>
        </q-card-section> 
      </div>

      <h6 class="q-ma-md">BUY CONDITION</h6>

      <div class="row q-mb-md">
        <q-card-section class="q-pt-none">
         <q-select
            outlined
            class="selectWidth bg-white"
            v-model="stratToSubmit.buyConditions.indicator"
            :options="indicatorOptions"
            label="Indicator" 
            :rules="[val => val != '' || 'Required']"
            ref="buyindicator"
            hint="*"/>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            outlined
            class="selectWidth bg-white"
            v-model="stratToSubmit.buyConditions.targetValue"
            type="number"
            label="Target value" 
            :rules="[val => val > 0 || 'Required']"
            ref="buyvalue"
            hint="*"/>
        </q-card-section> 
      </div>

      <h6 class="q-ma-md">SELL CONDITION</h6>

      <div class="row q-mb-md">
        <q-card-section class="q-pt-none">
         <q-select
            outlined
            class="selectWidth bg-white"
            v-model="stratToSubmit.sellConditions.indicator"
            :options="indicatorOptions"
            label="Indicator" 
            :rules="[val => val != '' || 'Required']"
            ref="sellindicator"
            hint="*"/>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            outlined
            class="selectWidth bg-white"
            v-model="stratToSubmit.sellConditions.targetValue"
            type="number"
            label="Target value" 
            :rules="[val => val >0|| 'Required']"
            ref="sellvalue"
            hint="*"/>
        </q-card-section> 
      </div>
    </div>
        <q-card-actions align="right">
          <q-btn class="q-ma-xs buttonstyle" type="submit" label="SAVE" color="primary"  />
        </q-card-actions>
      </form>
      </q-card>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      stratToSubmit: {
          name:'',
          active: false,
          ticker: '',
          amount: 0,
          timeframe: '',
          buyConditions: {
            indicator: '',
            targetValue: 0,
            conditionMet: false
          },
          sellConditions: {
            indicator: '',
            targetValue: 0,
            conditionMet: false
          }
      },
      tickerOptions: [
        'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'BTCETH', 'ZILUSDT'
      ],
      timeframeOptions: [
        '1m', '5m', '1h', '4h', '1d'
      ],
      indicatorOptions: [
        'RSI', 'SMA', 'MACD', 'EMA'
      ]
    }
  },
  methods: {
    ...mapActions('strats', ['addStrat']),
    submitForm() {
      this.$refs.name.validate()
      this.$refs.ticker.validate()
      this.$refs.amount.validate()
      this.$refs.timeframe.validate()
      this.$refs.buyindicator.validate()
      this.$refs.buyvalue.validate()
      this.$refs.sellindicator.validate()
      this.$refs.sellvalue.validate()
      if (!this.$refs.name.hasError && !this.$refs.ticker.hasError && !this.$refs.amount.hasError && !this.$refs.timeframe.hasError &&
      !this.$refs.buyindicator.hasError && !this.$refs.buyvalue.hasError && !this.$refs.sellindicator.hasError && !this.$refs.sellvalue.hasError) {
        this.submitStrat()
      }
    },
    submitStrat() {
      let payload = {
        strat: this.stratToSubmit
      }
      this.addStrat(payload)
      this.$emit('close')
    }
    
  }
}
</script>

<style lang="scss" scoped>
 .newStratCard {
  width: 650px;
 }
 .selectWidth {
  width: 150px;
 }
 .buttonstyle{
   width: 100px;
   height: 45px;
 }
</style>