<template>
	<div class="comment-view">
		<div class="comment-title-view">
			<CommentTitleView :title="CommentPanel">
			</CommentTitleView>
		</div>
		<div class="comment-content-view">
			<CommentContentView 
				:selectedRecord="selectedRecord"
				:commentObj="commentObj"
				:removeComment="removeComment"
				:changeDiscussionNum="changeDiscussionNum">
			</CommentContentView>
		</div>
	</div>
</template>
<script>
	import { mapState, mapMutations } from 'vuex';
	import CommentTitleView from './CommentTitleView.vue' 	
	import CommentContentView from './CommentContentView.vue'
	
	export default {
		name: "CommentView",
		props: {
			selectedRecord: {
				type: Array
			},
			removeComment: {
				type: Function
			},
			changeDiscussionNum: {
				type: Function
			}
		},
		data() {
			return {
				CommentPanel: "Comment Panel",
				commentObj: null
			}
		},
		components: {
			CommentTitleView, CommentContentView
		},
		computed: {
			...mapState([
		    ])
		},
		watch: {
			selectedRecord: function() {
				if ((typeof(this.selectedRecord) !== 'undefined') && (this.selectedRecord != null)) {
					this.commentObj = this.getCommentObj()
				} else {
					this.commentObj = null
				}
			}
		},
		mounted() {
		  let self = this
		},
		methods: {
			...mapMutations([
		    ]),
		    getCommentObj () {
		    	for (let i = 0; i < this.selectedRecord.length; i++) {
		    		if (this.selectedRecord[i].type === 'comment') {
		    			return this.selectedRecord[i].content
		    		}
		    	}
		    }
		}
	}
</script>
<style scoped lang="less">
  	@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
	.comment-view {
		position: absolute;
		left: 0%;
		top: 0%;
		width: 100%;
		height: 100%;
		.comment-title-view {
			position: absolute;
            top: 0%;
            height: 30px;
            left: 0%;
            width: 100%;
            border-bottom: @border-style;
		}
		.comment-content-view {
			position: absolute;
            top: 30px;
            bottom: 0%;
            left: 0%;
            width: 100%;
		}
	}
</style>