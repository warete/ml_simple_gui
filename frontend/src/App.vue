<template>
    <v-app>
        <v-app-bar app>
            <v-toolbar-title>{{ applicationTitle }}</v-toolbar-title>
        </v-app-bar>

        <v-main>
            <router-view></router-view>
        </v-main>
    </v-app>
</template>

<script>

    export default {
        name: 'App',

        data: () => ({
            applicationTitle: 'Simple Machine Learning GUI'
        }),
    };
</script>
