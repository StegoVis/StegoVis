<template>
  <div id="app">
    <el-menu
        class="el-menu-demo"
        mode="horizontal"
        background-color="#676767"
        text-color="#fff"
        :default-active="activeIndex"
        active-text-color="#ffd04b">
        <el-menu-item class='labelIcon' id="title">
          <router-link to="/" class="view-link">
            {{ appName }}
          </router-link>
        </el-menu-item>
        <el-menu-item index="upload" content="upload images">
          <router-link to="/upload" class="view-link">
            <i class="icon iconfont icon-upload"></i>
          </router-link>       
        </el-menu-item>
        <!-- <el-menu-item index="qr_code" content="embed data" @click="generateQRCode">
          <span class="el-dropdown-link">
            <i class="icon iconfont icon-Qr_code"></i>
          </span>
          <el-dropdown trigger="click" placement="bottom" :hide-on-click="false">
            <span class="el-dropdown-link">
              <i class="icon iconfont icon-Qr_code"></i><i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item class="block">
                <el-row>
                  <el-col :span="7">opacity</el-col>
                  <el-col :span="17">
                      <el-slider v-model="QRCodeOpacity" :step="1" :max="6" show-stops></el-slider>
                  </el-col>
                </el-row>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-menu-item> 
        <el-menu-item index="download_data" content="download image" @click="download_data">
          <i class="icon iconfont icon-Datadownload"></i>
        </el-menu-item> -->
    </el-menu>
    <div class = "content-wrapper1" v-loading="loading">
    </div>
    <div class = "content-wrapper">
        <keep-alive>
          <router-view></router-view>
        </keep-alive>
    </div>
<!--     <div class = "top-right-wrapper">
      <FABView></FABView>
    </div> -->
    <!--data dialog-->
    <!-- <el-dialog title="Upload Image" id="upload-image-dialog" 
      :visible.sync="uploadImageVisible">
      <UploadImage
        :imageDialogKey="imageDialogKey"
        :updateImagePreviewUrl="updateImagePreviewUrl"
        :decodeDataFromImage="decodeDataFromImage"
        :closeUploadImageDialog="closeUploadImageDialog"
        :updateImagePreviewDialogVisible="updateImagePreviewDialogVisible">
      </UploadImage>
    </el-dialog>
    <el-dialog :visible.sync="imagePreviewDialogVisible">
        <img width="100%" :src="dialogImageUrl" alt="">
    </el-dialog> -->
  </div>
</template>

<script>

// import UploadImage from './views/Dialog/UploadImage.vue'
import FABView from './views/FABView.vue'
// import BarChartSpec from './assets/spec/vega-lite/bar.vl.json'
// import population from './assets/spec/data/population.json'
// import barley from './assets/spec/data/barley.json'
import { sendQRData, decodeDataFromImage } from '@/communication/sender.js'
import { mapState, mapMutations } from 'vuex'
import { Dataset } from '@/Dataset/dataset.js'

