<template>
  <div
    ref="drawer-container"
    ondragstart="return false"
    class="drawer-container">
    <!-- 图片预览 -->
    <div class="drawer-img-box">
      <img
        class="drawer-img"
        :src="showImg?img:''">
    </div>
    <!-- 裁剪时半透明阴影 -->
    <div
      class="cropper-drag-box"
      :class="{ 'cropper-modal': isCrop }"
      :style="{ cursor: isToolbarShow && isCrop ? 'inherit' : 'crosshair' }"
      @mousedown.stop.prevent="onCropStart"
      @dblclick="onModalDoubleClick">
    </div>
    <!-- 截图框 -->
    <div
      v-show="isCrop"
      class="cropper-crop-box"
      @mouseenter="onCropBoxMouseEnter"
      @mousemove="onCropBoxMouseMove"
      @mouseleave="onCropBoxMouseLeave"
      :style="cropperBoxStyle">
      <!-- 截图框框图片 -->
      <div class="cropper-img">
        <img
          :src="img"
          :style="cropperImgStyle">
      </div>
      <!-- 截图框移动 -->
      <div
        class="cropper-move"
        @mousedown.stop.prevent="onCroperMove">
      </div>
      <!-- 截图宽高 -->
      <span
        class="cropper-info"
        :style="cropperInfoStyle">
        {{ cropperWidth }} × {{ cropperHeight }}
      </span>
      <!-- 截图框边框和点 -->
      <crop-border></crop-border>
      <!-- canvas画图 -->
      <div
        v-show="isToolbarShow"
        class="toolbar-container"
        :style="toolbarStyle">
        <toolbar
          ref="toolbar"
          :color.sync="toolbarColor"
          :fontSize.sync="toolbarFontSize"
          :lineWidth.sync="toolbarLineWidth"
          :toolStyle="toolStyle"
          :optionsStyle="optionsStyle"
          @drawType="onDrawType"
          @undoDraw="onUndoDraw"
          @saveDraw="onSaveDraw('saveImage')"
          @abandonDraw="onAbandonDraw"
          @completeDraw="onSaveDraw('copyImage')"></toolbar>
      </div>
      <!-- canvas涂鸦 -->
      <div v-show="showCanvas" class="full">
        <div id="container"></div>
      </div>
    </div>
  </div>
</template>

<script>
import CropBorder from './components/cropper-border.vue'
import Toolbar from './components/tool-bar'
import Painting from './core/painting'
import config from './config'
import Deferred from 'vue-deferred'

