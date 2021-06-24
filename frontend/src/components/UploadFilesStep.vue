<template>
  <div>
    <v-file-input
        :rules="rules"
        accept=".csv"
        placeholder="Файл с обучающей выборкой"
        label="Файл с обучающей выборкой"
        ref="dataFile"
        @change="onFileChange"
    ></v-file-input>
  </div>
</template>

<script>
import axios from 'axios';
import {API_DOMAIN} from '../constants';

export default {
  name: "UploadFilesStep",
  data: () => ({
    rules: [
      value => !value || value.size < 200000000 || 'Файл должен быть меньше 200 МБ!',
    ],
  }),
  methods: {
    onFileChange: function (file) {
      const form = new FormData();
      form.append('file', file);
      axios.post(`${API_DOMAIN}/upload_data/`,
          form,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
      )
          .then(function () {
            console.log('SUCCESS!!');
          })
          .catch(function () {
            console.log('FAILURE!!');
          });
    }
  }
}
</script>

<style scoped>

</style>
