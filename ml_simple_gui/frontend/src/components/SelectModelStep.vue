<template>
  <div>
    <v-row>
      <v-col cols="6"> Выберите обученную ранее модель </v-col>
      <v-col cols="6"> Или обучите новую </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-select
          :items="fittedModels"
          item-text="name"
          item-value="val"
          @change="(model) => onSelectModel(model)"
        ></v-select>
      </v-col>
      <v-col>
        <v-btn 
        @click="onFitNewModel"
        color="primary"
        >Обучить</v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import {mapGetters, mapActions} from 'vuex';

export default {
  name: "SelectModelStep",
  props: ["isOpened"],
  computed: {
    ...mapGetters({
      'fittedModels': 'main/fittedModels'
    }),
  },
  methods: {
    ...mapActions({
      uploadFile: "main/uploadFile",
      fetchUploadedFiles: "main/fetchUploadedFiles",
      setSelectedModel: "main/setSelectedModel",
    }),
    onSelectModel: async function (model) {
      this.setSelectedModel(model);
      this.$emit('next-step-number', 5);
      this.$emit('prev-step-number', 1);
    },
    onFitNewModel() {
      this.onSelectModel(null);
      this.$emit('next-step-number', null);
      this.$emit('prev-step-number', null);
      this.$emit('next-step');
    }
  },
  watch: {
    isOpened: function (val) {
      if (val) {
        this.setSelectedModel(null);
      }
    },
  },
};
</script>
