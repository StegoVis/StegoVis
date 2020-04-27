import tornado.ioloop
import tornado.web
import json
import pybase64
import io
import os
import sys
from PIL import Image
from os.path import abspath, dirname, join
from PyPDF4 import PdfFileReader
# from tornado_cors import CorsMixin

# class ImageExtractor(CorsMixin, tornado.web.RequestHandler):
	# CORS_ORIGIN = '*'
	# CORS_HEADERS = 'Content-Type'
	# CORS_METHODS = 'POST'
	
	# def set_default_headers(self):
	# 	self.set_header("Access-Control-Allow-Origin", "*")
	# 	self.set_header("Access-Control-Allow-Headers", "x-requested-with")
	# 	self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
	
class ImageExtractor(tornado.web.RequestHandler):
	def get(self):
		print("Hello, world")
		self.write("Hello, world")

	def post(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		requestBinary = self.request.body
		requestStr = requestBinary.decode()
		pdfdatahead, pdfdatacontent = requestStr.split(",")
		pdfdata = pybase64.b64decode(pdfdatacontent)
		pdfFileObj = PdfFileReader(io.BytesIO(pdfdata))
		print('pdfFileObj', pdfFileObj)
		imageArray = self.extractImageFromPdf(pdfFileObj)
		imageStrArray = []
		# processing the extracted image
		for i in range(len(imageArray)):
			buffered = io.BytesIO()
			# print(type(imageArray[i]))
			imageArray[i].save(buffered, format="PNG")
			imageStr = pybase64.b64encode(buffered.getvalue())
			imageStrArray.append(imageStr.decode("utf-8"))
		imageStrArrayStr = json.dumps(imageStrArray)
		self.write(imageStrArrayStr)

	def extractImageFromPdf(self, pdfFileObj):
		# r = PdfFileReader(io.BytesIO(pdfBinary))
		# print('r', r)
		# return
		# transfrom the string parameters to the json object
		# request_obj = json.loads(requestStr)
		# Image.open(io.BytesIO(pdfData))
		# imgdata = pybase64.b64decode(imgdatacontent)
		# hostImage = Image.open(io.BytesIO(imgdata))
		# r = PdfFileReader(io.BytesIO(pdfData))
		pageNo = 0
		imageArray = []
		while (pageNo < pdfFileObj.numPages):
			page = pdfFileObj.getPage(pageNo)
			if '/XObject' in page['/Resources']:
				xObject = page['/Resources']['/XObject'].getObject()
				for obj in xObject:
					print('obj', obj)
					if xObject[obj]['/Subtype'] == '/Image':
						size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
						data = xObject[obj].getData()
						if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
							mode = "RGB"
						else:
							mode = "P"
						if '/Filter' in xObject[obj]:
							if xObject[obj]['/Filter'] == '/FlateDecode':
								img = Image.frombytes(mode, size, data)
								imageArray.append(img)
								# img.save(obj[1:] + ".png")
							# elif xObject[obj]['/Filter'] == '/DCTDecode':
							# 	img = open(obj[1:] + ".jpg", "wb")
							# 	# imageArray.append(img)
							# 	img.write(data)
							# 	img.close()
							# elif xObject[obj]['/Filter'] == '/JPXDecode':
							# 	img = open(obj[1:] + ".jp2", "wb")
							# 	# imageArray.append(img)
							# 	img.write(data)
							# 	img.close()
							# elif xObject[obj]['/Filter'] == '/CCITTFaxDecode':
							# 	img = open(obj[1:] + ".tiff", "wb")
							# 	# imageArray.append(img)
							# 	img.write(data)
							# 	img.close()
						else:
							img = Image.frombytes(mode, size, data)
							imageArray.append(img)
			else:
				print("No image found.")
			pageNo += 1
		return imageArray
