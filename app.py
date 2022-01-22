from flask import Flask, render_template , request , jsonify
import cv2
from flask import send_file
from pdf2image import convert_from_path
import sys,os
import shutil

app = Flask(__name__)

def generateCard(mob):
	BASE_PATH = './output'
	userFolder = f"{BASE_PATH}/{mob}"
	userOutputFolder = f"{BASE_PATH}/{mob}/output"
	img = cv2.imread(userFolder + '/out.jpg')
	cropped_image = img[1044:1169, 1657:2499]
	resized = cv2.resize(cropped_image,(447,66))
	cv2.imwrite(f"{userFolder}/certificate.jpg",resized)

	cropped_image = img[1211:2394, 141:3316]
	resized = cv2.resize(cropped_image,(686,278))
	cv2.imwrite(f"{userFolder}/benificiary.jpg",resized)

	cropped_image = img[2369:3727, 199:3524]
	resized = cv2.resize(cropped_image,(947,387))
	cv2.imwrite(f"{userFolder}/vaccination.jpg",resized)
	cropped_image = img[3975:5634, 2422:4066]
	resized = cv2.resize(cropped_image,(305,304))
	cv2.imwrite(f"{userFolder}/qr.jpg",resized)

	l_img = cv2.imread("./sikho sikhao FRONT.jpg")
	s_img = cv2.imread(f"{userFolder}/benificiary.jpg")
	x_offset=13
	y_offset=257
	l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
	x_offset=697
	y_offset=244
	s_img = cv2.imread(f"{userFolder}/qr.jpg")
	l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
	x_offset=285
	y_offset=178
	s_img = cv2.imread(f"{userFolder}/certificate.jpg")
	l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
	cv2.imwrite(f'{userOutputFolder}/front.jpg',l_img)

	l_img = cv2.imread("./sikho sikhao back .jpg")
	x_offset=35
	y_offset=153
	s_img = cv2.imread(f"{userFolder}/vaccination.jpg")
	l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
	cv2.imwrite(f'{userOutputFolder}/back.jpg',l_img)
	shutil.make_archive(F'{mob}', 'zip', userOutputFolder)
	shutil.rmtree(userFolder)


############################################## THE REAL DEAL ###############################################
@app.route('/generate' , methods=['POST'])
def mask_image():
	# print(request.files , file=sys.stderr)
	name = request.form.get('username')
	print(name)
	BASE_PATH = './output'
	userFolder = f"{BASE_PATH}/{name}"
	userOutputFolder = f"{BASE_PATH}/{name}/output"
	os.mkdir(userFolder)
	os.mkdir(userOutputFolder)
	file = request.files['image'] ## byte file
	file.save(f"./output/{name}/"+file.filename);
	
	pages = convert_from_path(f"./output/{name}/"+file.filename, 500)
	for page in pages:
		page.save(f'./output/{name}/out.jpg', 'JPEG')
	generateCard(name)
	return render_template('./download.html')


@app.route('/download',methods=['POST'])
def download():
	name = request.form.get('username')
	print(name)
	return send_file(f'./{name}.zip', as_attachment=True)
##################################################### THE REAL DEAL HAPPENS ABOVE ######################################

@app.route('/delete',methods=['POST'])
def delete():
	name = request.form.get('username')
	print(name)
	os.remove(f'{name}.zip')
	return render_template('./index.html')

@app.route('/')
def home():
	return render_template('./index.html')

	
@app.after_request
def after_request(response):
    print("log: setting cors" , file = sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
	app.run(debug = True)
