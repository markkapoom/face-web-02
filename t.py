import os
import pathlib
import pickle
import shutil

import cv2
import pandas as pd

#object = pd.read_pickle(r'D:/test0002/encodings.pickle')
filename = 'encodings.pickle'
'''path = 'output/2jxTHNOXQ1.jpg'
image = cv2.imread(path)
cv2.imshow('image', image)
cv2.waitKey(0)'''
infile = open(filename,'rb')
new_dict = pickle.load(infile)
infile.close()
print(new_dict)
#os.chdir("data2/Khemanit Jamikorn t00002")
#print(os.path.abspath("file"))
import os
cp=pathlib.Path().absolute()
print(cp)
'''
d = "data2/cdgs"
for path in os.listdir(d):
    full_path = os.path.join(d, path)
    a = full_path
    print(full_path)
    source_dir = a
    target_dir = 'data/cdgs'
path2 = os.path.normpath(source_dir)
LL=path2.split(os.sep)
path3 = os.path.normpath(target_dir)
LL2=path3.split(os.sep)
print(LL,LL2)
for i, val in enumerate(LL):
    print (i, ",",val)
    if LL[i] == LL2[i]:
        break
    elif LL[i] != LL2[i]:
        target_dir += '/'+LL[2]
        file_names = os.listdir(source_dir)
        for file_name in file_names:
            shutil.move(os.path.join(source_dir, file_name), target_dir)
'''
print(os.environ)