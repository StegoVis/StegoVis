<template>
  <div class = "fab-main">
    <div class = "add-info">
      <span class="icon iconfont icon-plus"></span>
    </div>
    <div class = "info-name" v-for="infoObj in infoObjArray">
      {{ infoObj.name }}
    </div>
  </div>
</template>

<script> 
import { mapState, mapMutations } from 'vuex';
 // 
export default {
  name: 'FAB',
  props: {
  },
  data() {
    return {
      infoObjArray: [
        {
          name: 'data',
          type: 'data'
        },
        {
          name: 'dsl',
          type: 'code'
        }
      ]
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
  },  
  methods: {
  }
}
</script>

<style scoped lang="less">
  .fab-main {
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    padding: 0rem 0 2rem 2rem;
    .add-info {
      border-radius: 50px;
      background-color: #D2D2D2;
      padding: 8px 10px;
      box-shadow: 0 10px 10px rgba(0,0,0,.2), 0 4px 4px rgba(0,0,0,.15);
      cursor: pointer;
      margin-bottom: 1rem;
      .icon-plus {
        color: white;
        font-size: 1.5rem;
        &:hover{
          color: #eeeeee;
        }
      }
    }
    .info-name {
      width: 60px;
      padding: 8px 30px;
      border-radius: 50px 0px 0px 50px;
      background-color: #D2D2D2;
      box-shadow: 0 10px 10px rgba(0,0,0,.2), 0 4px 4px rgba(0,0,0,.15);
      cursor: pointer;
      margin-bottom: 1rem;
    }
  }
</style>
