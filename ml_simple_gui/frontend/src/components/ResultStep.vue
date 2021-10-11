<template>
    <v-row>
        <v-col cols="6">
            <v-skeleton-loader
                    v-if="resultLoading"
                    type="list-item-three-line, list-item-three-line, image, actions"
            ></v-skeleton-loader>
            <template
                    v-else
            >
                <v-list class="transparent">
                    <v-list-item>
                        <v-list-item-title>Точность</v-list-item-title>
                        <v-list-item-subtitle class="text-right">
                            {{ result.accuracy }}%
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                        <v-list-item-title>Чувствительность</v-list-item-title>
                        <v-list-item-subtitle class="text-right">
                            {{ result.sensitivity }}%
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                        <v-list-item-title>Специфичность</v-list-item-title>
                        <v-list-item-subtitle class="text-right">
                            {{ result.specificity }}%
                        </v-list-item-subtitle>
                    </v-list-item>
                </v-list>
            </template>
        </v-col>
    </v-row>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";

    export default {
        name: "ResultStep",
        props: ['isOpened'],
        methods: {
            ...mapActions({
                'fetchResults': 'main/fetchResults',
            }),
        },
        computed: {
            ...mapGetters({
                'trainTestDataFile': 'main/trainTestDataFile',
                'learningEpochs': 'main/learningEpochs',
                'modelParams': 'main/modelParams',
                'result': 'main/result',
                'resultLoading': 'main/resultLoading',
            })
        },
        watch: {
            isOpened: function (val) {
                if (val) {
                    this.fetchResults({
                        file: this.trainTestDataFile,
                        modelParams: this.modelParams,
                    });
                }
            },
        },
    }
</script>

<style scoped>

</style>
