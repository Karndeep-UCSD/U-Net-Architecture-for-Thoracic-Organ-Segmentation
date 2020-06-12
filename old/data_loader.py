import os
import numpy as np

# dealing with data's folder structure
d = 'C:/Users/19095/Documents/ECE228/NBIA_CT_Data/LCTSC/' 
fs = os.listdir(d)

for i,f in enumerate(fs):
    t = os.listdir(os.path.join(d,f))
    fs[i] = os.path.join(d, f,t[0])



data = []
heart = []
esophagus = []
lungL = []
lungR = []
spine = []
i=0
for f in fs:
    
    # print(os.listdir(os.path.join(d,f)))
    if i < 3:
        data_dir = os.path.join(d,f,'CTvolume.npy')
        heart_dir = os.path.join(d,f,'Heart.npy')
        esophagus_dir = os.path.join(d,f,'Esophagus.npy')
        lungL_dir = os.path.join(d,f,'Lung_L.npy')
        lungR_dir = os.path.join(d,f,'Lung_R.npy')
        spine_dir = os.path.join(d,f,'SpinalCord.npy')
        
        data.append(np.load(data_dir))
        heart.append(np.load(heart_dir))
        esophagus.append(np.load(esophagus_dir))
        lungL.append(np.load(lungL_dir))
        lungR.append(np.load(lungR_dir))
        spine.append(np.load(spine_dir))
        i+=1


data = np.concatenate(data, axis = -1)
heart = np.concatenate(heart, axis = -1)
esophagus = np.concatenate(esophagus, axis = -1)
lungL = np.concatenate(lungL, axis = -1)
lungR = np.concatenate(lungR, axis = -1)
spine = np.concatenate(spine, axis = -1)


    