export default {
  name: 'vue-painting',
  props: {
    img: {
      type: String,
      default: ''
    },
    selectedRecord: {
      type: Array
    },
    currentRecordSave: {
      type: Boolean
    },
    styleObj: {
      type: Object
    },
    unselectRecord: {
      type: Function
    },
    updateBrushRect: {
      type: Function
    },
    saveImage: {
      type: Function
    },
    copyImage: {
      type: Function
    },
    quit: {
      type: Function
    }
  },
  components: {
    CropBorder,
    Toolbar
  },
  data () {
    return {
      isDrawShow: false,
      // 容器宽高
      container: {
        width: 0,
        height: 0,
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
        leftWidth: 0,
        topHeight: 0
      },
      // 图片宽高
      imgTrueWidth: 0,
      imgTrueHeight: 0,
      showImg: false,
      // 是否在截图
      isCrop: false,
      // 是否移动裁剪框
      isMove: false,
      // 裁剪框大小
      cropperWidth: 0,
      cropperHeight: 0,
      // 裁剪框相对位置坐标
      cropperOffsetX: 0,
      cropperOffsetY: 0,
      // 裁剪框绝对位置坐标
      cropperX: 0,
      cropperY: 0,
      // 开始裁剪时的坐标
      cropperOriginX: 0,
      cropperOriginY: 0,
      isToolbarShow: false,
      draw: null,
      image: null,
      // 是否显示canvas涂鸦
      showCanvas: false,
      // 颜色
      toolbarColor: undefined,
      // 字体大小
      toolbarFontSize: undefined,
      // 粗细
      toolbarLineWidth: undefined,
      // 是否显示工具栏
      toolbarOptionsShow: false,
      // TODO: 工具栏样式
      toolStyle: {},
      // TODO: 工具选项栏样式
      optionsStyle: {},
      drawConfig: {}
    }
  },
  computed: {
    // 裁剪框位置样式控制
    cropperBoxStyle () {
      return {
        width: `${this.cropperWidth}px`,
        height: `${this.cropperHeight}px`,
        transform: `translate3d(${this.cropperOffsetX}px, ${this.cropperOffsetY}px, 0)`
      }
    },
    // 裁剪框里面照片位置样式控制
    cropperImgStyle () {
      return {
        width: `${this.container.width}px`,
        height: `${this.container.height}px`,
        transform: `translate3d(-${this.cropperOffsetX}px, -${this.cropperOffsetY}px, 0)`
      }
    },
    // 显示像素位置样式控制
    cropperInfoStyle () {
      return {
        top: this.cropperOffsetY > 22 ? '-22px' : '0px'
      }
    },
    // 工具栏位置样式控制
    toolbarStyle () {
      let styleObj = {}
      let toolbarH = this.toolbarOptionsShow ? 77 : 39
      let toolbarW = 266
      let offsetY = this.container.height - this.cropperOffsetY - this.cropperHeight
      let offsetX = this.cropperOffsetX + this.cropperWidth
      let x = 0
      let y = 0
      // 如果底部没有高度了
      if (offsetY <= toolbarH) {
        // 但是上面有高度
        if (this.cropperOffsetY >= toolbarH) {
          y = `${-toolbarH}px`
        }
      } else {
        // 如果底部还有高度
        y = `${this.cropperHeight + 5}px`
      }
      // 如果左侧超出全屏，则让其不超出
      if (offsetX <= toolbarW) {
        x = `${toolbarW - offsetX}px`
      }
      Object.assign(styleObj, {
        transform: `translate3d(${x}, ${y}, 0)`
      })
      return styleObj
    }
  },
  created () {
    window.addEventListener('keydown', this.onEscKeyDown, false)
    this.image = new Image()
    this.image.onload = () => {
      this.imgTrueWidth = this.image.width
      this.imgTrueHeight = this.image.height
      this.showImg = true
    }
    this.image.src = this.img
  },
  mounted () {
    this.init()
    // 禁用右键菜单
    document.oncontextmenu = function (e) {
      e.cancelBubble = true
      e.returnValue = false
      return false
    }
  },
  methods: {
    onEscKeyDown (e) {
      if (e.keyCode !== 27) return
      // esc键退出
      this.$emit('quit')
    },
    // 初始化容器和canvas
    init () {
      const pos = this.$refs['drawer-container'].getBoundingClientRect()
      this.container = {
        width: pos.width,
        height: pos.height,
        left: pos.left,
        right: pos.right,
        top: pos.top,
        bottom: pos.bottom,
        leftWidth: pos.left + pos.width,
        topHeight: pos.top + pos.height
      }
      let container = document.getElementById(container)
      // this.$forceUpdate()
      // this.showCanvas = true
      // console.log('showCanvas', this.showCanvas)
      this.draw = new Painting({
        container: 'container'
      })
    },
    beforeRecover() {
      let cropConfig = {
        type: 'crop',
        range: {
          'x': 0,
          'y': 0,
          'dx': 23,
          'dy': 14
        }
      }
      this.setCropConfig(cropConfig)
      this.isToolbarShow = false
      this.onDrawType('pencil')
      // this.onModalDoubleClick()
    },
    // 蒙层双击取消裁剪
    onModalDoubleClick () {
      if (this.isCrop) {
        this.isCrop = false
        this.clearCanvas()
      }
      this.unselectRecord()
      let brushRect = { x: 0, y: 0, dx: 1, dy: 1 }
      this.updateBrushRect(brushRect)
    },
    // 开始裁剪截图
    onCropStart (e) {
      // 不是鼠标左键
      if (this.isCrop || e.which !== 1) {
        if (e.which === 3) {
          // 右键关闭
          this.isCrop ? (this.isCrop = false) : this.$emit('quit')
          this.clearCanvas()
        }
        return
      }
      this.clearCanvas()
      this.isCrop = true
      this.isToolbarShow = false
      window.addEventListener('mousemove', this.onResizeCropper)
      window.addEventListener('mouseup', this.onEndResizeCropper)
      this.cropperOriginX = this.cropperOffsetX = e.offsetX
      this.cropperOriginY = this.cropperOffsetY = e.offsetY
      this.cropperX = e.clientX
      this.cropperY = e.clientY
      this.cropperWidth = 0
      this.cropperHeight = 0
    },
    onCropBoxMouseEnter (e) {
      // console.log('e', e)
    },
    onCropBoxMouseMove(e) {
      // console.log('e', e)
    },
    onCropBoxMouseLeave(e) {
      // console.log('e', e)
    },
    // 创建截图框并计算大小
    onResizeCropper (e) {
      const posX = e.clientX - this.cropperX
      const posY = e.clientY - this.cropperY
      // 向右
      if (posX > 0) {
        if ((this.cropperOriginX + posX) <= this.container.width) {
          this.cropperWidth = posX
          this.cropperOffsetX = this.cropperOriginX
        }
      } else {
        // 向左
        if ((this.cropperOriginX - this.cropperWidth) >= 0) {
          this.cropperWidth = Math.abs(posX)
          this.cropperOffsetX = this.cropperOriginX - this.cropperWidth
        }
      }
      // 向下
      if (posY > 0) {
        if ((this.cropperOriginY + this.cropperHeight) <= this.container.width) {
          this.cropperHeight = posY
          this.cropperOffsetY = this.cropperOriginY
        }
      } else {
        // 向上
        if ((this.cropperOriginY - this.cropperHeight) >= 0) {
          this.cropperHeight = Math.abs(posY)
          this.cropperOffsetY = this.cropperOriginY - this.cropperHeight
        }
      }
    },
    // 裁剪结束
    onEndResizeCropper (e) {
      if (this.cropperWidth === 0 && this.cropperHeight === 0) {
        this.isCrop = false
      } else {
        this.isToolbarShow = true
        let brushRect = {
          x: this.cropperOffsetX / this.container.width,
          y: this.cropperOffsetY / this.container.height,
          dx: this.cropperWidth / this.container.width,
          dy: this.cropperHeight / this.container.height
        }
        this.updateBrushRect(brushRect)
      }
      window.removeEventListener('mousemove', this.onResizeCropper)
      window.removeEventListener('mouseup', this.onEndResizeCropper)
    },
    // 截图框拖拽移动
    onCroperMove (e) {
      // console.log('movestart')
      this.isMove = true
      window.addEventListener('mousemove', this.onMoveCropper)
      window.addEventListener('mouseup', this.onEndMoveCropper)
      this.cropperX = e.clientX
      this.cropperY = e.clientY
      this.cropperOriginX = this.cropperOffsetX
      this.cropperOriginY = this.cropperOffsetY
    },
    // 移动裁剪框
    onMoveCropper (e) {
      const posX = e.clientX - this.cropperX
      const posY = e.clientY - this.cropperY
      if (((this.cropperOriginX + posX) >= 0) && ((this.cropperOriginX + posX) <= this.container.width)) {
        this.cropperOffsetX = this.cropperOriginX + posX
      }
      if (((this.cropperOriginY + posY) >= 0) && ((this.cropperOriginY + posY) <= this.container.width)) {
        this.cropperOffsetY = this.cropperOriginY + posY
      }
    },
    // 结束移动裁剪框
    onEndMoveCropper () {
      this.isMove = false
      window.removeEventListener('mousemove', this.onMoveCropper)
      window.removeEventListener('mouseup', this.onEndMoveCropper)
      // this.updateBrushRect(brushRect)
      let brushRect = {
        x: this.cropperOffsetX / this.container.width,
        y: this.cropperOffsetY / this.container.height,
        dx: this.cropperWidth / this.container.width,
        dy: this.cropperHeight / this.container.height
      }
      this.updateBrushRect(brushRect)
    },
    setCropConfig (cropConfig) {
      console.log('cropConfig', cropConfig)
      if (cropConfig != null) {
        if (cropConfig.type == 'crop') {
          this.cropperOffsetX = cropConfig.range.x
          this.cropperOffsetY = cropConfig.range.y
          this.cropperWidth = cropConfig.range.dx
          this.cropperHeight = cropConfig.range.dy
          this.isCrop = true
          this.isToolbarShow = true
        }
      }
    },
    // 设置canvas背景及位置
    async setCanvas () {
      return new Promise((resolve, reject) => {
        this.showCanvas = true
        this.$nextTick(() => {
          this.draw.drawImage({
            x: 0,
            y: 0,
            image: this.image,
            width: this.container.width,
            height: this.container.height,
            offsetX: this.cropperOffsetX,
            offsetY: this.cropperOffsetY
          })
          resolve()
        })
      })
    },
    // 清除重置canvas
    clearCanvas () {
      this.showCanvas = false
      this.draw.clear()
    },
    // canvas涂鸦
    onDrawType (type) {
      if (!type) {
        this.toolbarOptionsShow = false
        if (!this.draw.layers.length) {
          this.clearCanvas()
        }
        return
      }
      if (!this.showCanvas) {
        this.drawConfig = this.draw.setDrawConfig({
          color: this.toolbarColor,
          fontSize: this.toolbarFontSize,
          lineWidth: config.lineWidth[this.toolbarLineWidth]
        })
        this.setCanvas()
      }
      this.toolbarOptionsShow = true
      this.drawConfig = this.draw.setDrawConfig({ type })
    },
    // 撤销操作
    onUndoDraw () {
      this.draw.undo()
    },
    // 保存操作
    async onSaveDraw (event) {
      try {
        this.showCanvas || await this.setCanvas()
        let cropConfig = {
            type: 'crop',
            range: {
              'x': this.cropperOffsetX,
              'y': this.cropperOffsetY,
              'dx': this.cropperWidth,
              'dy': this.cropperHeight,
              'width': this.container.width,
              'height': this.container.height
            }
        }
        let currentRecord = this.draw.saveCurrentRecord(cropConfig)
        let blobData = await this.draw.toImage(1)
        this.$emit(event, blobData, currentRecord)
      } catch (err) {
        throw err
      }
    },
    onAbandonDraw () {
      this.isCrop = false
      this.clearCanvas()
      this.$emit('quit')
    }
  },
  beforeDestroy () {
    window.removeEventListener('keydown', this.onEscKeyDown, false)
    this.showImg = false
    this.image = null
    this.draw.destroy()
  },
  watch: {
    currentRecordSave () {
      if (this.currentRecordSave) {
        // 清空画布以及剪裁区域
        this.onModalDoubleClick()
      }
    },
    toolbarColor (val) {
      this.drawConfig = this.draw.setDrawConfig({
        color: val
      })
    },
    img () {
      this.image = new Image()
      this.image.onload = () => {
        this.imgTrueWidth = this.image.width
        this.imgTrueHeight = this.image.height
        this.showImg = true
      }
      this.image.src = this.img
      let width = +this.styleObj.width.replace("px", "")
      let height = +this.styleObj.height.replace("px", "")
      let top = +this.styleObj.top.replace("px", "")
      let left = +this.styleObj.left.replace("px", "")
      this.container.width = width
      this.container.height = height
      this.container.left = left
      this.container.top = top
      this.container.leftWidth = left + width
      this.container.topHeight = top + height
    },
    styleObj () {
      const pos = this.$refs['drawer-container'].getBoundingClientRect()
      this.container = {
        width: pos.width,
        height: pos.height,
        left: pos.left,
        right: pos.right,
        top: pos.top,
        bottom: pos.bottom,
        leftWidth: pos.left + pos.width,
        topHeight: pos.top + pos.height
      }
    },
    toolbarFontSize (val) {
      this.drawConfig = this.draw.setDrawConfig({
        fontSize: val
      })
    },
    toolbarLineWidth (val) {
      this.drawConfig = this.draw.setDrawConfig({
        lineWidth: config.lineWidth[val]
      })
    },
    cropperOffsetX (newVal, oldVal) {
      if (newVal <= 0) {
        this.cropperOffsetX = 1
        if (!this.isMove) {
          this.cropperWidth = this.cropperOriginX
        }
        return
      }
      if (newVal + this.cropperWidth >= this.container.width) {
        this.cropperOffsetX = this.container.width - this.cropperWidth - 1
      }
    },
    cropperOffsetY (newVal, oldVal) {
      // console.log('Y', newVal)
      if (newVal <= 0) {
        this.cropperOffsetY = 1
        if (!this.isMove) {
          this.cropperHeight = this.cropperOriginY
        }
        return
      }
      if (newVal + this.cropperHeight >= this.container.height) {
        this.cropperOffsetY = this.container.height - this.cropperHeight - 1
      }
    },
    cropperWidth (newVal, oldVal) {
      // console.log('w', newVal)
      // if (this.cropperOffsetX <= this.cropperOriginX) return
      if (newVal + this.cropperOffsetX >= this.container.width) {
        this.cropperWidth = this.container.width - this.cropperOffsetX
      }
    },
    cropperHeight (newVal, oldVal) {
      // console.log('h', newVal)
      // if (this.cropperOffsetY <= this.cropperOriginY) return
      if (newVal + this.cropperOffsetY >= this.container.height) {
        this.cropperHeight = this.container.height - this.cropperOffsetY - 1
      }
    },
    isCrop (val) {
      if (!val) {
        let ins = this.$refs['toolbar']
        ins && (ins.activeType = '')
      }
    },
    selectedRecord () {
      let self = this
      if (this.selectedRecord != null) {
        recoverRecord()
      } else {
        //  清空对于画布的剪裁
        this.isCrop = false
        this.clearCanvas()
        this.draw.clear()
      }
      function recoverRecord() {
        self.draw.clear()
        self.isCrop = false
        self.clearCanvas()
        // 设定crop的参数
        let cropConfig = self.selectedRecord[self.selectedRecord.length - 1]
        self.setCropConfig(cropConfig)
        self.setCanvas()
        setTimeout(function() {
          self.draw.recoverRecord(self.selectedRecord)
        }, 300)
        // 设定绘制的图形
        self.showCanvas = true
      }
    }
  }
}
</script>

