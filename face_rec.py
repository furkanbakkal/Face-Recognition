#! /usr/bin/python
# - *- coding: utf- 8 - *-


from imutils.video import VideoStream #modülleri ekledik
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import RPi.GPIO as GPIO

#Python2 ile çalıştırın

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) #11. sıradaki GPIO17 çıkış pini olarak ayarladık

#Anlık ismi tanınmayan yüz olma ihtimaline karşı bilinmeyen olarak tanımladık
currentname = "Bilinmeyen"

#Model eğittiğimiz çıktı paketimizin ismi
encodingsP = "encodings.pickle"

#Yüz tespit için xml dosyası
cascade = "haarcascade_frontalface_default.xml"

#Yüz tanıma için xml dosyamızı ekliyoruz
print("[-] Sistem Yükleniyor...")
data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)
print("[-] Kamera Başlatılıyor...")

#vs = VideoStream(src=0).start() #USB kamera için
vs = VideoStream(usePiCamera=True).start() #Pi Cam için
time.sleep(2.0)

#FPS sayacı
fps = FPS().start()


while True:
	
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	# Kamera pencerimizi 500x500 olarak ayarladık.
	#Biraz küçük ama tam erkan yaparsak FPS çok düşük olur.
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #yüz tespiti için gri filtre 
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #yüz tanıma için renkli filtre

	
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)
	#Gri olarak yüz tespit yaptık.
	#scaleFactor=ölçek
	#minNeighbors = basitçe hassasiyet diyebiliriz

	
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
	#Çerçeve boyutları w,h

	#Bulunan yüzleri tespit ettik
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []
	
	GPIO.output(11,0) #Ledi söndür

	#Eğer yüz varsa...
	for encoding in encodings:
		#Bulunan yüzle tanımladığımız arasında eşleşme varsa baktık
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Bilinmeyen" #eşleşme yoksa tanımlı bir yüz değildir
		
		#eşleşme varsa...
		if True in matches:
			#eşleşen yüzün index değerlerini bulduk
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			#Eşlesen kısımlar üzerinde döngüye yaptıracağız.
			#En yüksek orana sahip yüzü bulacağız.
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			#Yüzde olarak en fazla benzeyen yüzü seçiyoruz
			name = max(counts, key=counts.get)
			
			#En yüksek oranlı kişinin ismini konsola yazdırdık.
			if currentname != name:
				currentname = name
				print(currentname)		
		
		names.append(name)
		
	#Tanınan veya bilinmeyen yüzün etrafına çerçeve çizdik ismini yazdık.
	for ((top, right, bottom, left), name) in zip(boxes, names):
		#Renkler Mavi-Yeşil-Kırmızı kodlamasındadır (ör. 128,128,0)
		
		cv2.rectangle(frame, (left, top), (right, bottom),
			(128, 128, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			.8, (128,128, 0), 2)
			
		if name=="Furkan": #Eğer özel bir isim bulduysa ledi yak.
			GPIO.output(11,1)

	#Canlı video penceresi
	cv2.imshow("Yüz Tanıma Sistemi", frame)
	key = cv2.waitKey(1) & 0xFF

	#w tuşu ile pencereyi kapatabilirsiniz.
	if key == ord("w"):
		break

	#FPS değerimizi güncelledik.
	fps.update()
fps.stop() #ve durdurduk.

print("[-] İşlem Süresi: {:.2f}".format(fps.elapsed()))
print("[-] Ortalama FPS: {:.2f}".format(fps.fps()))

#FPS'inizin çok düşük olması normal. Ben RPI4 4GB ile ortalama 3-4 FPS alıyorum.


cv2.destroyAllWindows()
vs.stop()
