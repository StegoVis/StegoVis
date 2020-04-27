import axios from 'axios'
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'

export function extractUnderlyingData(row, imageFile, add_underlying_data) {
	// 向服务器端传递数据
	axios({
	  method: 'post',
	  url: '/extract_data',
	  data: imageFile,
	  timeout: 500000,
	  crossDomain: true
	})
	.then((res) => {
		console.log('res', res)
		add_underlying_data(row, res)
	  // update_data_attr(row, res)
	})
	.catch((err) => {
	  console.log('axios failed', err)
	});
}

export function extractInnerImage(row, docFile, add_underlying_image) {
	// 向服务器端传递数据
	axios({
	  method: 'post',
	  url: '/extract_image',
	  data: docFile,
	  timeout: 500000,
	  crossDomain: true
	})
	.then((res) => {
	  add_underlying_image(row, res)
	})
	.catch((err) => {
	  console.log('axios failed', err)
	});
}

export function sendData(image, render_host_image) {
	// 向服务器端传递数据
	axios({
	  method: 'post',
	  url: '/encode',
	  data: image,
	  timeout: 500000,
	  crossDomain: true
	})
	.then((res) => {
	  render_host_image(res)
	})
	.catch((err) => {
	  console.log('axios failed', err)
	});
}

export function decodeDataFromImage(fileUrl, updateExtractData) {
	console.log('fileUrl', fileUrl)
	axios({
	  method: 'post',
	  url: '/decode',
	  data: fileUrl,
	  timeout: 500000,
	  crossDomain: true
	})
	.then((res) => {
	  updateExtractData(res)
	})
	.catch((err) => {
	  console.log('axios failed', err)
	});
}

export function sendQRData(qrcode_data, render_host_image) {
	// 向服务器端传递数据
	axios({
	  method: 'post',
	  url: '/qrcode',
	  data: qrcode_data,
	  timeout: 500000,
	  crossDomain: true
	})
	.then((res) => {
	  render_host_image(res)
	})
	.catch((err) => {
	  console.log('axios failed', err)
	});
}
