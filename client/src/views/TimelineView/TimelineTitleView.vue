<template>
  <div class = "timeline-view-title">
    <span class = "text">{{title}}</span>
    <el-divider direction="vertical"></el-divider>
    <span class="icon iconfont icon-iosskipbackward" @click="playbackward"></span>
    <span class="icon iconfont" :class="{'icon-iosplay': !recordPlayState, 'icon-iospause': recordPlayState}" 
          @click="playRecord"></span>
    <span class="icon iconfont icon-iosskipforward" @click="playforward"></span>
    <span class="operation">
    </span>
  </div>
</template>

<script> 
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'DSLListTitle',
  props: {
    title: {
      type: String
    },
    download: {
      type: Function
    },
    playforward: {
      type: Function
    },
    playbackward: {
      type: Function
    },
    recordPlayState: {
      type: Boolean
    },
    changeRecordPlayState: {
      type: Function
    }
  },
  data() {
    return {
      mode: 'vis'
    }
  },
  created: function() {},
  beforeMount: function() {
  },
  mounted: function() {
  },
  watch: {
    displayMode: function() {
      //  更新在 visualization panel上选择的模式
      this.mode = this.displayMode
    }
  },
  computed: { 
    ...mapState([
      'displayMode'
    ]) 
  },  
  methods: {
    changeDisplayMode: function() {
      this.UPDATE_DISPLAY_MODE(this.mode)
    },
    ...mapMutations([
      'UPDATE_DISPLAY_MODE'
    ]),
    playRecord: function() {
      // this.recordPlayState = !this.recordPlayState
      this.changeRecordPlayState()
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
  .timeline-view-title {
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
