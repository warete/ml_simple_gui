<template>
    <div>
        <v-file-input
                :rules="rules"
                accept=".csv"
                placeholder="Файл с обучающей выборкой"
                label="Файл с обучающей выборкой"
        ></v-file-input>
    </div>
</template>

<script>
    export default {
        name: "UploadFilesStep",
        data: () => ({
            rules: [
                value => !value || value.size < 200000000 || 'Файл должен быть меньше 200 МБ!',
            ],
        }),
    }
</script>

<style scoped>

</style>