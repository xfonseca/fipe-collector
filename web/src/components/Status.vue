<template>
  <div id="status" v-if="showStatus">
    <h3>STATUS</h3>
    <table>
      <tbody>
        <tr class="general">
          <td class="brand"><b>GERAL</b></td>
          <td class="status">
            <div>
              <div class="status-car" v-bind:style="{ width: statusCarWidth + '%' }"> <span>{{statusCarWidth}}% modelo</span> </div>
              <div class="status-detail" v-bind:style="{ width: statusCarDetail + '%' }"> <span>{{statusCarDetail}}% detalhe</span> </div>
            </div>
          </td>
        </tr>
        <tr>
          <td class="brand">Fiat</td>
          <td class="status">
            <div>
              <div class="status-car" v-bind:style="{ width: statusCarWidth + '%' }"> <span>{{statusCarWidth}}% modelo</span> </div>
              <div class="status-detail" v-bind:style="{ width: statusCarDetail + '%' }"> <span>{{statusCarDetail}}% detalhe</span> </div>
            </div>
          </td>
        </tr>
        <tr>
          <td class="brand">Fiat</td>
          <td class="status">
            <div>
              <div class="status-car" v-bind:style="{ width: statusCarWidth + '%' }"> <span>{{statusCarWidth}}% modelo</span> </div>
              <div class="status-detail" v-bind:style="{ width: statusCarDetail + '%' }"> <span>{{statusCarDetail}}% detalhe</span> </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { EventBus } from '../event-bus.js';

export default {
  name: 'Status',
  data: function() {
    return {
      statusCarWidth: '80',
      statusCarDetail: '30',
      showStatus: false,
      isCollecting: false,
    }
  },
  methods: {
    updateStatus() {
      // check if is not already updating
      if (this.isCollecting == false) {
        // inform that now we are updating
        this.isCollecting = true;
        // request status for the first time
        this.getStatus();
        
        // keep updating status every 3 seconds
        var keepUpdating = setInterval(function() {
          // request status
          this.getStatus();

          // if it is not updating anymore, clear interval
          if (this.isCollecting == false) {
            clearInterval(keepUpdating);
          }
        }.bind(this), 3000);
      }
    },
    getStatus() {
      // request status
      alert('b');
    }
  },
  created() {
    EventBus.$on('collect-start', function () {
      // when the collect starts: show status div and start to update status
      this.updateStatus();
      this.showStatus = true;
    }.bind(this));
    EventBus.$on('collect-stop', function () {
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
    height: 40px;
  }
  table tbody tr.general {
    height: 90px;
  }
  table td.brand {
    width: 20%;
  }
  table tbody td.status {
    width: 80%;
    font-size: 11px;
    font-weight: bold;
    color: #ffffff;
  }
  table tbody tr.general td.status {
    font-size: 18px;
  }
  table tbody td.status span {
    margin-left: 5px;
  }
  table tbody td.status .status-car {
    background-color: blueviolet;
    height: 15px;
  }
  table tbody td.status .status-detail {
    background-color: yellowgreen;
    height: 15px;
  }
  table tbody tr.general td.status .status-car {
    background-color: blueviolet;
    height: 25px;
  }
  table tbody tr.general td.status .status-detail {
    background-color: yellowgreen;
    height: 25px;
  }
</style>
