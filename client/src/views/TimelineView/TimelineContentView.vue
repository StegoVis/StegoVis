<template>
  <div id="timeline-content" class="container" ref="container">
    <svg class="canvas" :style="canvasStyleObj">
      <g></g>
    </svg>
  </div>
</template>

<script>
  import { mapState, mapMutations } from 'vuex';

  export default {
    name: 'TimelineContent',
    data() {
      return {
        canvasWidth: 0,
        canvasHeight: 0,
        padding: {left: 0, right: 0, top: 0, bottom: 0},
        recordMargin: 60,
        recordRotationAngle: 45,
        canvasStyleObj: { width: '100%'},
        minDiscussionNum: 3
      }
    },
    props: {
      allRecordArray: Array,
      selectedRecord: Array,
      selectedRecordIndex: Number,
      discussionUpdate: Number
    },
    watch: {
        allRecordArray: function() {
          this.initCanvas()
          this.drawArrow()
          this.drawPoints()
        },
        selectedRecord: function() {
          if (this.selectedRecord == null) {
            this.unSelectAllRecord()
          }
        },
        selectedRecordIndex: function() {
          if (this.selectedRecordIndex == null) {
            return
          }
          this.unSelectRecord()
          this.selectRecord(this.selectedRecordIndex)
        },
        discussionUpdate: function() {
          this.updateDiscussionColor()
        }
    },
    computed: {
      ...mapState([
        ])
    },
    beforeMount: function() {
    },
    mounted: function() {
      this.initCanvas()
      this.drawArrow()
      this.drawPoints()
    },
    methods: {
      //  取消所有的探索记录的高亮
      unSelectAllRecord: function() {
        d3.select(this.$el)
          .select(".canvas")
          .select('g')
          .selectAll('.record-bg')
          .classed('selected', false)
      },
      getCommentTag: function(recordContentArray) {
        let commentObj = recordContentArray[recordContentArray.length - 2]
        if (commentObj.type === 'comment') {
          return commentObj.content.tag
        }
      },
      getCommentTitle: function(recordContentArray) {
        let commentObj = recordContentArray[recordContentArray.length - 2]
        if (commentObj.type === 'comment') {
          return commentObj.content.title
        }
      },
      getCommentContent: function(recordContentArray) {
        let commentObj = recordContentArray[recordContentArray.length - 2]
        if (commentObj.type === 'comment') {
          return commentObj.content.content
        }
      },
      initCanvas: function() {
        let padding = { left: 0.04, right: 0.04, top: 0.1, bottom: 0.1 }
        let clientWidth = this.$refs.container.clientWidth
        let clientHeight = this.$refs.container.clientHeight
        this.padding.top = clientHeight * padding.top
        this.padding.bottom = clientHeight * padding.bottom
        this.padding.left = clientWidth * padding.left
        this.padding.right = clientWidth * padding.right
        this.canvasHeight = clientHeight - this.padding.top - this.padding.bottom
        if (this.allRecordArray.length > 0) {
          let angleValue = this.recordRotationAngle / 180 * Math.PI
          let clientWidthRecord = this.canvasHeight / Math.tan(angleValue) + (this.allRecordArray.length - 1) * this.recordMargin + this.padding.left + this.padding.right
          clientWidth = clientWidth>clientWidthRecord?clientWidth:clientWidthRecord
        }
        this.canvasStyleObj.width = clientWidth + 'px'
        this.canvasWidth = clientWidth - this.padding.left - this.padding.right
        d3.select(this.$el)
          .select(".canvas")
          .select('g')
          .attr('transform', 'translate(' + this.padding.left + ',' + this.padding.top + ')')
      },
      drawArrow: function() {
        let lineLength = this.canvasWidth
        let lineStart = [0, this.canvasHeight]
        let lineEnd = [this.canvasWidth, this.canvasHeight];
        let markerBoxWidth = 8;
        let markerBoxHeight = 8;
        let refX = markerBoxWidth / 2;
        let refY = markerBoxHeight / 2;
        let markerWidth = markerBoxWidth / 2;
        let markerHeight = markerBoxHeight / 2;
        let arrowPoints = [[0, 0], [0, markerBoxHeight], [markerBoxWidth, markerBoxHeight / 2]];
        let arrowColor = '#999999'
        let arrowPathColor = '#999999'
        if ((this.allRecordArray == null) || (this.allRecordArray.length <= 0)) {
          return
        }  
        let svg = d3.select(this.$el)
          .select(".canvas")
          .select('g')
        svg.select('.arrow-marker').remove()
        svg.select('.arrow-path').remove()
        svg.append('defs')
          .append('marker')
          .attr('id', 'arrow')
          .attr('class', 'arrow-marker')
          .attr('viewBox', [0, 0, markerBoxWidth, markerBoxHeight])
          .attr('refX', refX)
          .attr('refY', refY)
          .attr('markerWidth', markerBoxWidth)
          .attr('markerHeight', markerBoxHeight)
          .attr('orient', 'auto-start-reverse')
          .append('path')
          .attr('class', 'arrow')
          .attr('d', d3.line() (arrowPoints))
          .attr('fill', arrowColor)
        svg.append('path')
          .attr('d', d3.line()([lineStart, lineEnd]))
          .attr('stroke', arrowPathColor)
          .attr('class', 'arrow-path')
          .attr('marker-end', 'url(#arrow)')
          .attr('fill', 'none')
      },
      updateDiscussionColor: function() {
        let self = this
        let minDiscussionNum = this.minDiscussionNum
        let svg = d3.select(this.$el)
          .select(".canvas")
          .select('g')
        let allRecordArray = this.allRecordArray
        if ((typeof(allRecordArray) == "undefined") || (allRecordArray == null)) {
          return
        }
        let discussionRange = d3.extent(allRecordArray, function(recordArray, index) {
          let discussionNum = self.getCommentDiscussion(recordArray)
          return discussionNum
        })
        let discussionColorRange = ['#fee0d2', '#de2d26']
        if (discussionRange[0] == 0) {
          discussionColorRange[0] = '#FFFFFF'
        }
        if (discussionRange[1] < minDiscussionNum) {
          discussionRange[1] = minDiscussionNum
        }
        var discussionColor = d3.scaleLinear()
          .domain(discussionRange)
          .range(discussionColorRange)
          .interpolate(d3.interpolateRgb)
        svg.selectAll('.record-discussion')
          .attr('fill', function(d, i) {
            // discussionColor
            let discussionNum = self.getCommentDiscussion(d)
            return discussionColor(discussionNum)
          })
          .style('opacity', function(d, i) {
            let discussionNum = self.getCommentDiscussion(d)
            if (discussionNum == 0) {
              return 0
            } 
          })
      },
      drawPoints: function() {
        let self = this
        let canvasHeight = this.canvasHeight
        let margin = this.recordMargin
        let angle = this.recordRotationAngle
        let angleValue = angle / 180 * Math.PI
        let minDiscussionNum = this.minDiscussionNum
        let svg = d3.select(this.$el)
          .select(".canvas")
          .select('g')
        let allRecordArray = this.allRecordArray
        if ((typeof(allRecordArray) == "undefined") || (allRecordArray == null)) {
          return
        }
        let discussionRange = d3.extent(allRecordArray, function(recordArray, index) {
          let discussionNum = self.getCommentDiscussion(recordArray)
          return discussionNum
        })
        let discussionColorRange = ['#fee0d2', '#de2d26']
        if (discussionRange[0] == 0) {
          discussionColorRange[0] = '#FFFFFF'
        }
        if (discussionRange[1] < minDiscussionNum) {
          discussionRange[1] = minDiscussionNum
        }
        var discussionColor = d3.scaleLinear()
          .domain(discussionRange)
          .range(discussionColorRange)
          .interpolate(d3.interpolateRgb)
        svg.selectAll('.comment-record').remove()
        svg.selectAll('.discussion-label').remove() 
        //  判断 allRecordArray 是否为null
        if ((this.allRecordArray == null) || (this.allRecordArray.length <= 0)) {
          return
        }  
        svg.append('text')
          .attr('class', 'discussion-label')
          .text('Discussion')
          .attr('alignment-baseline', 'middle')
          .attr('text-anchor', 'start')
          .attr('dx', '10px')
          .attr('dy', '0px')
        let commentRecord = svg.selectAll('.comment-record')
          .data(allRecordArray)
        let recordG = commentRecord.enter()
          .append('g')
          .attr('class', 'comment-record')
          .attr('id', function(d, i) {
            return 'comment-record-' + i
          })
          .attr('transform', function(d, i) {
            return 'translate(' + margin * i + ',' + canvasHeight + ')' + ' rotate(-' + angle + ')'
          })
        recordG.attr('transform', function(d, i) {
            return 'translate(' + margin * i + ',' + canvasHeight + ')' + ' rotate(-' + angle + ')'
          })
        recordG.exit().remove()
        let bgRectPadding = 2
        let bgRectPath = 'M '
        let pointArray = [
          [margin * Math.cos(angleValue) / 2 + bgRectPadding, margin * Math.sin(angleValue) / 2],
          [margin * Math.cos(angleValue) / 2 + canvasHeight / Math.sin(angleValue), margin * Math.sin(angleValue) / 2],
          [canvasHeight / Math.sin(angleValue) - margin * Math.cos(angleValue) / 2, -margin * Math.sin(angleValue) / 2],
          [-margin * Math.cos(angleValue) / 2 + bgRectPadding, -margin * Math.sin(angleValue) / 2],
          [margin * Math.cos(angleValue) / 2 + bgRectPadding, margin * Math.sin(angleValue) / 2]
        ]
        for (let i = 0; i < pointArray.length; i++) {
          if (i == 0) {
            bgRectPath = bgRectPath + + pointArray[i][0] + ' ' + pointArray[i][1]
            continue
          }
          bgRectPath = bgRectPath + ' L ' + pointArray[i][0] + ' ' + pointArray[i][1]
        }
        let recordBg = 
          recordG.append('path')
            .attr('class', 'record-bg')
            .attr('id', function(d, i) {
              return 'record-bg-' + i
            })
            .attr('d', bgRectPath)
            .on('click', selectRecord)
        let recordDis = 
          recordG.append('rect')
            .attr('class', 'record-discussion')
            .attr('x', -margin/2 + canvasHeight)
            .attr('width', margin)
            .attr('y', -canvasHeight-2.5)
            .attr('height', 5)
            .attr('transform', function(d, i) {
              return 'rotate(' + angle + ')'
            })
            .attr('fill', function(d, i) {
              // discussionColor
              let discussionNum = self.getCommentDiscussion(d)
              return discussionColor(discussionNum)
            })
            .style('opacity', function(d, i) {
              let discussionNum = self.getCommentDiscussion(d)
              if (discussionNum == 0) {
                return 0
              } 
            })
        let recordPoint = 
          recordG.append('circle')
            .attr('class', function(d, i) {
              let commentTag = self.getCommentTag(d)
              return 'record-point ' + commentTag
            })
            .attr('cx', 0)
            .attr('cy', 0)
            .attr('r', 5)
            .on('mouseover', this.highlightBg)
            .on('mouseout', this.unhighlightBg)
            .on('click', selectRecord)
        let recordCommentTitle = 
          recordG.append('text')
            .text(function(d, i) {
              return self.getCommentTitle(d)
            })
            .attr('class', 'comment-title')
            .attr('alignment-baseline', 'ideographic')
            .attr('text-anchor', 'start')
            .attr('dx', '18px')
            .attr('dy', '0px')
            .on('mouseover', this.highlightBg)
            .on('mouseout', this.unhighlightBg)
            .on('click', selectRecord)
        let recordCommentContent = 
          recordG.append('text')
            .text(function(d, i) {
              return self.getCommentContent(d).substring(0, 15) + '...'
            })
            .attr('alignment-baseline', 'hanging')
            .attr('text-anchor', 'start')
            .attr('dx', '18px')
            .attr('dy', '3px')
            .on('mouseover', this.highlightBg)
            .on('mouseout', this.unhighlightBg)
            .on('click', selectRecord)
        // 选择某个record
        function selectRecord(d, i) {
          let bgElement = d3.select(self.$el).select(".canvas").select('g').select('#record-bg-' + i)
          if (bgElement.classed('selected')) {
            self.unSelectRecord()
          } else {
            self.unSelectRecord()
            self.selectRecord(i)
          }
        }
      },
      //  返回comment对象
      getCommentDiscussion: function (recordArray) {
        for (let i = 0;i < recordArray.length;i++) {
          if (recordArray[i].type === 'comment') {
            let commentObj = recordArray[i]
            if ((commentObj != null) && (typeof(commentObj) !== "undefined")) {
              if ((typeof(commentObj.content.discussion) !== "undefined")) {
                return commentObj.content.discussion.length
              }
            }
            return 0
          }
        }
      },
      selectRecord: function(index) {
        let self = this
        let selectEvent = 'selectRecord'
        let selectedRecord = self.allRecordArray[index]
        d3.select(self.$el)
          .select(".canvas")
          .select('g')
          .select('#record-bg-' + index)
          .classed('selected', true)
        self.$emit(selectEvent, selectedRecord, index)
      },
      unSelectRecord: function() {
        let self = this
        let unSelectEvent = 'unselectRecord'
        d3.select(self.$el)
          .select(".canvas")
          .select('g')
          .selectAll('.record-bg')
          .classed('selected', false)
        self.$emit(unSelectEvent)
      },
      // 高亮背景
      highlightBg: function (d, i) {
          d3.select(this.$el)
            .select(".canvas")
            .select('g')
            .select('#record-bg-' + i)
            .classed('highlighted', true)
      },
      // 取消背景高亮
      unhighlightBg: function () {
          d3.select(this.$el)
            .select(".canvas")
            .select('g')
            .selectAll('.record-bg')
            .classed('highlighted', false)
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less">
#timeline-content {
  position: absolute;
  left: 0%;
  top: 0%;
  bottom: 0%;
  right: 0%;
  overflow-x: auto;
  .canvas {
    height: 100%;
    width: 100%;
    top: 0%;
    left: 0%;
    .comment-title {
      font-weight: bold;
    }
    .arrow {
      fill: #999999;
    }
    .arrow-path {
      stroke: #999999;
      stroke-width: 1px;
    }
    .record-bg {
      fill: white;
      opacity: 0;
      &:hover {
        fill: #f9d79c;
        opacity: 1;
      }
      &.highlighted {
        fill: #f9d79c;
        opacity: 1;
      }
      &.selected {
        stroke: #f2b14c;
        stroke-width: 1px;
        fill: #f9d79c;
        opacity: 1;
      }
    }
    .record-point {
      cursor: pointer;
    }
    .to-do {
      stroke: black;
      stroke-width: 1px;
      fill: #449dfc;
    }
    .finding {
      stroke: black;
      stroke-width: 1px;
      fill: #68c243;
    }
    .question {
      stroke: black;
      stroke-width: 1px;
      fill: #f47070;
    }
    .hypothesis {
      stroke: black;
      stroke-width: 1px;
      fill: #909399;
    }
  }
}
</style>
