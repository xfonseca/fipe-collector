<template>
  <div id="collect-buttons">
    <button :disabled="statusDatabase" v-bind:class="{ done: statusDatabase }" @click="startDatabase($event)">Start database</button>
    <button :disabled="!statusDatabase"  v-bind:class="{ done: statusMarca }" @click="collectMarca($event)">Collect "Marca"</button>
    <button :disabled="!statusMarca" v-bind:class="{ done: statusCarro }" @click="collectCarro($event)">Collect "Carro"</button>
    <button :disabled="!statusCarro" v-bind:class="{ done: statusDetalhe }" @click="collectDetalhe($event)">Collect "Detalhe"</button>
    <button :disabled="!statusCarro" @click="copySqlToClipboard()">Copy SQL to clipboard</button>
    <br><br><hr>
  </div>
</template>

<script>
import { EventBus } from '../event-bus.js';
import axios from 'axios';

export default {
  name: 'Collect',
  data: function() {
    return {
      statusDatabase: false,
      statusMarca: false,
      statusCarro: false,
      statusDetalhe: false
    }
  },
  methods: {
    startDatabase(event) {
      // disable button
      event.target.disabled = true;

      // request 
      axios
      .get('http://0.0.0.0:7002/migration/table-create')
      .then(() => {
        // enable next collect button
        this.statusDatabase = true;
      })
      .catch(e => {
        // alert error
        alert(e)
        // enable button
        event.target.disabled = false;
        // inform stop collecting
        EventBus.$emit('collect-stop');
      })
    },
    collectMarca(event) {
      // disable button
      event.target.disabled = true;

      // request 
      axios
      .get('http://0.0.0.0:7002/collect/marca')
      .then(() => {
        // enable next collect button
        this.statusMarca = true;
        // inform start collecting
        EventBus.$emit('collect-start');
        // inform stop collecting
        EventBus.$emit('collect-stop');
      })
      .catch(e => {
        // alert error
        alert(e)
        // enable button
        event.target.disabled = false;
        // inform stop collecting
        EventBus.$emit('collect-stop');
      })
    },
    collectCarro(event) {
      // disable button
      event.target.disabled = true;
      // inform start collecting
      EventBus.$emit('collect-start');

      // request 
      axios
      .get('http://0.0.0.0:7002/collect/carro')
      .then(() => {
        // enable next collect button
        this.statusCarro = true;
        // inform stop collecting
        EventBus.$emit('collect-stop');
      })
      .catch(e => {
        // alert error
        alert(e)
        // enable button
        event.target.disabled = false;
        // inform stop collecting
        EventBus.$emit('collect-stop');
      })
    },
    collectDetalhe(event) {
      // disable button
      event.target.disabled = true;
      // inform start collecting
      EventBus.$emit('collect-start');

      // request 
      axios
      .get('http://0.0.0.0:7002/collect/detalhe')
      .then(() => {
        // enable next collect button
        this.statusDetalhe = true;
        // inform stop collecting
        EventBus.$emit('collect-stop');
      })
      .catch(e => {
        // alert error
        alert(e)
        // enable button
        event.target.disabled = false;
        // inform stop collecting
        EventBus.$emit('collect-stop');
      })
    },
    copySqlToClipboard() {
      alert('copiado')
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
