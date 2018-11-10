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
          <b-card>
          <table class = "table table-hover">
            <tr>
              <td> {{ marker.title }} </td>
              <td>
                <img
                  :src="marker.pic"
                  style="max-width:100%;max-height:100%;text-align:center;"
                  /> </td>
            <tr>
              <td> Current: {{ marker.curr }}°F </td>
            </tr>
            <tr>
              <td> Max: {{ marker.max }}°F </td>
              <td> Min: {{ marker.min }}°F </td>
            </tr>
          </table>
        </b-card>
        </l-popup>
          <!--<b-modal ref="openWeatherIconModal" id="loc-weather-icon-modal" hide-footer>
            <p> {{ marker.pic }} </p>
          <img :src="marker.pic" style="max-width:100%;max-height:100%;text-align:center;"/>
          </b-modal> -->
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
  props: ["lat_long"],
  components: { LMap, LTileLayer, LMarker, LPopup },
  data() {
    return {
      zoom: 2,
      url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
      /*bounds: L.latLngBounds(bounds.bounds),
      maxBounds: L.latLngBounds(bounds.bounds),*/
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
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
    markers: function() {
      var output = [];
      for (var i = 0; i < this.lat_long.length; i++) {
        var obj = {};
        var current = this.lat_long[i];
        obj["pic"] = current["weather"]["matches"];
        obj["title"] = current["title"];
        obj["max"] = current["weather"]["max"];
        obj["min"] = current["weather"]["min"];
        obj["curr"] = current["weather"]["temperature"];
        obj["position"] = L.latLng(current["coords"][0], current["coords"][1]);
        output.push(obj);
      }
      return output;
    },
/*
    bounds: function(){
      var bounds = {}
      var mostleft = this.lat_long[0]['coords'][0]
      var mostright = this.lat_long[0]['coords'][0]
      var mostnorth = this.lat_long[0]['coords'][1]
      var mostsouth = this.lat_long[0]['coords'][1]
      for (var i = 0; i<this.lat_long.length; i++){
        var current = this.lat_long[i];
        if (current['coords'][0] < mostleft){
          mostleft = current['coords']
        }
        if (current['coords'][0] > mostright){
          mostright = current['coords']
        }
        if (current['coords'][1] < mostsouth){
          mostsouth = current['coords']
        }
        if (current['coords'][1] > mostnorth){
          mostnorth = current['coords']
        }
      }
      bounds['bounds'] = [[mostleft,mostsouth],[mostright,mostnorth]]
      return bounds
    }*/
  }
};
</script>
<style>
html,
body,
#app {
  height: 94%;
  width: 90%;
  margin-left: 50px;
}
</style>