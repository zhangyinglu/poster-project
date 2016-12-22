import numpy as np
from sklearn.decomposition import PCA, IncrementalPCA
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
import os
import os.path
import json
from PIL import Image, ImageFile
from sklearn.preprocessing import MultiLabelBinarizer
ImageFile.LOAD_TRUNCATED_IMAGES = True


#thir folder is custom
i = 0
rootdir = "/home/ylzhang/DATA/info/jsons"
allmv_labels = []
dataX = np.empty((2048, 200*300*3))
class_mv = {'Drama':1, 'Comedy':2, 'Thriller':3, 'Action':4, 'Romance':5, 'Horror':6, 'Documentary':7, 'Crime':8, 'Adventure':9, 'Science Fiction':10, 'Family':11, 'Fantasy':12, 'Mystery':13, 'Animation':14, 'Music':15, 'Foreign':16, 'History':17, 'War':18, 'TV Movie':19, 'Western':20}
Ipca = IncrementalPCA(n_components = 2048, batch_size = 2048)
r_mean = 0.485886
y_mean = 0.429402
g_mean = 0.395833
for _,_,filenames in os.walk(rootdir):
        for filename in filenames:
                if (filename == '.') or (filename == '..'):
                        continue
                if not os.path.isfile('/home/ylzhang/resizedposter/mainPoster/'+filename[0:-5]+'_new.jpg'):
                        continue
                print(filename+' Start!')
                tmp_img = np.array(Image.open('/home/ylzhang/resizedposter/mainPoster/'+filename[0:-5]+'_new.jpg'),'f')
                if len(tmp_img.shape)<3:
                        continue
                with open('./DATA/info/jsons/'+filename, 'r') as f:
                        mv_labels = []
                        data = json.load(f)
                        labels = data['genres']
                        for label in labels:
                                mv_labels.append(class_mv[label])
                allmv_labels.append(mv_labels)
                #filename = filename[0:-5]+'_new.jpg'
                im = tmp_img
                im = im/255.0
                #print im.shape
                #tmp_test = im[:,:,0].reshape(1,200*300)
                #dataX[i,0:200*300] = tmp_test
                dataX[i,0:200*300] = im[:,:,0].reshape(1,200*300)-r_mean
                dataX[i,200*300:200*300*2] = im[:,:,1].reshape(1,200*300)-y_mean
                dataX[i,200*300*2:200*300*3] = im[:,:,2].reshape(1,200*300)-g_mean
                i = i+1
                if i == 2048:
                        Ipca.partial_fit(dataX)
                        i = 0
label = MultiLabelBinarizer().fit_transform(allmv_labels)
j = 0
data = np.empty((12000,2048))
tmp = np.empty((1,180000))
for _,_,filenames in os.walk(rootdir):
        for filename in filenames:
                if (filename == '.') or (filename == '..'):
                        continue
                if not os.path.isfile('/home/ylzhang/resizedposter/mainPoster/'+filename[0:-5]+'_new.jpg'):
                        continue
                print(filename+' Start!')
                tmp_img = np.array(Image.open('/home/ylzhang/resizedposter/mainPoster/'+filename[0:-5]+'_new.jpg'),'f')
                if len(tmp_img.shape)<3:
                        continue
                with open('./DATA/info/jsons/'+filename, 'r') as f:
                        mv_labels = []
                        data = json.load(f)
                        labels = data['genres']
                        for label in labels:
                                mv_labels.append(class_mv[label])
                allmv_labels.append(mv_labels)
                #filename = filename[0:-5]+'_new.jpg'
                im = tmp_img
                im = im/255.0
                #print im.shape
                #tmp_test = im[:,:,0].reshape(1,200*300)
                #dataX[i,0:200*300] = tmp_test
                tmp[0,0:200*300] = im[:,:,0].reshape(1,200*300)-r_mean
                tmp[0,200*300:200*300*2] = im[:,:,1].reshape(1,200*300)-y_mean
                tmp[0,200*300*2:200*300*3] = im[:,:,2].reshape(1,200*300)-g_mean
                data[j,:] = np.ravel(Ipca.transform(tmp))
                j = j+1
                print ((Ipca.transform(tmp)).shape)
                print (type(Ipca.transform(tmp)))
                break
#data=data[0:j,:]
dataX = []
tmp = []
print (data.shape)
