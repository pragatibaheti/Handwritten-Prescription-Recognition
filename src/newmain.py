import os
import cv2
from WordSegmentation import wordSegmentation, prepareImg
from DataLoader import DataLoader, Batch
from Model import Model, DecoderType
from main import FilePaths
from SamplePreprocessor import preprocess

def main():
	fnCharList = '../model/charList.txt'
	fnAccuracy = '../model/accuracy.txt'
	fnTrain = '../data/'
	fnInfer = '../data/test2.png'
	fnCorpus = '../data/corpus.txt'
	"""reads images from data/ and outputs the word-segmentation to out/"""

	# read input images from 'in' directory
	imgFiles = os.listdir('../d/')
	model = Model(open(fnCharList).read(), DecoderType.BestPath, mustRestore=True)
	file=FilePaths()
	for (i,f) in enumerate(imgFiles):
		print('Segmenting words of sample %s'%f)
		
		# read image, prepare it by resizing it to fixed height and converting it to grayscale
		img = prepareImg(cv2.imread('../data/%s'%f), 50)
		
		# execute segmentation with given parameters
		# -kernelSize: size of filter kernel (odd integer)
		# -sigma: standard deviation of Gaussian function used for filter kernel
		# -theta: approximated width/height ratio of words, filter function is distorted by this factor
		# - minArea: ignore word candidates smaller than specified area
		res = wordSegmentation(img, kernelSize=25, sigma=11, theta=7, minArea=100)
		
		# write output to 'out/inputFileName' directory
		#if not os.path.exists('../out/%s'%f):
			#os.mkdir('../out/%s'%f)
		
		# iterate over all segmented words
		print('Segmented into %d words'%len(res))
		for (j, w) in enumerate(res):
			(wordBox, wordImg) = w
			(x, y, w, h) = wordBox
			batch = Batch(None, [img])
			(recognized, probability) = model.inferBatch(batch, True)
			print('Recognized:', '"' + recognized[0] + '"')
			print('Probability:', probability[0])	
			#cv2.imwrite('../out/%s/%d.png'%(f, j), wordImg) # save word
			cv2.rectangle(img,(x,y),(x+w,y+h),0,1) # draw bounding box in summary image
		
		# output summary image with bounding boxes around words
		#cv2.imwrite('../out/%s/summary.png'%f, img)


if __name__ == '__main__':
	main()