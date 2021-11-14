<template>
    <form @submit.prevent="submitForm">
    <div class="text-h6">{{ tab }} Here</div>
        
    <div class="row q-mt-md">
        <q-input
          class="col bg-white"
          outlined
          v-model="formData.email"
          label="Email"
          lazy-rules
          ref="email"
          :rules="[val => val.length >0 || 'Email is required', val => validEmail(val) || 'Please enter a valid email address']"  />
    </div>
    <div class="row q-mt-xs">
         <q-input
           class="col bg-white"
           outlined
           v-model="formData.password"
           label="Password"
           type="password"
           lazy-rules
           ref="password"
           :rules="[  val => val.length >0 || 'Password is required', val => val.length >= 6 || 'Please use minimum 6 characters']" />
    </div>
    <div class="row q-mt-xs">
        <q-space />
         <q-btn color="primary" text-color="secondary" :label="tab" type="submit"/>
    </div>
    </form>
</template>

<script>
export default {
    props:['tab'],
    data() {
        return {
            formData: {
                email: '',
                password: ''
            }
        }
    },
    methods: {
        submitForm() {
            this.$refs.email.validate()
            this.$refs.password.validate()
            if (!this.$refs.email.hasError && !this.$refs.password.hasError) {
                if(this.tab=='Login') {
                    console.log('login the user');
                } else {
                    console.log('register user');
                }
            }
        },
        validEmail(email) {
            const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                return re.test(String(email).toLowerCase());
        }
    }
}
</script>

<style>

</style>