<template>
	<div class="data-view">
		<div class="data-title-view">
			<DataTitleView :title="DataPanel">
			</DataTitleView>
		</div>
		<div class="data-content-view" ref="datacontent">
			<DataContentView
				:params="params"
				:dataColumn="dataColumn"
				:fixedAttr="fixedAttr"
				v-if="dataLoaded">
			</DataContentView>
		</div>
	</div>
</template>
<script>
	import { mapState, mapMutations } from 'vuex';
	import DataTitleView from './DataTitleView.vue' 	
	import DataContentView from './DataContentView.vue'
	import { loadData } from '@/Dataset/loadData.js'

	export default {
		name: "DataView",
		props: {
			brushRect: {
				type: Object
			},
			originalData: {
				type: String
			},
			updateTsvData: {
				type: Function
			}
		},
		data() {
			return {
				DataPanel: "Data Panel",
				dataLoaded: false,
				dataArray: [],
				csvData: {},
				dataColumn: [],
				fixedAttr: null,
				posColumn: ['x', 'y', 'dx', 'dy'],
				params: [],
				padding: 85,
				rowHeight: 30
			}
		},
		components: {
			DataTitleView, DataContentView
		},
		computed: {
			...mapState([
		    ])
		},
		watch: {
			brushRect: function() {
				this.updateFilteredData()
				this.params.data = this.filteredRawDataArray
			},
			originalData: function () {
				this.updateOriginalData()
			}
		},
		mounted() {
			if ((this.originalData == null) || (typeof(this.originalData) === 'undefined') || (this.originalData == "")) {
				return
			}
		  // $.when(csvDataDeferObj).then(function() {
		  //   self.dataLoaded = true
		  //   self.$forceUpdate()
		  // })
		  // loadData('data.csv').then(function(csvData) {
		  // 	self.csvData = csvData
		  // 	// let tsvData = d3.csvFormat(csvData)
		  // 	// self.updateTsvData(tsvData)
		  // 	let posColumn = self.posColumn
		  //   self.dataColumn = csvData.columns.filter(word => (posColumn.indexOf(word) === -1))
		  //   self.dataProcess() // 对于读取的csvData进行预处理
		  //   self.updateFilteredData() // 更新筛选的数据结果
		  //   self.initParams()
		  //   csvDataDeferObj.resolve()
		  // })
		},
		methods: {
			...mapMutations([
		    ]),
		    updateOriginalData: function() {
			  	let csvData = d3.csvParse(this.originalData);
			  	this.csvData = csvData
			  	let posColumn = this.posColumn
			  	this.dataColumn = csvData.columns.filter(word => (posColumn.indexOf(word) === -1))
			  	this.dataProcess() // 对于读取的csvData进行预处理
			  	this.updateFilteredData() // 更新筛选的数据结果
			  	this.initParams()
			  	console.log('csvData', csvData)
			  	this.dataLoaded = true
			  	this.$forceUpdate()
		    },
		    dataProcess: function() {
		    	let csvData = this.csvData
		    	let posColumn = this.posColumn
		    	let dataColumn = this.dataColumn
		    	let rawDataArray = [dataColumn]
		    	let posDataArray = [posColumn]
		    	for (let i = 0; i < csvData.length; i++) {
		    		let itemObj = csvData[i]
		    		let itemDataArray = []
		    		let itemPosArray = []
		    		for (let j = 0; j < dataColumn.length; j++) {
			    		let value = itemObj[dataColumn[j]]
			    		if (!isNaN(Number(value))) {
			    			itemDataArray.push(Number(value))
			    		} else {
			    			itemDataArray.push(value)
			    		}
			    	}
			    	for (let j = 0; j < posColumn.length; j++) {
			    		let value = itemObj[posColumn[j]]
			    		if (!isNaN(Number(value))) {
			    			itemPosArray.push(Number(value))
			    		} else {
			    			itemPosArray.push(value)
			    		}
			    	}
			    	rawDataArray.push(itemDataArray)
			    	posDataArray.push(itemPosArray)
		    	}
		    	this.rawDataArray = rawDataArray
		    	this.posDataArray = posDataArray
		    },
		    updateFilteredData: function () {
		    	let posColumn = this.posColumn
		    	let dataColumn = this.dataColumn
		    	let posDataArray = this.posDataArray
		    	let rawDataArray = this.rawDataArray
		    	if ((typeof(rawDataArray) === 'undefined') || (rawDataArray == null)) {
		    		return
		    	}
				let filteredRawDataArray = [dataColumn]
				let filteredPosDataArray = [posColumn]
		    	for (let i = 1; i < rawDataArray.length; i++) {
		    		let itemPos = posDataArray[i]
		    		let brushRect = this.brushRect
		    		if (!itemInRange2(itemPos, brushRect, posColumn)) {
		    			continue
		    		}
			    	let itemData = rawDataArray[i]
			    	filteredRawDataArray.push(itemData)
			    }
			    this.filteredRawDataArray = filteredRawDataArray
			    this.filteredPosDataArray = filteredPosDataArray
			    //	判断item是否在刷选的区域范围内
			    function itemInRange(itemPos, brushRect, posColumn) {
			    	let indexX = posColumn.indexOf('x'), indexDx = posColumn.indexOf('dx'),
			    		indexY = posColumn.indexOf('y'), indexDy = posColumn.indexOf('dy')
			    	// 将问题取反，不在brushRect的范围内
			    	let itemMinX = itemPos[indexX], itemMaxX = itemPos[indexX] + itemPos[indexDx],
			    		itemMinY = itemPos[indexY], itemMaxY = itemPos[indexY] + itemPos[indexDy]
			    	let brushMinX = brushRect.x, brushMaxX = brushRect.x + brushRect.dx,
			    		brushMinY = brushRect.y, brushMaxY = brushRect.y + brushRect.dy
			    	if ((brushMinY > itemMaxY) || (brushMaxY < itemMinY) || (brushMaxX < itemMinX) || (brushMinX > itemMaxX)) {
			    		return false
			    	}
			    	return true
			    }
			    //	判断item是否 #完全# 在刷选的区域范围内
			    function itemInRange2(itemPos, brushRect, posColumn) {
			    	let padding = 0.005
			    	let indexX = posColumn.indexOf('x'), indexDx = posColumn.indexOf('dx'),
			    		indexY = posColumn.indexOf('y'), indexDy = posColumn.indexOf('dy')
			    	// 将问题取反，不在brushRect的范围内
			    	let itemMinX = itemPos[indexX], itemMaxX = itemPos[indexX] + itemPos[indexDx],
			    		itemMinY = itemPos[indexY], itemMaxY = itemPos[indexY] + itemPos[indexDy]
			    	let brushMinX = brushRect.x, brushMaxX = brushRect.x + brushRect.dx,
			    		brushMinY = brushRect.y, brushMaxY = brushRect.y + brushRect.dy
			    	brushMaxX = (1 - brushMaxX) <= padding ? 1 : brushMaxX
			    	brushMaxY = (1 - brushMaxY) <= padding ? 1 : brushMaxY
			    	brushMinX = brushMinX <= padding ? 0 : brushMinX
			    	brushMinY = brushMinY <= padding ? 0 : brushMinY
			    	if ((brushMaxX >= itemMaxX) && (brushMaxY >= itemMaxY) && (brushMinX <= itemMinX) && (brushMinY <= itemMinY)) {
			    		return true
			    	}
			    	return false
			    }
		    },
		    initParams: function() {
		    	let filteredRawDataArray = this.filteredRawDataArray
		    	let contentHeight = this.$refs.datacontent.clientHeight
		  		let rowNum = Math.floor((contentHeight - this.padding) / this.rowHeight) - 1 // 去掉table的header占据的一行
		    	//	所有的column都支持排序
			    let sortArray = []
			    for (let i = 0; i < this.dataColumn.length; i++) {
			    	sortArray.push(i)
			    }
			    this.params = {
			    	data: filteredRawDataArray,
			    	header: 'row',
			    	enableSearch: true,
			    	pageSize: rowNum,
	        		pageSizes: [5, 10, 20, 50],
	        		pagination: true,
	        		height: contentHeight - this.padding,
	        		stripe: true,
	        		sort: sortArray
			    }
		    }
		}
	}
</script>
<style>
	.data-view {
		.flex-c-e {
			-webkit-justify-content: flex-start !important;
		}
		.vue-pagination {
			position: fixed !important;
		}
	}
</style>
<style scoped lang="less">
  	@border-style: 0.05rem solid rgba(180, 180, 180, 0.3);
	.data-view {
		position: absolute;
		left: 0%;
		top: 0%;
		width: 100%;
		height: 100%;
		.data-title-view {
			position: absolute;
            top: 0%;
            height: 30px;
            left: 0%;
            width: 100%;
            border-bottom: @border-style;
		}
		.data-content-view {
			position: absolute;
            top: 30px;
            bottom: 0%;
            left: 0%;
            width: 100%;
            overflow: auto;
		}
	}
</style>