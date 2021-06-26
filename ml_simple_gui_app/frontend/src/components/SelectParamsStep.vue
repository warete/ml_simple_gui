<template>
    <v-skeleton-loader
            v-if="modelParamsLoading"
            type="list-item-three-line, list-item-three-line, image, actions"
    ></v-skeleton-loader>
    <v-row
            v-else
    >
        <v-col
                v-for="code in Object.keys(modelParams)"
                :key="modelParams[code].code"
        >
            <v-text-field
                    :label="modelParams[code].name"
                    :name="modelParams[code].code"
                    :value="modelParams[code].defaultValue"
                    @change="event => onParamValueChange(event, modelParams[code].code)"
                    required
            ></v-text-field>
        </v-col>
    </v-row>
</template>

<script>
    import {mapActions, mapGetters} from "vuex";

    export default {
        name: "SelectParamsStep",
        props: ['isOpened'],
        data: () => ({}),
        methods: {
            ...mapActions({
                'setModelParam': 'main/setModelParam',
                'fetchModelParams': 'main/fetchModelParams',
            }),
            onParamValueChange(value, paramCode) {
                this.setModelParam({code: paramCode, value});
            }
        },
        computed: {
            ...mapGetters({
                'modelParams': 'main/modelParams',
                'modelParamsLoading': 'main/modelParamsLoading',
            })
        },
        watch: {
            isOpened: function (val) {
                if (val) {
                    this.fetchModelParams();
                }
            },
        },
    }
</script>

<style scoped>

</style>
