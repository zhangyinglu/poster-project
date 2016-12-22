#resize
import os
import os.path
import PIL
import imghdr
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#thir folder is custom
rootdir = "/home/ylzhang/DATA/posters"
basewidth = 200
outlier_data = []
for _,_,filenames in os.walk(rootdir):
        for filename in filenames:
                if (filename == '.') or (filename == '..'):
                        continue
                print(filename+' Start!')
                imgType = imghdr.what(os.path.join(rootdir,filename))
                if imgType == 'jpeg':
                        imgType = 'jpg'
                try:
                        img = Image.open(os.path.join(rootdir,filename))
                        #wpercent = (basewidth / float(img.size[0]))
                        #hsize = int((float(img.size[1]) * float(wpercent)))
                        img = img.resize((basewidth, 300), PIL.Image.ANTIALIAS)
                        img.save('/home/ylzhang/resizedposter/posters/'+filename+'_new.'+imgType)
                        print(os.path.join(rootdir,filename)+'Finished!')
                except Exception:
                        outlier_data.append(filename)
                        pass

print('Broken data ID: ')
print(outlier_data)
