// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable */
import "bootstrap/dist/css/bootstrap.css";
import Vue from "vue";
import L from "leaflet";
import BootstrapVue from "bootstrap-vue";
import App from "./App";
import router from "./router";
import "leaflet.icon.glyph";

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png")
});

Vue.config.productionTip = false;

Vue.use(BootstrapVue);

/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  components: { App },
  template: "<App/>"
});
