<template>
    <div>
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
                    <q-item-label>Amount: {{ strat.amount }} </q-item-label>
                </q-item-section>

                <q-item-section 
                    @click="updateStrat({id: id, updates: { active: !strat.active } })"
                    clickable>
                   <q-checkbox
                      :value="strat.active" />
                </q-item-section>
            
            </div>

            <div class="row q-mb-md">
                <div class="col bg-info q-ma-sm">
                <q-item-section class="bg-green-5 ">
                    <q-item-label class="text-center text-weight-bolder" >BUY @</q-item-label>
                </q-item-section>

                <q-item-section >
                    <q-list
                    v-for="(buyCon, key) in strat.buyConditions"
                    :key="key"
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
                        v-for="(sellCon, key) in strat.sellConditions"
                        :key="key"
                        >
                        <q-item >
                        <q-item-section>
                            <q-item-label>Indicator: {{ sellCon.indicator }}</q-item-label>
                        </q-item-section>

                        <q-item-section>
                            <q-item-label>{{ sellCon.aob }} {{ sellCon.targetValue }} </q-item-label>
                        </q-item-section>

                        </q-item>
                    </q-list>
                    </q-item-section>
                </div>
            </div>

            
            
            </div>

        </q-item>
    </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
    props: ['strat', 'id'],
    methods: {
        ...mapActions('strats', ['updateStrat'])
    }
}
</script>

<style>

</style>