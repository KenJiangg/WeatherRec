<template>
    <div id="alert">
        <b-alert variant="success" show dismissible>{{ message }}</b-alert>
        <br>
    </div>
</template>
<script>
export default {
  props: ["message"]
};
</script>
