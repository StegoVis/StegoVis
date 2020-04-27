<template>
  <div id = 'data-dialog'>
    <div class = "content-container">
      <el-upload
        class="upload-demo"
        drag
        action="http://127.0.0.1:14452/"
        :http-request="getFile"
        :auto-upload="true"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :before-upload="onBeforeUpload"
        :on-success="handleUploadSuccess"
        :file-list="fileList"
        :show-file-list="false"
        multiple>
        <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
      </el-upload>
      <span class = "inner-label">Your Dateset:</span>
      <el-table
        ref="fileDataTable"
        :data="fileList"
        style="width: 100%;margin-bottom: 20px;"
        row-key="fileIndex"
        highlight-current-row
        @row-dblclick="dataTableRowDBClick"
        @row-click="dataTableRowClick"
        border
        :key="tableKey"
        default-expand-all>
        <el-table-column
          prop="fileIndex"
          label="FileIndex"
          sortable>
        </el-table-column>
        <el-table-column
          prop="fileName"
          label="Filename"
          sortable>
        </el-table-column>
        <el-table-column
          prop="thumbnail"
          label="Thumbnail"
          width="150">
          <template  slot-scope="scope">
            <img v-if="scope.row.type === 'Image'" class="image thumbnail" :src="scope.row.thumbnail_url">
            <span v-if="scope.row.type === 'Doc'">{{scope.row.thumbnail_url}}</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="date"
          label="Date"
          sortable>
        </el-table-column>
        <el-table-column
          prop="size"
          label="Size"
          sortable>
        </el-table-column>
        <el-table-column
          prop="data"
          label="Data"
          sortable>
        </el-table-column>
        <el-table-column
          prop="type"
          label="Type"
          width="100"
          :filters="[{ text: 'Doc', value: 'Doc' }, { text: 'Image', value: 'Image' }]"
          :filter-method="filterTag"
          filter-placement="bottom-end"
          align="center">
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.type === 'Doc' ? 'Image' : 'success'"
              disable-transitions>{{scope.row.type}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
            prop="action"
            label="Action"
            align="center"
            width="180">
            <template slot-scope="scope">
              <el-dropdown 
                trigger="click"
                @command="command => handleCommand(command, scope.row)"
                placement="bottom">
                <el-button type="info" class="action-button">
                  action<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu class="action-dropdown" slot="dropdown">
                  <el-dropdown-item icon="el-icon-document" command="extract">
                    Extract
                  </el-dropdown-item>
                  <el-dropdown-item icon="el-icon-close-notification" command="cancel">
                    Cancel
                  </el-dropdown-item>
                  <el-dropdown-item icon="el-icon-folder-delete" command="delete" divided>
                    Delete
                  </el-dropdown-item>
                  <el-dropdown-item icon="el-icon-close-notification" command="download">
                    Download
                  </el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </template>
          </el-table-column>
        </el-table>
        <div slot="footer" class="dialog-footer">
          <el-button @click="cancelSelection">Cancel</el-button>
          <el-button type="primary" @click="confirmSelection">OK</el-button>
        </div>
      </div>
  </div>
</template>

<script>
  import { mapState, mapMutations } from 'vuex'
  import { ImageCompressor } from 'image-compressor';
  import { extractUnderlyingData, extractInnerImage } from '@/communication/sender.js'

  export default {
    name: 'Upload',
    components: {
    },
    data() {
      return {
         fileList: [],
         tempSelection: null,
         tableKey: 0
        } 
    },
    watch: {
    },
    props: {
      initTreeDataName: {
        type: String
      }
    },
    created: function () {
    },
    beforeMount: function() {
      this.fileList = sysDatasetObj.getFileList()
      this.compressorSettings = {
        toWidth: 100,
        toHeight: 100,
        mimeType: 'image/png',
        mode: 'strict',
        quality: 1,
        vReverse: false,
        hReverse: false,
        speed: 'low'
      }
      this.ImageCompressor = new ImageCompressor
    },
    mounted: function() {
    },
    computed: {
      ...mapState([
          'userInfoName',
          'selectedItem'
        ])
    },
    methods: {
      ...mapMutations([
        'UPDATE_SELECTED_ITEM',
        'UPDATE_LOADING_MODE'
      ]),
      dataTableRowDBClick: function() {
      },
      dataTableRowClick: function(row) {
        let self = this
        let fileName = row.fileName
        if (self.tempSelection != null) {
          if ((self.tempSelection.fileName !== fileName) && (row.type === 'Image')) {
            //  设置当前选中的层次结构数据名称
            selectRow(row)
          } else {
            unSelectRow()
          }
        } else {
          selectRow(row)
        }
        //  选择点击的row
        function selectRow(row) {
          self.tempSelection = row
          self.$refs.fileDataTable.setCurrentRow(row)
        }
        //  取消选择当前点击的row
        function unSelectRow() {
          self.tempSelection = null
          self.$refs.fileDataTable.setCurrentRow()
        }
      },
      // setCurrent(fileName) {
      //   //  根据selectedDataset的属性值得到选择的数据集所处的位置
      //   for (let i = 0; i < this.fileList.length; i++) {
      //     let fileDataObj = this.fileList[i]
      //     if (fileDataObj.fileName === fileName) {
      //       let row = this.fileList[i]
            
      //       break
      //     }
      //   }
      // },
      handlePreview: function() {
      },
      handleRemove: function () {
      },
      onBeforeUpload: function(file) {
        let self = this
        const isJPG = file.type === 'image/jpeg'
        const isPNG = file.type === 'image/png'
        const isPDF = file.type === 'application/pdf'
        const imageCompressor = new ImageCompressor
        let compressorSettings = this.compressorSettings
        // 将文件大小换算为MB，且取小数点后两位
        let fileSize = file.size / 1024 / 1024
        fileSize = fileSize.toFixed(2)
        if ((!isJPG) && (!isPNG) && (!isPDF)) {
          let message = 'The uploaded image must be JPG or PNG format.'
          this.promptMessage('error', message)
              return false
        }
        // 这个文件在上传的文件列表中是不存在的
        if (this.fileList.map(function(e) { return e.name }).indexOf(file.name) !== -1) {
          let message = 'The uploaded image has existed.'
          this.promptMessage('error', message)
          return false
        }
        let fileObj = {}
        var reader = new FileReader()
        reader.onload = function () {
          fileObj.fileName = file.name
          fileObj.fileIndex = self.fileList.length + 1
          fileObj.rawFileUri = reader.result
          fileObj.date = self.formatDate()
          fileObj.size = fileSize + 'MB'
          if (isJPG || isPNG) {
            fileObj.type = 'Image'
          } else if (isPDF) {
            fileObj.type = 'Doc'
            fileObj.thumbnail_url = '-----'
            fileObj.data = '-----'
          }
          if (fileObj.type == 'Image') {
            //  对于图片的大小进行压缩，显式在文件表格中
            imageCompressor.run(reader.result, compressorSettings, function(compressedSrc) {
                fileObj.thumbnail_url = compressedSrc
                self.fileList.push(fileObj)
            })
          } else {
            self.fileList.push(fileObj)
          }
        }
        reader.readAsDataURL(file)
      },
      handleUploadSuccess: function () {
      },
      getFile: function () {
      },
      filterTag(value, row) {
        return row.type === value;
      },
      // cancel the selection
      cancelSelection: function() {
        this.tempSelection = null
        this.$refs.fileDataTable.setCurrentRow()
        this.UPDATE_SELECTED_ITEM(null)
      },
      confirmSelection: function () {
        if (this.tempSelection != null) {
          this.UPDATE_SELECTED_ITEM(this.tempSelection)
          this.$router.push('/')
        }
      },
      promptMessage: function(type, message) {
        this.$message({
          type: type,
          message: message
        })
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
      // 在表格的每一个条目中的方法
      handleCommand: function(command, row) {
        let self = this
        switch(command) {
          case 'extract':
             self.extractInfo(row)
             break;
          case 'cancel':
             self.cancelExtract(row)
             break;
          case 'delete':
             let deleteState = self.deleteFile(row)
             if (deleteState) {
               //  如果确认删除了元素，那么需要重新设定现有元素的fileIndex属性
               self.resetFileIndex()
             } 
             break
          case 'download':
             self.downloadFile(row)
             break
        } 
      },
      downloadFile: function(row) {
        let rawFileUri = row.rawFileUri
        if ((typeof(rawFileUri) !== 'undefined') && (rawFileUri != null)) {
          let rawImageObj = this.dataURLtoFile(rawFileUri, 'image.png')
          let imageLink = document.createElement("a")
          imageLink.href = URL.createObjectURL(rawImageObj)
          imageLink.download = rawImageObj.name
          imageLink.click()
        }
        let rawDataObj = row.rawDataObj
        if ((typeof(rawDataObj) !== 'undefined') && (rawDataObj != null)) {
          let dataLink = document.createElement("a")
          dataLink.download = rawDataObj.name
          dataLink.href = URL.createObjectURL(rawDataObj)
          dataLink.click()
        }
      },
      resetFileIndex: function () {
        for (let i = 0; i < this.fileList.length; i++) {
          this.fileList[i].fileIndex = i + 1
        }
      },
      extractInfo: function (row) {
        let self = this
        this.UPDATE_LOADING_MODE(true)
        if (row.type === 'Image') {
          extractUnderlyingData(row, row.rawFileUri, addUnderlyingData)
        } else if (row.type === 'Doc') {
          extractInnerImage(row, row.rawFileUri, addInnerImage)
        }
        // 在文件对象中修改数据属性
        function addUnderlyingData(row, res) {
          let underlyingData = res.data.extractStr
          let blob = new Blob([underlyingData], { type: 'text/json' })
          let underlyingDataObj = new File([blob], "test.json", {type: "text/json"})
          let fileSize = underlyingDataObj.size / 1024 / 1024
          fileSize = fileSize.toFixed(2) 
          row.data = fileSize + 'MB'
          row.rawDataStr = underlyingData
          row.rawDataObj = underlyingDataObj
          // 重新绑定更新视图
          self.tableKey = (self.tableKey + 1) % 2
          //  结束提取数据的计算
          self.UPDATE_LOADING_MODE(false)
        }
        //  在文件对象中增加新的图像对象
        function addInnerImage(row, res) {
          let underlyingImageArray = res.data
          for (let i = 0; i < underlyingImageArray.length; i++) {
            let innerImageUri = 'data:image/png;base64,' + underlyingImageArray[i]
            if (typeof(row.children) === 'undefined') {
              row.children = []
            }
            addImage2Children(row, innerImageUri, i)
          }
          //  结束提取图像的计算
          self.UPDATE_LOADING_MODE(false)
        }
        //  将图像增加到children数组中
        function addImage2Children(row, innerImageUri, index) {
          const imageCompressor = new ImageCompressor
          var innerImageObj = self.dataURLtoFile(innerImageUri, 'image.png')
          let fileSize = innerImageObj.size / 1024 / 1024
          fileSize = fileSize.toFixed(2)
          imageCompressor.run(innerImageUri, self.compressorSettings, function(compressedSrc) {
            let imageFileObj = {
              fileName: row.fileName.replace('.pdf', '') + '-img' + index + '.png',
              fileIndex: row.fileIndex + '-' + index,
              date: self.formatDate(),
              size: fileSize + 'MB',
              type: 'Image',
              // rawImageObj: innerImageObj,
              rawFileUri: innerImageUri
            }
            imageFileObj.thumbnail_url = compressedSrc
            row.children.push(imageFileObj)
            // 重新绑定更新视图
            self.tableKey = (self.tableKey + 1) % 2
          })
        }
      },
      //  将 uri装换为文件对象
      dataURLtoFile: function (dataurl, filename) {
        var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
            bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
            while(n--) {
                u8arr[n] = bstr.charCodeAt(n);
            }
        return new File([u8arr], filename, {type:mime});
      },
      cancelExtract: function (row) {

      },
      deleteFile: function (row) {
        let fileIndex = this.fileList.map(function(e) { return e.fileIndex }).indexOf(row.fileIndex)
        if (fileIndex !== -1) {
          // 删除选中的文件
          this.fileList.splice(fileIndex, 1)
          let message = "Delete the selected file successfully."
          this.promptMessage('success', message)
          return true
        } else {
          let message = "The file does not exist in the file list."
          this.promptMessage('error', message)
          return false
        }
      }
    }
  }
</script>
<style lang="less">
  #data-dialog {
    .el-table td, .el-table th {
      padding: 5px 0 !important;
    }
    .el-tag {
      padding: 0px 0px;
      line-height: 29px;
      height: 27px;
      width: 70px;
      border-radius: 0px;
    }
    .el-button--mini, .el-button--mini.is-round {
      padding: 3px 5px;
    }
    .el-upload {
      width: 100%;
      .el-upload-dragger {
        width: 100%;
        height: 100px;
        .el-upload__text {
          line-height: 100px;
          width: 100%;
        }
      }
    }
  }
</style>
<style scoped lang="less">
  #data-dialog {
    padding: 1rem 3rem 1rem 3rem;
      .inner-label {
        margin-top: 10px;
        margin-bottom: 10px;
        font-size: 1.2rem;
      }
    .content-container {
      margin-top: 10px;
      margin-bottom: 10px;
      text-align: left;
      overflow-y: auto;
    }
    .dialog-footer {
      text-align: right;
      .el-button {
        padding: 6px 10px;
        border-radius: 0px;
      }
    }
    .action-button {
      padding: 6px 20px;
      border-radius: 0px;
    }
  }
  .action-dropdown {
    text-align: center;
    min-width: 150px;
    border-radius: 0px;
  }
  .image.thumbnail {
    width: 100px;
    height: 100px;
  }
  .el-dropdown-menu__item--divided {
    margin-top: 0px;
    &:before {
      height: 0px;
      margin: 0px 0px;
      
    }
  }
</style>
