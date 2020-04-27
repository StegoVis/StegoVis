<template>
  <div id="data-content" class="container" ref="tableContainer" style="width: 1200px">
    <!-- <el-table
        ref="rawDataTable"
        :data="dataArray"
        style="width: 100%; margin-bottom: 20px;"
        row-key="fileIndex"
        highlight-current-row
        border
        :height="tableHeight"
        :key="tableKey"
        :stripe="true"
        default-expand-all>
        <el-table-column 
          v-for="item in dataColumns"
            :prop="item"
            :label="item"
            width="150"
            :fixed="item===fixedAttr"
            :sortable="true">
        </el-table-column>
    </el-table> -->
    <vue-table-dynamic 
      :params="params" ref="table">
    </vue-table-dynamic>
  </div>
</template>

<script>
  import { mapState, mapMutations } from 'vuex';
  import VueTableDynamic from 'vue-table-dynamic'

  export default {
    name: 'DataContent',
    data() {
      return {
        tableKey: 0,
        tableHeight: 0
      }
    },
    components: {
      VueTableDynamic
    },
    props: {
      dataArray: {
        type: Array
      },
      dataColumn: {
        type: Array
      },
      fixedAttr: {
        type: String
      },
      params: {
        type: Object
      }
    },
    watch: {
    },
    computed: {
      ...mapState([
        ])
    },
    beforeMount: function() {
      console.log('dataColumn', this.dataColumn)
      let tableColumnNum = this.dataColumn.length
      let tableWidth = tableColumnNum * 100
    },
    mounted: function() {
      this.tableHeight = this.$refs.tableContainer.clientHeight
      this.tableKey = (this.tableKey + 1) % 2
    },
    methods: {

    }
  }
</script>
<style>
  .vue-pagination.flex-c-e {
    -webkit-justify-content: flex-start;
  }
  .tools-search {
    width: 100%;
  }
</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
#data-content {
  position: absolute;
  left: 0%;
  top: 0%;
  bottom: 0%;
  right: 0%;
  overflow: auto;
}
</style>
