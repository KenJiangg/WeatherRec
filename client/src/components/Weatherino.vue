<template>
  <!-- eslint-disable max-len -->
  <div id="app">
    <link href="https://afeld.github.io/emoji-css/emoji.css" rel="stylesheet">
    <div id="side">
      <alert :message="message" v-if="showMessage"></alert>
      <button type="button" class="btn btn-success btn-sm" v-b-modal.loc-modal>Add Location</button>
      <br>
      <br>
      <div style="height:450px;overflow:auto;">
      <table id="table" class="table table-hover">
        <thead>
          <tr>
            <th scope="col">Location</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(loc, index) in yourLoc" :key="index">
            <b-card style="max-width: 30rem;">
              <td>{{ loc.title }}</td>
              <td>
                <button
                  type="button"
                  class="btn btn-success btn-sm"
                  v-b-modal.loc-weather-modal
                  @click="openWeather(loc)"
                >Weather</button>
                <!-- <button type="button" class="btn btn-outline-danger btn-sm" @click= "onDeleteLoc(loc)">X</button> -->
              </td>
              <td>
                <i :class="loc.emoji"></i>
              </td>
            </b-card>
          </tr>
        </tbody>
      </table>
      </div>
      <b-modal ref="addLocModal" id="loc-modal" title="Add a New Location" hide-footer>
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group id="form-title-group" label="Location:" label-for="form-title-input">
            <b-form-input
              id="form-title-input"
              type="text"
              v-model="addLocForm.title"
              required
              placeholder="Enter Location"
            ></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
      </b-modal>
      <b-modal ref="editLocModal" id="loc-update-modal" title="Update" hide-footer>
        <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
          <b-form-group
            id="form-title-edit-group"
            label="Location:"
            label-for="form-title-edit-input"
          >
            <b-form-input
              id="form-title-edit-input"
              type="text"
              v-model="editForm.title"
              required
              placeholder="Enter Location"
            ></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="submit" variant="danger">Cancel</b-button>
        </b-form>
      </b-modal>
      <b-modal size="lg" ref="openWeatherModal" id="loc-weather-modal" title="Graphs" hide-footer>
        <table class="table table-hover">
          <tbody>
            <tr>
              <td>
                <d3-multi-line
                  :data="minMax"
                  :options="minMaxOptions"
                  :margin="margin"
                  @range-updated="(dateTimeStart, dateTimeEnd) => fetchDataWithCurrentInterval(dateTimeStart, dateTimeEnd)"
                  width="100%"
                  height="300px"
                ></d3-multi-line>
              </td>
            </tr>
            <tr>
              <td>
                <d3-line
                  :data="precip"
                  :options="precipOptions"
                  :margin="margin"
                  @range-updated="(dateTimeStart, dateTimeEnd) => fetchDataWithCurrentInterval(
              dateTimeStart, dateTimeEnd)"
                  width="100%"
                  height="300px"
                ></d3-line>
              </td>
            </tr>
            <tr>
              <td>
                <d3-line
                  :data="wind"
                  :options="windOptions"
                  :margin="margin"
                  @range-updated="(dateTimeStart, dateTimeEnd) => fetchDataWithCurrentInterval(
              dateTimeStart, dateTimeEnd)"
                  width="100%"
                  height="300px"
                ></d3-line>
              </td>
            </tr>
            <tr>
              <td>
                <d3-line
                  :data="hum"
                  :options="humOptions"
                  :margin="margin"
                  @range-updated="(dateTimeStart, dateTimeEnd) => fetchDataWithCurrentInterval(
              dateTimeStart, dateTimeEnd)"
                  width="100%"
                  height="300px"
                ></d3-line>
              </td>
            </tr>
          </tbody>
        </table>
      </b-modal>
    </div>
    <div id="full_div">
      <simpmaps :lat_long="lat_long"></simpmaps>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import axios from "axios";
import Alert from "./Alert";
import Maps from "./Maps";

export default {
  data() {
    return {
      yourLoc: [],
      lat_long: [],
      addLocForm: {
        title: ""
      },
      message: "",
      showMessage: false,
      editForm: {
        id: "",
        title: ""
      },
      precip: [],
      wind: [],
      hum: [],
      minMax: {}
    };
  },
  components: {
    alert: Alert,
    simpmaps: Maps
  },
  methods: {
    getLoc() {
      const path = "http://localhost:5000/index";
      axios
        .get(path)
        .then(res => {
          this.yourLoc = res.data.yourLoc;
          this.message = res.data.message;
          this.lat_long = res.data.lat_long;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addLoc(payload) {
      const path = "http://localhost:5000/index";
      axios
        .post(path, payload)
        .then(() => {
          this.getLoc();
          this.showMessage = true;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
          this.getLoc();
        });
    },
    initForm() {
      this.addLocForm.title = "";
      this.editForm.id = "";
      this.editForm.title = "";
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addLocModal.hide();
      const payload = {
        title: this.addLocForm.title
      };
      this.addLoc(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addLocModal.hide();
      this.initForm();
    },
    editLoc(loc) {
      this.editForm = loc;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editLocModal.hide();
      const payload = {
        title: this.editForm.title
      };
      this.updateLoc(payload, this.editForm.id);
    },
    updateLoc(payload, locID) {
      const path = `http://localhost:5000/index/${locID}`;
      axios
        .put(path, payload)
        .then(res => {
          this.getLoc();
          this.message = "Location updated";
          this.showMessage = true;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
          this.getLoc();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editLocModal.hide();
      this.initForm();
      this.getLoc();
    },
    removeLoc(locID) {
      const path = `http://localhost:5000/index/${locID}`;
      axios
        .delete(path)
        .then(() => {
          this.getLoc();
          this.message = "Location removed!";
          this.showMessage = true;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
          this.getLoc();
        });
    },
    onDeleteLoc(loc) {
      this.removeLoc(loc.id);
    },
    onWeather(evt) {
      evt.preventDefault();
      const payload = {
        title: this.loc.title
      };
      this.openWeather(payload);
    },
    openWeather(payload) {
      const path = "http://localhost:5000/index/weather";
      axios
        .put(path, payload)
        .then(res => {
          (this.precip = res.data.precip),
            (this.wind = res.data.wind),
            (this.hum = res.data.hum),
            (this.minMax = res.data.minMax);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
          this.getLoc();
        });
    }
  },
  created() {
    this.getLoc();
  },
  computed: {
    precipOptions: function() {
      var obj = {};
      obj["axisXLabel"] = "Next Week's Precipitation";
      obj["axisYLabel"] = "Chance of Precipitation (%)";
      obj["tickSize"] = 5;
      return obj;
    },
    windOptions: function() {
      var obj = {};
      obj["axisXLabel"] = "Next Week's Wind";
      obj["axisYLabel"] = "Wind Speed (mph) ";
      obj["tickSize"] = 5;
      return obj;
    },
    minMaxOptions: function() {
      var obj = {};
      obj["axisXLabel"] = "Next Week's Temperature";
      obj["axisYLabel"] = "Temperature (°F) ";
      obj["tickSize"] = 5;
      return obj;
    },
    humOptions: function() {
      var obj = {};
      obj["axisXLabel"] = "Next Week's Humidity";
      obj["axisYLabel"] = "Humidity (%) ";
      obj["tickSize"] = 5;
      return obj;
    },
},
}
</script>
<style>
#side {
  float: left;
  width: 300px;
}
#full_div {
  position: absolute;
  overflow-x: auto;
  top: 100px;
  right: 0;
  left: 500px;
  bottom: 0;
  padding-left: 8px;
  width: 60%;
  height: 80%;
}
</style>