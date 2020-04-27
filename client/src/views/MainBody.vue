<template>
  <div class="main-body">
    <div class = "vis-panel" ref="visview">
      <PaintingView v-if="showPaintingView" 
        :styleObj="paintingImageStyleObject"
        :imageSrc="imageSrc"
        :unselectRecord="unselectRecord"
        :selectedRecord="selectedRecord"
        :updateBrushRect="updateBrushRect"
        :onCopyImage="onCopyImage"
        :hideData2Image="hideData2Image"
        :currentRecordSave="currentRecordSave">
      </PaintingView>
    </div>
    <div class = "right-wrapper">
      <div class = "right-top-wrapper">
        <div class = "data-wrapper" :style="{right: dataWrapperRight + '%'}">
          <DataView 
            :brushRect="brushRect"
            :originalData="originalData"
            :updateTsvData="updateTsvData">
          </DataView>
        </div>
        <div class = "comment-wrapper" :style="{left: (100 - dataWrapperRight) + '%'}">
          <CommentView 
            :selectedRecord="selectedRecord"
            :removeComment="removeComment"
            :changeDiscussionNum="changeDiscussionNum">
          </CommentView>
        </div>        
      </div>
      <div class = "timeline-wrapper">
        <TimelineView
          :allRecordArray="allRecordArray"
          :discussionUpdate="discussionUpdate"
          :selectRecord="selectRecord"
          :selectedRecord="selectedRecord"
          :selectedRecordIndex="selectedRecordIndex"
          :unselectRecord="unselectRecord"
          :playforward="playforward"
          :playbackward="playbackward"
          :recordPlayState="recordPlayState"
          :changeRecordPlayState="changeRecordPlayState">
        </TimelineView>
      </div>
    </div>
    <el-dialog
        width="30%"
        id="comment-dialog"
        title="Comment Dialog"
        :visible.sync="commentDialogVisible"
        append-to-body>
        <div id="comment-title-hint" class="comment-input-hint">Comment title<span class="nonempty">*</span>:</div>
        <el-input placeholder="Comment" v-model="currentCommentTitle" 
          :autofocus="false" @input="changeCommentTitle"></el-input>
        <div id="comment-content-hint" class="comment-input-hint">Comment content:</div>
        <el-input placeholder="Comment description" v-model="currentCommentContent" 
          :autofocus="false" @input="changeCommentContent"></el-input>
        <div class="comment-tag-container">
          <span class="comment-input-hint">Comment tags<span class="nonempty">*</span>:</span>
          <el-tag :effect="currentCommentTag!==commentObj.type?'plain':'dark'" class="comment-tag" :type="commentObj.color" v-for="commentObj in commentTypeArray" @click="changeCommentTag(commentObj)">
            {{commentObj.type}}
          </el-tag>
        </div>
        <div class="comment-warning-hint">{{currentCommentWarningHint}}</div>
        <span slot="footer" class="dialog-footer">
           <el-button @click="cancelSaveComment">Cancel</el-button>
           <el-button type="primary" @click="confirmSaveComment">Confirm</el-button>
        </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import cars from '../assets/spec/data/cars.json'
import PaintingView from './PaintingView/PaintingView.vue'
import TimelineView from './TimelineView/TimelineView.vue'
import DataView from './DataView/DataView.vue'
import CommentView from './CommentView/CommentView.vue'
import { sendData } from '@/communication/sender.js'

