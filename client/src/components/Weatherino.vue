<template>
<!-- eslint-disable max-len -->
<div id="app">
  <div id="side">
  <alert :message= "message" v-if= "showMessage"></alert>
  <button type="button" class="btn btn-success btn-sm" v-b-modal.loc-modal>Add Location</button>
  <br><br>
  <table id = "table" class="table table-hover">
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
          <!--<button type="button" class="btn btn-success btn-sm" v-b-modal.loc-weather-modal @click= "openWeather(loc)">Weather</button>
          <button type="button" class="btn btn-dark btn-sm" v-b-modal.loc-update-modal @click="editLoc(loc)">Update</button>-->
          <button type="button" class="btn btn-outline-danger btn-sm" @click= "onDeleteLoc(loc)">X</button>
        </td>
        </b-card>
      </tr>
    </tbody>
  </table>
  <b-modal ref="addLocModal" id="loc-modal" title="Add a New Location" hide-footer>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
        label="Location:"
        label-for="form-title-input">
        <b-form-input id="form-title-input"
          type="text"
          v-model= "addLocForm.title"
          required
          placeholder="Enter Location">
        </b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </b-modal>
  <!--
  <b-modal ref="editLocModal" id="loc-update-modal" title="Update" hide-footer>
    <b-form @submit= "onSubmitUpdate" @reset= "onResetUpdate" class="w-100">
      <b-form-group id= "form-title-edit-group" label = "Location:" label-for= "form-title-edit-input">
        <b-form-input id="form-title-edit-input" type= "text" v-model= "editForm.title" required placeholder= "Enter Location">
        </b-form-input>
      </b-form-group>
      <b-button type= "submit" variant= "primary"> Update </b-button>
      <b-button type= "submit" variant= "danger"> Cancel </b-button>
    </b-form>
  </b-modal>
  <b-modal ref="openWeatherModal" id="loc-weather-modal" title="Weather" hide-footer>
    <table class = "table table-hover">
      <tbody>
        <tr v-for="(info, index) in info" :key="index">
          <td> {{ location }} </td>
          <button type="button" class="btn btn-outline-dark btn-sm" v-b-modal.loc-weather-icon-modal>VisuWeather</button>
          <button type="button" class="btn btn-outline-primary btn-sm" v-b-modal.rec-weather-modal>RecClothing</button>
        </tr>
        <tr v-for="(info, index) in info" :key="index">
          <td> {{ info.temperature }}°F </td>
          <td> Maximum : {{ info.max }}°F </td>
          <td> Minimum : {{ info.min }}°F </td>
        </tr>
        <tr v-for="(info, index) in info" :key="index">
          <td> {{ info.rain }} </td>
        </tr>
      </tbody>
    </table>
  </b-modal>
  <b-modal ref="openWeatherIconModal" id="loc-weather-icon-modal" hide-footer>
    <img :src="pic" style="max-width:100%;max-height:100%;text-align:center;"/>
  </b-modal>
  <b-modal ref="recWeatherModal" id="rec-weather-modal" hide-footer>
    <img :src="rec"/>
  </b-modal>
-->
</div>
<div id="full_div">
  <simpmaps :lat_long= "lat_long"></simpmaps>
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
      location: "",
      info: [],
      pic: "",
      icon: "",
      rec: ""
    };
  },
  components: {
    alert: Alert,
    simpmaps : Maps
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
          this.location = res.data.location;
          this.pic = res.data.pic;
          this.info = res.data.info;
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
  }
};
</script>
<style>
#side{
  float:left;
  width:300px;
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
  height:80%;
}
</style>