//	导入csv数据
export async function loadData (fileName, ) {
	//	全局的graph对象
	var data = await d3.csv(fileName)
	return data
}