<template>
  <div class="data-view-title">
    <span class="text">{{title}}</span>
    <el-divider direction="vertical"></el-divider>
    <span class="operation">
      <el-radio-group v-model="mode" @change="changeDisplayMode" size="mini">
        <el-radio-button label="table"></el-radio-button>
        <el-radio-button label="vis"></el-radio-button>
      </el-radio-group>
    </span>
  </div>
</template>

<script> 
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'DataTitle',
  props: {
    title: {
      type: String
    }
  },
  data() {
    return {
      mode: 'table'
    }
  },
  created: function() {

  },
  beforeMount: function() {

  },
  mounted: function() {

  },
  watch: {

  },
  computed: { 
    ...mapState([
    ]) 
  },  
  methods: {
    ...mapMutations([
      'UPDATE_DISPLAY_MODE'
    ]),
    changeDisplayMode: function() {
      
    }
  }
}
</script>
<style>
  .el-radio-button--mini .el-radio-button__inner {
    padding: 3px 4px !important;
  }
</style>
<style scoped lang="less">
  @border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
  .data-view-title {
    display: flex; 
    width: 100%; 
    height: 100%; 
    margin: auto; 
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    .el-divider--vertical {
      margin-top: 7px;
    }
    .iconfont {
      vertical-align: middle;
      margin-top: 4px;
      margin-bottom: 4px;
      font-size: 20px;
      &:hover {
        background: lightgray;
      }
    }
    .operation {
      position: absolute;
      margin-top: 4px;
      right: 5px;
    }
    .text {
       padding-left: 5px;
       margin-left: 0; /* Important */ 
       margin-right: 0; /* Important */ 
       margin-top: auto; /* Important */ 
       margin-bottom: auto; /* Important */ 
       text-align: left;
       font-weight: bold;
    }
  }
</style>
