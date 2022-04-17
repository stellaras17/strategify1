import { openURL } from 'quasar'
import fetch from 'node-fetch'
export default {
    data() {
        return {
            news: []
        }
    },
    methods: {
        fetchNews(){
            const date = new Date();
            date.setDate(date.getDate() - 10)
            let d = date.getFullYear() + '-' + (parseInt(date.getMonth())+1).toString() + '-' + date.getDate()
            console.log(d);
            var news = new Array
            fetch('https://newsapi.org/v2/everything?q=bitcoin news OR cryptocurrency news&from='+d+'&sortBy=publishedAt&apiKey=80489bc6cf9d4a489e5cc3aa0daf8f05')
            .then(a=>a.json())
            .then(response => response.articles.forEach(element => {
                news.push(element)
            }))
            this.news=news
            
        },
        goToUrl(url) {
            openURL(url)
        }
    },
    mounted() {
        this.fetchNews()
    }
}