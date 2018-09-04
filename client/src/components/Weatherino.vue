<template>
<!-- eslint-disable max-len -->
<div id="app">
  <alert :message= "message" v-if= "showMessage"></alert>
  <button type="button" class="btn btn-success btn-sm" v-b-modal.loc-modal>Add Location</button>
  <br><br>
  <table class="table table-hover">
    <thead>
      <tr>
        <th scope="col">Location</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(loc, index) in yourLoc" :key="index">
        <td>{{ loc.title }}</td>
        <td>
          <button type="button" class="btn btn-success btn-sm">Weather</button>
          <button type="button" class="btn btn-danger btn-sm">Delete</button>
        </td>
      </tr>
    </tbody>
  </table>
  <b-modal ref="addLocModal" id="loc-modal" title="Add a new Location" hide-footer>
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
</div>
</template>

<script>
/* eslint-disable no-unused-vars */
import axios from 'axios';
import Alert from './Alert';

export default{
  data() {
    return {
      yourLoc: [],
      addLocForm: {
        title: '',
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getLoc() {
      const path = 'http://localhost:5000/index';
      axios.get(path)
        .then((res) => {
          this.yourLoc = res.data.yourLoc;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addLoc(payload) {
      const path = 'http://localhost:5000/index';
      axios.post(path, payload)
        .then(() => {
          this.getLoc();
          this.message = 'Location Added';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getLoc();
        });
    },
    initForm() {
      this.addLocForm.title = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addLocModal.hide();
      const payload = {
        title: this.addLocForm.title,
      };
      this.addLoc(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addLocModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getLoc();
  },
};
</script>
