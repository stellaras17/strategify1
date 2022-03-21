<template>
    <div>
        <q-banner class="bg-primary text-secondary ">
            {{ strat.name}}
            <q-btn
              @click="promptToDelete(id)"
              class="float-right"
              dense
              flat
              round
              color="secondary"
              icon="delete" />
              
            <q-btn
              @click="showEditStrat = true"
              class="float-right"
              dense
              flat
              round
              color="secondary"
              icon="edit" />

            <q-btn
              @click="promptToShare(id, strat)"
              class="float-right"
              dense
              flat
              round
              color="secondary"
              icon="share" />
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
                    clickable
                    class="cursor-pointer">
                   <q-checkbox
                     class="no-pointer-events cursor-pointer"
                     label="Active"
                      :value="strat.active" />
                </q-item-section>
            
            </div>

            <div class="row q-mb-md">
                <div class="col bg-info q-ma-sm">
                <q-item-section class="bg-green-5 ">
                    <q-item-label class="text-center text-weight-bolder" >BUY @</q-item-label>
                </q-item-section>

                <q-item-section >
                    
                    <q-item >
                    <q-item-section>
                        <q-item-label>Indicator: {{ strat.buyConditions.indicator }}</q-item-label>
                    </q-item-section>

                    <q-item-section>
                        <q-item-label> {{ strat.buyConditions.targetValue }}</q-item-label>
                    </q-item-section>

                    </q-item>
                    
                </q-item-section>
                </div>

                <div class="col bg-info q-ma-sm">
                <q-item-section class="bg-red-5 ">
                    <q-item-label class="text-center text-weight-bolder" >SELL @</q-item-label>
                </q-item-section>

                <q-item-section >
                        <q-item >
                        <q-item-section>
                            <q-item-label>Indicator: {{ strat.sellConditions.indicator }}</q-item-label>
                        </q-item-section>

                        <q-item-section>
                            <q-item-label> {{ strat.sellConditions.targetValue }} </q-item-label>
                        </q-item-section>

                        </q-item>
                    </q-item-section>
                </div>
            </div>
            </div>

        <q-dialog v-model="showEditStrat">
         <edit-strat :strat="strat" :id="id" @close="showEditStrat = false" />
        </q-dialog>

        </q-item>
    </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
    data() {
        return {
            showEditStrat: false
        }
    },
    props: ['strat', 'id'],
    methods: {
        ...mapActions('strats', ['updateStrat', 'deleteStrat']),
        ...mapActions('hub', ['dbAddStrat']),
        promptToDelete(id) {
            this.$q.dialog({
                title: 'Confirm',
                message: 'Are you sure you want to delete this Strategy? Once deleted, it cannot be retrieved',
                cancel: true,
                persistent: true
            }).onOk(() => {
                this.deleteStrat(id)
            })
        },
        promptToShare(key, strat) {
            this.$q.dialog({
                title: 'Confirm',
                message: 'Share strategy to the hub?',
                cancel: true,
                persistent: true
            }).onOk(() => {
                console.log(key);
                let payload = {
                    id: key,
                    strat: strat
                }
                this.dbAddStrat(payload);
            })
        }
    },
    components: {
        'edit-strat': require('components/Strats/EditStrat.vue').default
    }
}
</script>

<style>

</style>