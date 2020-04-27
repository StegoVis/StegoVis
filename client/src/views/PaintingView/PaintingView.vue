<template>
	<div class = "painting-view">
		<div class = "painting-title-view">
			<PaintingTitleView 
				:title="PaintingPanel"
				:hideData2Image="hideData2Image">
			</PaintingTitleView>
		</div>
		<div class="painting-content-view" ref="content" v-if="showPaintingContent">
			<div class="painting-image-view"
				 :style="styleObj">
				<VuePainting
					v-show="(imageSrc!=='')&&(typeof(imageSrc)!='undefined')"
					:img="imageSrc"
	        		:selectedRecord="selectedRecord"
	        		:unselectRecord="unselectRecord"
	        		:updateBrushRect="updateBrushRect"
	 				:currentRecordSave="currentRecordSave"
	 				:styleObj="styleObj"
					@saveImage="onSaveImage"
	        		@copyImage="onCopyImage"
	        		@quit="onQuitDraw">
				</VuePainting>
			</div>
		</div>
	</div>
</template>
<script>
	import { mapState, mapMutations } from 'vuex';
	import VuePainting from '@/components/VuePainting/index.js'
	import PaintingTitleView from './PaintingTitleView.vue' 	

	export default {
		name: "VisView",
		props: {
		    styleObj: {
		    	type: Object
		    },
		    imageSrc: {
		    	type: String,
      			default: ""
		    },
		    selectedRecord: {
		      type: Array
		    },
		    unselectRecord: {
		      type: Function
		    },
		    hideData2Image: {
		      type: Function
		    },
		    onCopyImage: {
		      type: Function
		    },
		    updateBrushRect: {
		      type: Function
		    },
		    currentRecordSave: {
		      type: Boolean
		    }
		},
		data() {
			return {
				PaintingPanel: "Painting Panel",
				showPaintingContent: true,
				paintingImageStyleObject: {
				  position: 'absolute',
				  width: "0px",
				  height: "0px",
				  top: "0px",
				  left: "0px",
				  visibility: 'visible'
				},
				titleHeight: 30
			}
		},
		components: {
			PaintingTitleView, VuePainting
		},
		computed: {
			...mapState([
		      'selectedItem'
		    ])
		},
		watch: {
			selectedItem: function() {
			}
		},
		beforeMount() {
		},
		mounted() {
		},
		methods: {
			...mapMutations([
		    ]),
		    initPaintingContent () {
		    	this.contentWidth = this.$refs.content.clientWidth
	      		this.contentHeight = this.$refs.content.clientHeight
		    },
		    initPaintingImage (rawFileUri) {
		    	var imgObj = new Image()
				imgObj.src = rawFileUri
		    	let imgWidth = imgObj.width
		    	let imgHeight = imgObj.height 
		    	let contentWidth = this.contentWidth
		    	let contentHeight = this.contentHeight
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
	      		this.showPaintingContent = true
		    },
		    download () {
		    },
		    onQuitDraw () {
		    },
		    onSaveImage (blobFile) {
		        var a = document.createElement('a')
		        a.download = `painting-${+new Date}.png`
		        a.href = window.URL.createObjectURL(blobFile)
		        a.click()
		    }
		}
	}
</script>
<style scoped lang="less">
  	@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
	.painting-view {
		position: absolute;
		left: 0%;
		top: 0%;
		width: 100%;
		height: 100%;
		.painting-title-view {
			position: absolute;
            top: 0%;
            height: 30px;
            left: 0%;
            width: 100%;
            border-bottom: @border-style;
		}
		.painting-content-view {
			position: absolute;
            top: 30px;
            bottom: 0%;
            left: 0%;
            width: 100%;
            .painting-image-view {
            	position: absolute;
            }
		}
	}
</style>