export default {
  name: 'MainBody',
  components: {
    PaintingView,
    TimelineView,
    DataView,
    CommentView
  },
  data() {
    return {
      dynamicLinkChartSpec: {
        "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
        "title": "cars",
        "background": "white",
        "vconcat": [
          {
            "mark": "point",
            "selection": {
              "brush": {
                "type": "interval",
                "init": {"x": [55, 160], "y": [13, 37]}
              }
            },
            "encoding": {
              "x": {"field": "Horsepower", "type": "quantitative"},
              "y": {"field": "Miles_per_Gallon", "type": "quantitative"},
              "color": {
                "condition": {"selection": "brush", "field": "Cylinders", "type": "ordinal"},
                "value": "grey"
              },
              "tooltip": {"field": "Name", "type": "nominal"}
            },
            "transform": [{"filter": {"selection": "click"}}]
          },
          {
            "mark": "bar",
            "selection": {
              "click": {"type": "single", "encodings": ["x"]}
            },
            "encoding": {
              "x": {
                "field": "Year", 
                "type": "nominal",
                "axis": {"labelAngle": -40}
              },
              "y": {"aggregate": "count", "type": "quantitative"},
              "color": {
                "condition": {
                  "selection": "click",
                  "value": "steelblue"
                },
                "value": "grey"
              }
            },
            "transform": [{"filter": {"selection": "brush"}}]
          }
        ]
      },
      showPaintingView: false,
      visviewWidth: 0,
      visviewHeight: 0,
      viewKey: 0,
      imageSrc: "",
      paintingImageStyleObject: {
        position: 'absolute',
        width: "0px",
        height: "0px",
        top: "0px",
        left: "0px"
      },
      allRecordArray: [],
      selectedRecord: null,
      selectedRecordIndex: null,
      csvDataset: null,
      brushRect: { x: 0, y: 0, dx: 1, dy: 1 }, // 默认情况下选中整个图片
      dataWrapperRight: 0,
      commentDialogVisible: false,
      currentCommentTitle: '',
      currentCommentContent: '',
      currentCommentWarningHint: '',
      commentTypeArray: [
        {type: 'question', color: 'danger'}, {type: 'finding', color: 'success'}, 
        {type: 'hypothesis', color: 'info'}, {type: 'to-do', color: ''}
      ],
      initCommentTag: 'question',
      currentCommentTag: 'question',
      currentRecord: null, 
      currentRecordSave: false,
      recordPlayState: false, 
      timeInterval: 3000,
      originalData: null,
      discussionUpdate: 1
    }
  },
  props: {
  },
  watch: { 
    selectedItem: function() {
      if (this.selectedItem != null) {
        this.initSelectedItem()
      }
    }
  },
  methods: {
    ...mapMutations([
      'UPDATE_LOADING_MODE'
    ]),
    initSelectedItem () {
      let self = this
      let rawFileUri = this.selectedItem.rawFileUri
      var imgObj = new Image()
      imgObj.onload = function() {
        self.initPaintingImage(this.width, this.height)
        self.imageSrc = rawFileUri
        console.log('self.selectedItem', self.selectedItem)
        if (typeof(self.selectedItem.rawDataStr) !== 'undefined') {
          if (self.selectedItem.rawDataStr !== "") {
            let rawDataContent = JSON.parse(self.selectedItem.rawDataStr)
            self.originalData = rawDataContent.data
            self.allRecordArray = rawDataContent.comment
          }
        }
        self.viewKey = (self.viewKey + 1) % 2
      }
      imgObj.src = rawFileUri
    },
    generateQRCodeCallBack: function() {
      // hide loading page
      this.loading = false
    },
    initPaintingView: function() {
      this.visviewWidth = this.$refs.visview.clientWidth
      this.visviewHeight = this.$refs.visview.clientHeight
      this.paintingImageStyleObject.width = this.visviewWidth + 'px'
      this.paintingImageStyleObject.height = this.visviewHeight + 'px'  
    },
    initPaintingImage (width, height) {
      let imgWidth = width
      let imgHeight = height
      let contentWidth = this.visviewWidth
      let contentHeight = this.visviewHeight - 30
      let widthRatio = contentWidth / imgWidth, 
        heightRatio = contentHeight / imgHeight
      let adjustContentHeight = 0, adjustContentWidth = 0,
        adjustContentTop = 0, adjustContentLeft = 0
      if (widthRatio > heightRatio) {
        // 图像的宽度一侧需要放大的更多 => 按照高度充满进行计算，调整容器的宽度
        adjustContentHeight = contentHeight
        adjustContentWidth = adjustContentHeight * imgWidth / imgHeight
        adjustContentTop = 0
        adjustContentLeft = (contentWidth - adjustContentWidth) / 2
      } else {
        // 图像的高度一侧需要放大的更多 => 按照宽度充满进行计算，调整容器的高度
        adjustContentWidth = contentWidth
        adjustContentHeight = adjustContentWidth * imgHeight / imgWidth
        adjustContentLeft = 0
        adjustContentTop = (contentHeight - adjustContentHeight) / 2
      }
      this.paintingImageStyleObject.width = adjustContentWidth + 'px'
      this.paintingImageStyleObject.height = adjustContentHeight + 'px'
      this.paintingImageStyleObject.top = adjustContentTop + 'px'
      this.paintingImageStyleObject.left = adjustContentLeft + 'px'
    },
    onCopyImage (blobFile, currentRecord) {
      if (currentRecord != null) {
        this.commentDialogVisible = true
        //  记录当前传递的record
        this.currentRecord = currentRecord
      }
    },
    selectRecord (record, index) {
      this.selectedRecord = record
      this.selectedRecordIndex = index
      if (record.length > 0) {
        let cropObj = record[record.length - 1]
        let brushRect = {
          'x': cropObj.range['x']/cropObj.range['width'],
          'dx': cropObj.range['dx']/cropObj.range['width'],
          'y': cropObj.range['y']/cropObj.range['height'],   
          'dy': cropObj.range['dy']/cropObj.range['height']     
        }
        this.updateBrushRect(brushRect)
        this.dataWrapperRight = 30
      }
    },
    unselectRecord () {
      let brushRect = { 'x': 0, 'dx': 1, 'y': 0, 'dy': 1 }
      this.updateBrushRect(brushRect)
      this.selectedRecord = null
      this.selectedRecordIndex = null
      this.dataWrapperRight = 0
      this.currentRecordSave = false
    },
    updateBrushRect (brushRect) {
      this.brushRect = brushRect
    },
    cancelSaveComment: function() {
      this.resetCommentSettings()
      this.commentDialogVisible = false
      this.currentRecordSave = false
    },
    confirmSaveComment: function() {
      if ((typeof(this.currentRecord) !== 'undefined') && (this.currentRecord != null)) {
        let commentObj = {
          type: 'comment',
          content: {
            title: this.currentCommentTitle,
            content: this.currentCommentContent,
            tag: this.currentCommentTag,
            date: this.formatDate(),
            discussion: []
          }
        }
        this.currentRecord.splice(this.currentRecord.length - 1, 0, commentObj)
        this.allRecordArray.push(this.currentRecord)
        this.currentRecordSave = true
      }
      this.resetCommentSettings()
      this.commentDialogVisible = false
    },
    removeComment: function() {
      this.allRecordArray.splice(this.selectedRecordIndex, 1)
      this.unselectRecord()
    },
    // 获取格式化的日期属性
    formatDate: function() {
      var d = new Date(),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear();
      if (month.length < 2) 
          month = '0' + month;
      if (day.length < 2) 
          day = '0' + day;
      return [year, month, day].join('-');
    },
    // 重置comment的类型
    resetCommentSettings: function() {
      this.currentCommentTitle = ""
      this.currentCommentContent = ""
      this.currentCommentTag = this.initCommentTag
    },
    changeCommentTitle: function() {
      let currentCommentTitle = this.currentCommentTitle
    },
    changeCommentContent: function() {
      let currentCommentContent = this.currentCommentContent
    },
    changeCommentTag: function(commentObj) {
      this.currentCommentTag = commentObj.type
    },
    // 向前播放
    playforward: function() {
      if ((this.selectedRecordIndex == null) || (typeof(this.selectedRecordIndex) === 'undefined')) {
        this.recordPlayState = false
        return
      }
      if (this.selectedRecordIndex >= (this.allRecordArray.length - 1)) {
        this.recordPlayState = false
        return
      }
      this.selectedRecordIndex += 1
      this.selectedRecord = this.allRecordArray[this.selectedRecordIndex]
    },
    // 向后播放
    playbackward: function() {
      if ((this.selectedRecordIndex == null) || (typeof(this.selectedRecordIndex) === 'undefined')) {
        this.recordPlayState = false
        return
      }
      if (this.selectedRecordIndex <= 0) {
        this.recordPlayState = false
        return
      }
      this.selectedRecordIndex -= 1
      this.selectedRecord = this.allRecordArray[this.selectedRecordIndex]
    },
    changeRecordPlayState: function() {
      let self = this
      let timeInterval = self.timeInterval
      self.recordPlayState = !self.recordPlayState
      if (self.recordPlayState) {
        //  开始播放Record
        setTimeout(startPlay, timeInterval)
      }
      function startPlay() {
        if(self.recordPlayState) {
          self.playforward()
          setTimeout(startPlay, timeInterval)
        }
      }
    },
    updateTsvData: function(originalData) {
      this.originalData = originalData
    },
    hideData2Image: function() {
      this.UPDATE_LOADING_MODE(true)
      let savedData = {
        'comment_data': {
          'comment': this.allRecordArray,
          'data': this.originalData
        },
        'image_uri': this.imageSrc
      }
      console.log('savedData', savedData)
      let savedDataStr = JSON.stringify(savedData)
      sendData(savedDataStr, this.updateHostImage)
    },
    updateHostImage: function(res) {
      let hostImageStr = res.data
      console.log('hostImageStr', hostImageStr)
      let hostImageUri = 'data:image/png;base64,' + hostImageStr
      this.selectedItem.rawFileUri = hostImageUri
      this.imageSrc = hostImageUri
      //  完成将数据隐藏到图片中的计算
      this.UPDATE_LOADING_MODE(false)
    },
    changeDiscussionNum: function() {
      this.discussionUpdate = (this.discussionUpdate + 1) % 2
    }
  },
  beforeMount: function() {
    let self = this
    // let csvDataDeferObj = $.Deferred()
    // $.when(csvDataDeferObj).then(function() {
    //   self.loading = false
    // })
    // loadData('data.csv').then(function(csvData) {
    //   console.log('csvdata', csvData)
    //   csvDataDeferObj.resolve()
    // })
    // this.initPaintingView()
  },
  mounted: function() {
    this.dynamicLinkChartSpec.data = {
      "values": cars
    }
    //  初始化视图的大小之后将showPaintingView设置为true
    this.initPaintingView()
    if (this.selectedItem != null) {
      this.initSelectedItem()
    }
    this.showPaintingView = true
  },
  computed: {
    ...mapState([
      'selectedItem',
      'loading'
    ])
  }
}
</script>
<style lang="less">
  #comment-dialog {
    z-index:10;
    .el-dialog__body {
      padding: 10px 20px !important;
    }
    #comment-content-hint {
      margin-top: 10px;
    }
    .comment-input-hint {
      font-weight: bold;
    }
    .comment-warning-hint {
      color: red;
    }
    .nonempty {
      color: red;
    }
    
    .comment-tag-container {
      margin-top: 5px;
      .comment-tag {
        margin: 5px;
        padding: 0 5px;
        cursor: pointer;
      }
    }
  }
