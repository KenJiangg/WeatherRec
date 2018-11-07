<template>
<body>
  <div id="app">
    <l-map :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker
      v-for="(marker, index) in markers"
      :key="index"
      :lat-lng="marker.position"
      @add="openPopup">
        <l-popup
        :content="marker.text"
        :options="{ autoClose: false, closeOnClick: false }">
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</body>
</template>

<script>
/* eslint-disable */
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";

export default {
  name: "Example",
  components: { LMap, LTileLayer, LMarker, LPopup },
  data() {
    return {
      zoom: 10,
      center: L.latLng(47.41322, -1.219482),
      url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      markers: [
        {
          position: L.latLng(47.41322, -1.219482),
          text: "Marker 1"
        },
        {
          position: L.latLng(47.31322, -1.219482),
          text: "Marker 2"
        }
      ]
    };
  },
  methods: {
    openPopup: function(event) {
      Vue.nextTick(() => {
        event.target.openPopup();
      });
    }
  }
};
</script>
<style>
html,
body,
#app {
  height: 97%;
  width: 90%;
  align-content: center;
}
</style>