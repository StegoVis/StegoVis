export function Dataset () {
	this.fileList = []
}

Dataset.prototype = {
	init: function() {
	},
	getFileList: function() {
		return this.fileList
	},
	
}