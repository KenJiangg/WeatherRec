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
          <button type="button" class="btn btn-success btn-sm" @click= "openWeather(loc)">Weather</button>
          <button type="button" class="btn btn-dark btn-sm" v-b-modal.loc-update-modal @click="editLoc(loc)">Update</button>
          <button type="button" class="btn btn-danger btn-sm" @click= "onDeleteLoc(loc)">Delete</button>
        </td>
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
      editForm: {
        id: '',
        title: '',
      },
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
      this.editForm.id = '';
      this.editForm.title = '';
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
    editLoc(loc) {
      this.editForm = loc;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editLocModal.hide();
      const payload = {
        title: this.editForm.title,
      };
      this.updateLoc(payload, this.editForm.id);
    },
    updateLoc(payload, locID) {
      const path = `http://localhost:5000/index/${locID}`;
      axios.put(path, payload)
        .then((res) => {
          this.getLoc();
          this.message = 'Location updated';
          this.showMessage = true;
        })
        .catch((error) => {
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
      axios.delete(path)
        .then(() => {
          this.getLoc();
          this.message = 'Location removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getLoc();
        });
    },
    onDeleteLoc(loc) {
      this.removeLoc(loc.id);
    },
  },
  created() {
    this.getLoc();
  },
};
</script>