<style lang="less" scoped>
  .drawer-container {
    position: relative;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    z-index: 3;
  }

  .full {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    user-select: none;
    box-sizing: border-box;
  }

  .drawer-img-box {
    .full;
    overflow: hidden;

    .drawer-img {
      width: 100%;
      height: 100%;
      user-select: none;
    }
  }

  .cropper-drag-box {
    .full;
    cursor: crosshair;
  }

  .cropper-modal {
    .full;
    background: rgba(0, 0, 0, 0.5);
  }

  .cropper-crop-box {
    position: relative;
    .full;

    .cropper-img {
      display: block;
      overflow: hidden;
      width: 100%;
      height: 100%;
      outline: 1px solid #39f;
      outline-color: rgba(51, 153, 255, 0.75);
      user-select: none;
    }

    .cropper-info {
      font-family: sans-serif;
      position: absolute;
      left: 0px;
      min-width: 65px;
      text-align: center;
      color: white;
      line-height: 20px;
      background-color: rgba(0, 0, 0, 0.8);
      font-size: 12px;
    }

    .cropper-move {
      .full;
      cursor: move;
    }
  }

  .toolbar-container {
    position: absolute;
    right: 0;
    top: 0;
    z-index: 100;
  }

  .full #container {
    width: 100%;
    height: 100%;
  }

  #container {
    cursor: crosshair;
  }
</style>
<style>
  html, body {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
</style>