</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
.main-body {
  width: 100%;
  height: 100%;
  .vis-panel {
    position: absolute;
    top: 0%;
    bottom: 0%;
    left: 0%;
    right: 50%;
    border-right: @border-style;
  }
  .right-wrapper {
    position: absolute;
    top: 0%;
    bottom: 0%;
    left: 50%;
    right: 0%;
    .right-top-wrapper {
      position: absolute;
      top: 0%;
      bottom: 25%;
      left: 0%;
      right: 0%;
      border-bottom: @border-style; 
      .data-wrapper {
        position: absolute;
        top: 0%;
        bottom: 0%;
        left: 0%;
        right: 0%; //30%
      }
      .comment-wrapper {
        position: absolute;
        top: 0%;
        bottom: 0%;
        left: 100%; //70%
        right: 0%;
        border-left: @border-style;
      }
    }
    .timeline-wrapper {
      position: absolute;
      top: 75%;
      bottom: 0%;
      left: 0%;
      right: 0%;
    }
  }
    // .dsl-panel {
    //   position: absolute;
    //   top: 0%;
    //   bottom: 0%;
    //   left: 50%;
    //   right: 25%;
    //   border-right: @border-style;
    // }
  .data-panel {
    position: absolute;
    top: 0%;
    bottom: 0%;
    left: 50%;
    right: 0%;
  }
}
</style>
