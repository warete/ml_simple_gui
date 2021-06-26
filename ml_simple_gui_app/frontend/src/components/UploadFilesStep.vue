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
    import {mapActions, mapGetters} from 'vuex';

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
                'trainTestDataFile': 'main/trainTestDataFile'
            })
        },
        methods: {
            ...mapActions({
                'uploadFile': 'main/uploadFile'
            }),
            onFileChange: async function (file) {
                await this.uploadFile(file || {});
            }
        }
    }
</script>

<style scoped>

</style>
