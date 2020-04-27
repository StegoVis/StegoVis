<template>
	<div class="timeline-view">
		<div class="timeline-title-view">
			<TimelineTitleView :title="VisPanel" 
				:download="downloadImage"
				:playforward="playforward"
				:playbackward="playbackward"
				:changeRecordPlayState="changeRecordPlayState"
				:recordPlayState="recordPlayState">
			</TimelineTitleView>
		</div>
		<div class="timeline-content-view">
			<TimelineContentView 
				:allRecordArray="allRecordArray"
				:selectedRecord="selectedRecord"
				:selectedRecordIndex="selectedRecordIndex"
				:discussionUpdate="discussionUpdate"
				@selectRecord="selectRecord"
        		@unselectRecord="unselectRecord">
			</TimelineContentView>
		</div>
	</div>
</template>
<script>
	import { mapState, mapMutations } from 'vuex';
	import TimelineTitleView from './TimelineTitleView.vue' 	
	import TimelineContentView from './TimelineContentView.vue'
	
	export default {
		name: "TimelineView",
		props: {
			allRecordArray: {
				type: Array
			},
			selectedRecord: {
				type: Array
			},
			selectedRecordIndex: {
				type: Number
			},
			discussionUpdate: {
				type: Number
			},
			selectRecord: {
				type: Function
			},
			unselectRecord: {
				type: Function
			},
			playforward: {
				type: Function
			},
			playbackward: {
				type: Function
			},
			changeRecordPlayState: {
				type: Function
			},
			recordPlayState: {
				type: Boolean
			}
		},
		data() {
			return {
				VisPanel: "Timeline Panel"
			}
		},
		components: {
			TimelineTitleView, TimelineContentView
		},
		computed: {
			...mapState([
		    ])
		},
		watch: {
		},
		mounted() {
		  let self = this
		},
		methods: {
			...mapMutations([
		    ]),
			downloadImage: function() {

			}
		}
	}
</script>
<style scoped lang="less">
  	@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
	.timeline-view {
		position: absolute;
		left: 0%;
		top: 0%;
		width: 100%;
		height: 100%;
		.timeline-title-view {
			position: absolute;
            top: 0%;
            height: 30px;
            left: 0%;
            width: 100%;
            border-bottom: @border-style;
		}
		.timeline-content-view {
			position: absolute;
            top: 30px;
            bottom: 0%;
            left: 0%;
            width: 100%;
		}
	}
</style>