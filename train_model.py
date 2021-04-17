#! /usr/bin/python
# - *- coding: utf- 8 - *-

from imutils import paths #Gerekli modülleri ekledik.
import face_recognition
import pickle
import cv2
import os

#Data klasörü içindeki veriler çekiliyor.
print("[-] Resimler işleniyor...")
imagePaths = list(paths.list_images("data"))

#Resimler ve isimler için dizi oluşturduk.
knownEncodings = []
knownNames = []


for (i, imagePath) in enumerate(imagePaths):
	#Resim ve isim dosyaları çekilip değerlendirme yapılıyor.
	print("[-] İşlenen resim {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	#Resim okuma, renk düzeni ayarları yapılandırması
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	#Resimlerdeki yüzler bulunuyor
	boxes = face_recognition.face_locations(rgb,
		model="hog")

	#Yüzler taranıyor
	encodings = face_recognition.face_encodings(rgb, boxes)

	for encoding in encodings:
		
		#Yüz isim eşleştirmesi yapılıyor
		knownEncodings.append(encoding)
		knownNames.append(name)

#Eğitilmiş dosya oluşturuluyor
print("[-] Tamamlanıyor...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
