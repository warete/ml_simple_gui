<template>
    <div>
      Загрузите файл с выборкой
        <v-file-input
                :rules="rules"
                accept=".csv"
                placeholder="Файл с обучающей выборкой"
                label="Файл с обучающей выборкой"
                ref="dataFile"
                @change="onFileChange"
        ></v-file-input>
      или выберите загруженный ранее файл
      <v-select
            :items="uploadedFilesSelect"
            item-text="name"
            item-value="val"
            @change="file => onSelectFile(file)"
        ></v-select>
    </div>
</template>

<script>
    import {mapActions, mapGetters} from 'vuex';
    import {map} from 'lodash';

    export default {
        name: "UploadFilesStep",
        props: ['isOpened'],
        data: () => ({
            rules: [
                value => !value || value.size < 200000000 || 'Файл должен быть меньше 200 МБ!',
            ],
        }),
        computed: {
            ...mapGetters({
                'trainTestDataFile': 'main/trainTestDataFile',
                'uploadedFiles': 'main/uploadedFiles',
            }),
            uploadedFilesSelect() {
              return map(this.uploadedFiles, file => ({
                name: file,
                val: file
              }))
            }
        },
        methods: {
            ...mapActions({
                'uploadFile': 'main/uploadFile',
                'fetchUploadedFiles': 'main/fetchUploadedFiles',
                'setTrainTestFile': 'main/setTrainTestFile',
            }),
            onFileChange: async function (file) {
                await this.uploadFile(file || {});
            },
            onSelectFile: async function (file) {
              this.setTrainTestFile(file);
            },
        },
        mounted: async function() {
            await this.fetchUploadedFiles();
        }
    }
</script>

<style scoped>

</style>
