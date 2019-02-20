<template>
  <div id="status" v-if="showStatus">
    <h3>STATUS</h3>
    <table>
      <tbody>
        <tr class="general">
          <td class="brand"><b>GERAL</b></td>
          <td class="status">
            <div>
              <div class="status-brand" v-bind:style="{ width: statusGeralMarca + '%' }"> <span>{{statusGeralMarca}}% marca</span> </div>
              <div class="status-car" v-bind:style="{ width: statusGeralCarro + '%' }"> <span>{{statusGeralCarro}}% carro</span> </div>
              <div class="status-detail" v-bind:style="{ width: statusGeralDetalhe + '%' }"> <span>{{statusGeralDetalhe}}% detalhe</span> </div>
            </div>
          </td>
        </tr>
        <tr v-bind:key="marcaIndex" v-for="(marca, marcaIndex) in statusMarca">
          <td class="brand">{{marca.marca_nome}}</td>
          <td class="status">
            <div>
              <div class="status-brand" v-bind:style="{ width: '100%' }"> <span>{{statusGeralMarca}}% marca</span> </div>
              <div class="status-car" v-bind:style="{ width: marca.status_carro + '%' }"> <span>{{marca.status_carro}}% carro</span> </div>
              <div class="status-detail" v-bind:style="{ width: marca.status_detalhe + '%' }"> <span>{{marca.status_detalhe}}% detalhe</span> </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { EventBus } from '../event-bus.js';
import axios from 'axios';

export default {
  name: 'Status',
  data: function() {
    return {
      statusCarWidth: '80',
      statusCarDetail: '30',
      showStatus: false,
      isCollecting: false,
      statusGeralMarca: 100,
      statusGeralCarro: 0,
      statusGeralDetalhe: 0,
      statusMarca: [],
    }
  },
  methods: {
    updateStatus() {
      // check if is not already updating
      if (this.isCollecting == false) {
        // inform that now we are updating
        this.isCollecting = true;

        // request status for the first time
        this.setStatus();
        
        // keep updating status every 3 seconds
        var keepUpdating = setInterval(function() {
          // request status
          this.setStatus();

          // if it is not updating anymore, clear interval
          if (this.isCollecting == false) {
            clearInterval(keepUpdating);
          }
        }.bind(this), 2000);
      }
    },
    setStatus() {
      // request status
      console.log('updating status');

      // request 
      axios
      .get(process.env.APP_URL + '/status/collect')
      .then(result => {
        this.statusGeralCarro = result.data.data.geral.carro
        this.statusGeralDetalhe = result.data.data.geral.detalhe
        this.statusMarca = result.data.data.marca
      })
      .catch(e => {
        // alert error
        console.log(e)
      })
    }
  },
  created() {
    EventBus.$on('collect-start', function () {
      console.log('collect start');
      // when the collect starts: show status div and start to update status
      this.updateStatus();
      this.showStatus = true;
    }.bind(this));
    EventBus.$on('collect-stop', function () {
      console.log('collect stop');
      // when the collect stops: stop to update status
      this.isCollecting = false;
    }.bind(this))
  }
}
</script>

<style scoped>
  h3 {
    margin: 50px 0 30px 0;
  }
  #status {
    margin-top: 50px;
  }
  table {
    margin: auto;
    width: 70%;
    text-align: left;
  }
  table tbody tr {
    height: 60px;
  }
  table tbody tr.general {
    height: 110px;
  }
  table td.brand {
    width: 20%;
  }
  table tbody td.status {
    width: 80%;
    font-size: 11px;
    font-weight: bold;
    color: #FFF;
  }
  table tbody tr.general td.status {
    font-size: 18px;
  }
  table tbody td.status span {
    margin-left: 5px;
  }
  table tbody td.status .status-brand {
    background-color: #2302f6;
    height: 15px;
  }
  table tbody td.status .status-car {
    background-color: #7b67f9;
    height: 15px;
  }
  table tbody td.status .status-detail {
    background-color: #d3ccfd;
    height: 15px;
  }
  table tbody tr.general td.status .status-brand {
    background-color: #2302f6;
    height: 25px;
  }
  table tbody tr.general td.status .status-car {
    background-color: #7b67f9;
    height: 25px;
  }
  table tbody tr.general td.status .status-detail {
    background-color: #d3ccfd;
    height: 25px;
  }
</style>
