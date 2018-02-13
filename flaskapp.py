from flask import Flask, request, Response
app = Flask(__name__)

from flask import jsonify

# Exception classes to allow more expressive errors
class ExceptWithDescription(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['description'] = self.message
        return rv

@app.errorhandler(ExceptWithDescription)
def handle_exception_with_description(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



@app.route('/')
def hello_world():
	return 'usage /backglass?image_format=JPG&image_url=https%3A%2F%2Fs3.amazonaws.com%2Fscore_pics%2F1234%2FABCD.jpg'

# The following is ONLY needed to run locally, for the purpose of debugging.
#if __name__ == '__main__':
#	app.run()

@app.route('/backglass', methods = ['GET'])
def backglassIdentify():
	#api_key = request.headers.get('api-key')
	#print("api_key: {0}".format(api_key) )
	#if ( api_key != 'com.pindigoapp:18012601' \
	#	 and api_key != 'com.rakonza:18012600'):
	#	raise ExceptWithDescription('Access Denied', status_code=403)

	import tempfile
	folder = tempfile.mkdtemp()
	filename = "X"

	image_url = request.args.get('image_url')
	image_format = request.args.get('image_format')

	if not image_format:
		image_format = 'JPG'

	if ( image_format!='JPG' and image_format!='PNG' and image_formay!='any' ):
		raise ExceptWithDescription('image_format must be JPG, PNG, or any', status_code=400)


	import urllib
	urllib.urlretrieve( image_url, "{0}/{1}".format(folder, filename))

	import turicreate as tc
	data = tc.image_analysis.load_images(folder, format=image_format, with_path=True)

	# because there is no concurrency model in python, we can't build a model pool, or cache the loaded model.
	model = tc.load_model('/home/ubuntu/flaskapp/_backglass_v201_')

	sf = model.predict_topk(data, k=3)

	saPindigo = tc.SArray([ ])
	saPinside = tc.SArray([ ])
	saName = tc.SArray([ ])

	if ( sf.num_rows() == 1 ):
		c1 = sf[0]['class']
		l1 = c1.split(" | ")
		saPindigo = tc.SArray([ l1[0] ])
		saPinside = tc.SArray([ l1[1] ])
		saName = tc.SArray([ l1[2] ])
	if ( sf.num_rows() == 2 ):
		c1 = sf[0]['class']
		l1 = c1.split(" | ")
		c2 = sf[1]['class']
		l2 = c2.split(" | ")
		saPindigo = tc.SArray([ l1[0], l2[0] ])
		saPinside = tc.SArray([ l1[1], l2[1] ])
		saName = tc.SArray([ l1[2], l2[2] ])
	if ( sf.num_rows() == 3 ):
		c1 = sf[0]['class']
		l1 = c1.split(" | ")
		c2 = sf[1]['class']
		l2 = c2.split(" | ")
		c3 = sf[2]['class']
		l3 = c3.split(" | ")
		saPindigo = tc.SArray([ l1[0], l2[0], l3[0] ])
		saPinside = tc.SArray([ l1[1], l2[1], l3[1] ])
		saName = tc.SArray([ l1[2], l2[2], l3[2] ])

	sf = sf.add_column( saPindigo, 'pindigo_id')
	sf = sf.add_column( saPinside, 'pinside_id')
	sf = sf.add_column( saName, 'name')

	sf = sf.remove_column('class')
	sf = sf.remove_column('id')
	sf = sf.sort('probability', ascending=False)

	json_filename = "{0}/{1}.json".format(folder, filename)
	sf.export_json(json_filename)

	f = open(json_filename)
	json_text = f.read()
	f.close()

	import shutil
	shutil.rmtree(folder)

	return Response(json_text, status=200, mimetype='application/json')