export default {
  name: 'app',
  components: {
    FABView
  },
  data() {
    return {
      appName: "Information Hiding",
      operationArray: [],
      activeIndex: '',
      uploadImageVisible: false,
      imagePreviewDialogVisible: false,
      imageDialogKey: 0,
      // specFromImage: {},
      // dataFromImage: {},
      dialogImageUrl: '',
      QRCodeOpacity: 1,
    }
  },
  computed: {
    ...mapState([
      'displayMode',
      'loading'
    ])
  },
  watch: {
    displayMode: function() {
      console.log('displayMode', this.displayMode)
    }
  },
  methods: {
    iconClass(operation) {
      return 'icon-' + operation
    },
    upload_data: function() {
      this.uploadImageVisible = true
    },
    closeUploadImageDialog: function() {
      this.uploadImageVisible = false
    },
    updateImagePreviewDialogVisible: function() {
      this.imagePreviewDialogVisible = true
    },
    updateImagePreviewUrl: function(dialogImagePreviewUrl) {
      this.dialogImageUrl = dialogImagePreviewUrl
    },
    generateQRCode: function() {
      this.$refs.visview.generate_qr_code()
      // show loading page
    },
    generateQRCodeCallBack: function() {
      // hide loading page
    },
    decodeDataFromImage: function(file) {
      let ImageParameterObj = {
        image_uri: file.url
      }
      decodeDataFromImage(ImageParameterObj, this.updateExtractData)
    },
    updateExtractData: function(res) {
      if ((typeof(res) !== 'undefined') && (res != null)) {
          let resData = res.data
          console.log('resData', resData)
          if (typeof(resData) !== 'undefined') {
            this.promptMessage(resData.type, resData.message)
          }
          if (resData.type === 'success') {
            let extractStr = resData.extractStr
            console.log('extractStr', extractStr)
          } 
      }
    },
    download_data: function() {
    },
    sendQRData2Server: function() {
      let qrcode_data = "date precipitation temp_max temp_min wind weather 2012/01/01 0.0 12.8 5.0 4.7 drizzle 2012/01/02 10.9 10.6 2.8 4.5 rain 2012/01/03 0.8 11.7 7.2 2.3 rain 2012/01/04 20.3 12.2 5.6 4.7 rain 2012/01/05 1.3 8.9 2.8 6.1 rain 2012/01/06 2.5 4.4 2.2 2.2 rain 2012/01/07 0.0 7.2 2.8 2.3 rain 2012/01/08 0.0 10.0 2.8 2.0 sun 2012/01/09 4.3 9.4 5.0 3.4 rain 2012/01/10 1.0 6.1 0.6 3.4 rain 2012/01/11 0.0 6.1 -1.1 5.1 sun 2012/01/12 0.0 6.1 -1.7 1.9 sun 2012/01/13 0.0 5.0 -2.8 1.3 sun 2012/01/14 4.1 4.4 0.6 5.3 snow 2012/01/15 5.3 1.1 -3.3 3.2 snow"
      sendQRData(qrcode_data)
    },
    promptMessage: function(type, message) {
      this.$message({
        type: type,
        message: message
      })
    }
  },
  mounted: function() {
  },
  beforeMount: function() {
    let self = this
    window.sysDatasetObj = new Dataset()
  }
}
</script>

<style lang="less">
  #app {
    // 数据集的选择对话框
    #upload-image-dialog {
      .el-dialog {
        width: 70%;
        min-width: 400px;
        min-height: 400px;
        .el-dialog__header {
          text-align: left;
        }
      }
      .el-dialog__body {
        text-align: left;
      }
    }
    .circular {
      height: 8rem !important;
      width: 8rem !important;
    }
  }
  .el-dropdown-menu.el-popper {
    min-width: 240px;
    padding: 5px 0;
    .el-dropdown-menu__item {
      padding: 0 8px;
      .el-slider {
        .el-slider__button {
          width: 12px;
          height: 12px;
        }
      }
    }
  }
</style>
<style scoped lang="less">
html {
  font-size: 100%;
}
@menu-height: 2.5rem;
@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  position: absolute;
  top: 0%;
  bottom: 0%;
  left: 0%;
  right: 0%;
  overflow: hidden;
  .el-menu.el-menu--horizontal {
    .el-menu-item {
      height: @menu-height;
      line-height: @menu-height;
    }
    .el-menu-item {
      border-bottom-color: rgb(84, 92, 100) !important;
      font-weight: bolder;
      font-size: 1rem;
      color: #dadada !important;
      padding: 0 10px;
      .view-link {
        text-decoration: None;
      }
      .icon {
        color: #dadada !important;
      }
      .el-icon-arrow-down.el-icon--right {
        color: #dadada !important;
      }
    }
    .el-divider--vertical {
      margin: 0 0;
    }
  }
  .labelIcon {
    font-size: 1rem;
  }
  .top-right-wrapper {
    right: 0vw;
    top: 8vh;
    z-index: 999;
    position: fixed;
  }
  .content-wrapper {
    position: absolute;
    top: @menu-height;
    left: 0%;
    bottom: 0%;
    right: 0%;
  }
  .content-wrapper1 {
    position: absolute;
    top: @menu-height;
    left: 0%;
    bottom: 0%;
    right: 0%;
  }
  .right-wrapper {
    .right-top-wrapper {

    }
    .timeline-wrapper {

    }
  }
}
</style>
