<template>
    <div id="alert">
        <b-alert variant="dark" show dismissible>{{ message }}</b-alert>
        <br>
    </div>
</template>
<script>
/* eslint-disable */
export default {
  props: ["message"]
};
</script>
