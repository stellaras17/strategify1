<template>
  <q-card class="newStratCard bg-info">
    <form @submit.prevent="submitForm">
        <q-card-section class="row">
          <div class="text-h6">Edit Strategy</div>
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
            :rules="[val => !!val || 'Strategy needs a name']"
            ref="validation"
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
            :rules="[val => !!val || 'Required']"
            ref="validation"
            hint="*" />
        </q-card-section>
          
        <q-card-section class="q-pt-none">
         <q-select
            outlined
            class="selectWidth bg-white"
            v-model="stratToSubmit.timeframe"
            :options="timeframeOptions"
            label="Timeframe" 
            :rules="[val => !!val || 'Required']"
            ref="validation"
            hint="*"/>
        </q-card-section>
          
        <q-card-section class="q-pt-none">
          <q-input
            outlined
            type="number"
            class="selectWidth bg-white"
            v-model="stratToSubmit.amount"
            label="Amount" 
            :rules="[val => !!val || 'Required']"
            ref="validation"
            hint="*"/>
        </q-card-section> 
      </div>

      <h6 class="q-ma-md">BUY CONDITIONS</h6>

     <div
        class="row q-mb-md"
        v-for="(condition, key) in stratToSubmit.buyConditions"
        :key="key">
        <q-card-section class="q-pt-none" >
         <q-select
            outlined
            class="selectWidth bg-white"
            v-model="condition.indicator"
            :options="indicatorOptions"
            label="Indicator" 
            :rules="[val => !!val || 'Required']"
            ref="validation"
            hint="*"/>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            outlined
            class="selectWidth bg-white"
            v-model="condition.targetValue"
            type="number"
            label="Target value" 
            :rules="[val => !!val || 'Required']"
            ref="validation"
            hint="*"/>
        </q-card-section> 
      </div>

      <h6 class="q-ma-md">SELL CONDITIONS</h6>

      <div
        class="row q-mb-md"
        v-for="(condition, key) in stratToSubmit.sellConditions"
        :key="key">
        <q-card-section class="q-pt-none">
         <q-select
            outlined
            class="selectWidth bg-white"
            v-model="condition.indicator"
            :options="indicatorOptions"
            label="Indicator" 
            :rules="[val => !!val || 'Required']"
            ref="validation"
            hint="*"/>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            outlined
            class="selectWidth bg-white"
            v-model="condition.targetValue"
            type="number"
            label="Target value" 
            :rules="[val => !!val || 'Required']"
            ref="validation"
            hint="*"/>
        </q-card-section> 
      </div>
    </div>
        <q-card-actions align="right">
          <q-btn class="q-ma-xs buttonstyle" type="submit" label="SAVE" color="primary" v-close-popup />
        </q-card-actions>
      </form>
      </q-card>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  props: ['strat','id'],
  data() {
    return {
      stratToSubmit: {
          name:'',
          active: false,
          ticker: '',
          amount: 0,
          timeframe: '',
          buyConditions: {},
          sellConditions: {}
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
    ...mapActions('strats', ['updateStrat']),
    submitForm() {
      this.$refs.validation.validate()
      if (!this.$refs.validation.hasError) {
        this.submitStrat()
      }
    },
    submitStrat() {
      let payload = {
        id: this.id,
        updates: this.stratToSubmit
      }
      console.log(payload);
      this.updateStrat(payload)
    }
  },
  mounted() {
    this.stratToSubmit = Object.assign({}, this.strat)
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