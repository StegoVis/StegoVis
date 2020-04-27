<template>
  <div class="comment-container" ref="tableContainer" >
    <!-- <div class="comment-body"></div>
    <div class="comment-body"></div>
    <div class="comment-body"></div> -->
    <el-container v-if="commentObj!=null">
      <el-header>
        <div class="comment-info">
          <div class="comment-title">
            {{commentObj.title}}
          </div>
          <div class="comment-content">
            {{commentObj.content}}
          </div> 
          <div class="comment-operation">
            <span class="icon-comment-container">
              {{commentObj.discussion.length}}
              <span class="icon iconfont icon-comment"></span>
            </span>
            &nbsp; | &nbsp;
            <span class="icon iconfont icon-remove" @click="removeComment"></span>
            &nbsp; | &nbsp;
            <span> {{commentObj.date}} </span>
          </div>
        </div>        
      </el-header>
      <el-main class="discussion-container">
        <el-card class="discussion-body" v-for="(dissObj, index) in commentObj.discussion">
          {{dissObj.content}} 
          <div class="discussion-operation">
            <span class="icon iconfont icon-remove" @click="removeDiscussion(index)"></span>
            &nbsp; | &nbsp;
            <span> {{dissObj.date}} </span>
          </div>
        </el-card>
      </el-main>
      <el-footer>
        <el-input placeholder="Please input" v-model="newDiscussion" @change="updateDiscussion">
          <el-button slot="append" icon="el-icon-s-promotion" @click="sendDiscussion"></el-button>
        </el-input>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
  import { mapState, mapMutations } from 'vuex';

  export default {
    name: 'DataContent',
    data() {
      return {
        tableKey: 0,
        tableHeight: 0,
        newDiscussion: ""
      }
    },
    components: {
    },
    props: {
      commentObj: {
        type: Object,
        default: function() {
          return {
            title: "huahuahu",
            content: "ahahuahuhauhauhuahuahu",
            date: '2020-01-02',
            discussion: []
          }
        }
      },
      removeComment: {
        type: Function
      },
      changeDiscussionNum: {
        type: Function
      }
    },
    watch: {
      commentObj: function() {
        console.log('change comment object')
      }
    },
    computed: {
      ...mapState([
        ])
    },
    beforeMount: function() {
      //  初始化discussion
      this.newDiscussion = ""
      if (this.commentObj != null) {
        if (typeof(this.commentObj.title) === 'undefined') {
          this.commentObj.title = ""
        }
        if (typeof(this.commentObj.content) === 'undefined') {
          this.commentObj.content = ""
        }
        if (typeof(this.commentObj.date) === 'undefined') {
          this.commentObj.date = ""
        }
        if (typeof(this.commentObj.discussion) === 'undefined') {
          this.commentObj.discussion = []
        }
      }
    },
    mounted: function() {
    },
    methods: {
      sendDiscussion: function() {
        if (typeof(this.commentObj.discussion) === 'undefined') {
          this.commentObj.discussion = []
        }
        this.commentObj.discussion.push({
          content: this.newDiscussion,
          date: this.formatDate()
        })
        this.newDiscussion = ""
        this.changeDiscussionNum()
      },
      removeDiscussion: function(dissIndex) {
        if (typeof(this.commentObj.discussion) !== 'undefined') {
          this.commentObj.discussion.splice(dissIndex, 1)
        }
      },
      updateDiscussion: function() {
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
      }
    }
  }
</script>
<style lang="less">
.comment-container {
  .el-card__body {
    padding: 5px 10px !important; 
    word-wrap: break-word; 
    word-break: break-all;
    text-align: left;
    color: #999999;
  }
  .el-input__inner {
    padding: 0px 5px;
    border-radius: 0px;
  }
  .el-input-group__append {
    border-radius: 0px;
    padding: 0px 10px;
  }
  .el-icon-s-promotion {
    font-size: 20px;
  }
  .iconfont {
    cursor: pointer;
    padding: 1.5px;
  }
  .icon-remove {
    &:hover {
      background: #dddddd;
    }
  }
}
</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
.comment-container {
  position: absolute;
  left: 0%;
  top: 0%;
  bottom: 0%;
  right: 0%;
  flex-direction: column;
  .el-container {
    height: calc(100% - 2px);
    width: 100%;
    margin-top: 1px;
    margin-bottom: 1px;
    .el-header {
      text-align: center;
      padding: 5px 10px;
      background-color: white;
      text-align: left;
      height: 90px !important;
      // border-top: @border-style;
      // border-bottom: @border-style;
      .comment-info {
        height: 90px;
        overflow-y: auto;
        .comment-title {
          font-weight: bold;
        }
        .comment-title, .comment-content {
          line-height: 19px;
          word-wrap:break-word; 
          word-break:break-all;
          padding-bottom: 5px;
        }
        .comment-operation {
          display: flex;
          flex-direction: row-reverse;
          .icon-comment-container {
            color: steelblue;
            font-weight: bold;
          }
          .icon-remove {
            color: red;
            font-weight: bold;
          }
        }
      }
    }
    .el-footer {
      text-align: center;
      padding: 0px 0px;
      background-color: white;
      text-align: left;
      height: 40px !important;
      min-height: 40px !important;
      .el-input-group__append {
        padding: 0 10px !important;
      }
    }
    .el-main {
      height: calc(100% - 80px - 40px);
      padding: 0px;
      overflow-y: auto;
      padding: 0px 10px;
      .el-card {
        // margin-top: 5px;
        // margin-bottom: 5px;
        -webkit-box-shadow: none;
        border-radius: 0px;
        border: none;
        border-top: 1px solid #EBEEF5;        
        &:last-child {
          border-bottom: 1px solid #EBEEF5;
        }
        .discussion-operation {
          display: flex;
          flex-direction: row-reverse;
        }
      }
    }
  }
}
</style>
