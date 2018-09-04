import Vue from 'vue';
import Router from 'vue-router';
import Weatherino from '@/components/Weatherino';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Weatherino',
      component: Weatherino,
    },
  ],
  mode: 'history',
});
