<template>
  <div class="fab-view">
    <FAB :position="position"
          :bg-color-open="bgColorOpen"
          :actions="fabActions"
          :positionObj="positionObj"
          :mainTooltip="mainTooltip">
    </FAB>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import FAB from '../components/FAB.vue'

export default {
  name: 'FABView',
  components: {
    FAB
  },
  data() {
    return {
      position: 'top-right',
      bgColorOpen: '#778899',
      fabActions: [
        {
          name: 'data',
          icon: 'icon-data',
          color: '#ff7f00'
        },
        {
          name: 'code',
          icon: 'icon-code',
          color: '#377eb8'
        },
        {
          name: 'comments',
          icon: 'icon-comments',
          color: '#a65628'
        },
        {
          name: 'add',
          icon: 'icon-add',
          color: '#4daf4a'
        }
      ],
      positionObj: {
        leftRight: '2vw',
        topBottom: '8vh'
      },
      mainTooltip: 'click to show all the inner document'
    }
  },
  props: {
    
  },
  watch: {
      
  },
  computed: {
    ...mapState([
      ])
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
.fab-view {
  width: 100%;
  height: 100%;
}
</style>
