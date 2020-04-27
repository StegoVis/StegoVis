import tornado.ioloop
import tornado.web
from EncodeHandler import EncodeHandler
from DecodeHandler import DecodeHandler
from ImageExtractor import ImageExtractor
from DataExtractor import DataExtractor

def make_app():
	return tornado.web.Application([
		(r"/encode", EncodeHandler),
		(r"/decode", DecodeHandler),
		(r"/extract_image", ImageExtractor),
		(r"/extract_data", DataExtractor)
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(14453)
	print ('listen 14453....')
	tornado.ioloop.IOLoop.current().start()