<template>
  <div id="collect-buttons">
    <button :disabled="statusDatabase" v-bind:class="{ done: statusDatabase }" @click="startDatabase($event)">Start database</button>
    <button :disabled="!statusDatabase"  v-bind:class="{ done: statusMarca }" @click="collect($event, 'marca')">Collect "Marca"</button>
    <button :disabled="!statusMarca" v-bind:class="{ done: statusCarro }" @click="collect($event, 'carro')">Collect "Carro"</button>
    <button :disabled="!statusCarro" v-bind:class="{ done: statusDetalhe }" @click="collect($event, 'detalhe')">Collect "Detalhe"</button>
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
    // starts the database like a migration
    startDatabase(event) {
      // disable button
      event.target.disabled = true;

      // request 
      axios
      .get(process.env.APP_URL + '/migration/table-create')
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

    // collect data
    collect(event, what) {
      // disable button
      event.target.disabled = true;

      // inform start collecting
      EventBus.$emit('collect-start');
      
      // request 
      axios
      .get(process.env.APP_URL + '/collect/' + what)
      .then(() => {
        // enable next collect button
        if (what == 'marca') {
          this.statusMarca = true;
        } else if (what == 'carro') {
          this.statusCarro = true;
        } else if (what == 'detalhe') {
          this.statusDetalhe = true;
        }

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

    // copy sql of collected data to clipboard
    copySqlToClipboard() {
      window.open(process.env.APP_URL + "/dumping/dbmysql?startingId=0", "_blank");    
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
