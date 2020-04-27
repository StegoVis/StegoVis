<template>
  <div class = "content">
    {{ content }}
  </div>
</template>

<script> 
import { mapState, mapMutations } from 'vuex';

export default {
  name: 'ContentView',
  props: {
    content: {
      type: String
    }
  },
  data() {
    return {
    }
  },
  created: function() {

  },
  beforeMount: function() {
  },
  mounted: function() {
    console.log('content', this.content)
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
  @border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
  .content {
    display: flex; 
    width: 100%; 
    height: 100%; 
    margin: auto; 
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    border-bottom: @border-style;
    white-space: pre-wrap;
  }
</style>
