import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import VueSocketIOExt from 'vue-socket.io-extended';
import { io } from 'socket.io-client';
import {register} from '@/components/public/register'
import { createI18n } from 'vue-i18n'
import deDEBase from '@/lang/de-DE.json'

export const socket = io('http://localhost:1992');

export const i18n = createI18n({
    locale: 'de-DE',
    messages: {
        'de-DE': deDEBase
    }
})

export const app = createApp(App)

register(app)
app.use(i18n)
app.use(store).use(router)
app.use(VueSocketIOExt, socket)
app.mount('#app')