<template>
  <div id="collect-buttons">
    <button v-bind:class="{ done: statusDatabase }">Start database</button>
    <button :disabled="!statusDatabase"  v-bind:class="{ done: statusMarca }">Collect "Marca"</button>
    <button :disabled="!statusModelo" v-bind:class="{ done: statusModelo }">Collect "Modelo"</button>
    <button :disabled="!statusDetalhe" v-bind:class="{ done: statusDetalhe }">Collect "Detalhe"</button>
    <br><br><hr>
  </div>
</template>

<script>
export default {
  name: 'Collect',
  data: function() {
    return {
      statusDatabase: false,
      statusMarca: false,
      statusModelo: false,
      statusDetalhe: false
    }
  }
}
</script>

<style scoped>
  #collect-buttons button{
    margin: 10px;
    width: 150px;
    height: 30px;
    cursor: pointer;
  }
  #collect-buttons button:disabled{
    cursor: not-allowed;
  }
  #collect-buttons button.done{
    background-color: #98FB98;
  }
</style>
