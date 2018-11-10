<template>
<body>
  <div id="app">
    <l-map :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker
      v-for="marker in markers"
      :key="marker.text"
      :lat-lng="marker.position"
      >
        <l-popup>
          <table class = "table table-hover">
            <tr>
              <td> {{ marker.title }} </td>
            <tr>
              <td> Current: {{ marker.curr }}°F </td>
            </tr>
            <tr>
              <td> Max: {{ marker.max }}°F </td>
              <td> Min: {{ marker.min }}°F </td>
            </tr>
          </table>
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
  props: ['lat_long'],
  components: { LMap, LTileLayer, LMarker, LPopup },
  data() {
    return {
      zoom: 1,
      url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
/*      markers: [
        {
          position: L.latLng(47.41322, -1.219482),
          text: "Marker 1"
        },
        {
          position: L.latLng(47.31322, -1.219482),
          text: "Marker 2"
        }
      ]*/
    };
  },
  computed: {
    markers: function(){
      var output = []
      for(var i = 0; i<this.lat_long.length; i++){
        var obj = {};
        var current = this.lat_long[i]
        obj['title'] = current['title']
        obj['max'] = current['weather']['max']
        obj['min'] = current['weather']['min']
        obj['curr'] = current['weather']['temperature']
        obj['position'] = L.latLng(current['coords'][0],current['coords'][1])
        output.push(obj)
      }
        return output
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