import glob
import pydicom
import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import polygon
import os


def sample_stack(stack, rows=6, cols=6, start_with=10, show_every=3, title = ''):
    fig,ax = plt.subplots(rows,cols,figsize=[12,12])
    if title != '':
        fig.suptitle(title)
    image_num = min(rows*cols, int(np.floor((stack.shape[2] - start_with) / show_every)))
    for i in range(image_num):
        ind = start_with + i*show_every
        ax[int(i/rows),int(i % rows)].set_title('slice %d' % ind)
        ax[int(i/rows),int(i % rows)].imshow(stack[:,:,ind],cmap='gray')
        ax[int(i/rows),int(i % rows)].axis('off')
    plt.show()

def read_structure(structure):
    contours = []
    for i in range(len(structure.ROIContourSequence)):
        contour = {}
        contour['color'] = structure.ROIContourSequence[i].ROIDisplayColor
        contour['number'] = structure.ROIContourSequence[i].ReferencedROINumber
        contour['contours'] = [s.ContourData for s in structure.ROIContourSequence[i].ContourSequence]
        contour['organ'] = structure.StructureSetROISequence[i].ROIName
        contours.append(contour)
    return contours

def get_mask(contours, data):
    z = [round(s.ImagePositionPatient[2],1) for s in data]
    pos_r = data[0].ImagePositionPatient[1]
    spacing_r = data[0].PixelSpacing[1]
    pos_c = data[0].ImagePositionPatient[0]
    spacing_c = data[0].PixelSpacing[0]

    labels = [np.zeros_like(CTvolume, dtype=np.uint8) for a in range(len(contours))]
    i=0
    for con in contours:
        num = int(con['number'])
        for c in con['contours']:
            nodes = np.array(c).reshape((-1, 3))
            assert np.amax(np.abs(np.diff(nodes[:, 2]))) == 0
            z_index = z.index(np.around(nodes[0, 2], 1))
            r = (nodes[:, 1] - pos_r) / spacing_r
            c = (nodes[:, 0] - pos_c) / spacing_c
            rr, cc = polygon(r, c)
            labels[i][rr, cc, z_index] = num

        i += 1
        colors = tuple(np.array([con['color'] for con in contours]) / 255.0)

    return labels, colors

def get_mask_combined(contours, data):
    z = [round(s.ImagePositionPatient[2],1) for s in data]
    pos_r = data[0].ImagePositionPatient[1]
    spacing_r = data[0].PixelSpacing[1]
    pos_c = data[0].ImagePositionPatient[0]
    spacing_c = data[0].PixelSpacing[0]

    label = np.zeros_like(CTvolume, dtype=np.uint8)
    for con in contours:
        num = int(con['number'])
        for c in con['contours']:
            nodes = np.array(c).reshape((-1, 3))
            assert np.amax(np.abs(np.diff(nodes[:, 2]))) == 0
            z_index = z.index(np.around(nodes[0, 2], 1))
            r = (nodes[:, 1] - pos_r) / spacing_r
            c = (nodes[:, 0] - pos_c) / spacing_c
            rr, cc = polygon(r, c)
            label[rr, cc, z_index] = num

        colors = tuple(np.array([con['color'] for con in contours]) / 255.0)

    return label, colors

plot_figs = False

# dealing with data's folder structure
d = 'C:/Users/19095/Documents/ECE228/NBIA_CT_Data/LCTSC - backup - Copy/'  # karndeep computer
d_out_data = 'C:/Users/19095/Documents/ECE228/ECE228_Project/Processed_data/data/'
d_out_label = 'C:/Users/19095/Documents/ECE228/ECE228_Project/Processed_data/label/'
fs = os.listdir(d)

for i,f in enumerate(fs):
    t = os.listdir(os.path.join(d,f))
    fs[i] = os.path.join(d, f,t[0])

# get sementation files and data folders
dirs = [] # list of lists: [segmentation directory, data directory]
for f in fs:
    ls = os.listdir(f)
    # only consider folders
    r = [] # remove files that will be ignored
    for l in ls:
        if not os.path.isdir(os.path.join(f,l)):
            r.append(l)
    for val in r:
        ls.remove(val)
    # store good directories
    if len(ls) == 2:
        if len(os.listdir(os.path.join(f,ls[0]))) == 1:
            dirs.append([os.path.join(f,ls[0]),os.path.join(f,ls[1])])
        else:
            dirs.append([os.path.join(f,ls[1]),os.path.join(f,ls[0])])
    else:
        raise ValueError("folder structure unexpected")


for i,D in enumerate(dirs):
        
    seg_dir = os.path.join(D[0],os.listdir(D[0])[0])
    print('loading data....\n', fs[i])
    data_dir = D[1] + '/*'

    ## read in CT volume ##
    dcms = glob.glob(data_dir)
    data = [pydicom.dcmread(dcm) for dcm in dcms]
    CTvolume = np.stack([d.pixel_array for d in data], axis = -1)

    #Threshold negative values and normalize
    CTvolume[CTvolume < 0] = 0
    CTvolume = CTvolume/np.amax(CTvolume)

    # visualize CT volume
    if plot_figs:
        sample_stack(CTvolume, title = 'CT images')
    
    #Save Data
    fname = d_out_data + str(i).zfill(3) + '_CTvolume.npy'
    np.save(fname,CTvolume)

    ## read in segmentation file ##
    seg_file = pydicom.dcmread(seg_dir)
    contours = read_structure(seg_file)

    # generate masks
    labels, colors = get_mask(contours, data)             # individual organ labels
    join_labels, colors = get_mask_combined(contours, data)     # combined label

    # visualize labels
    if plot_figs:
        sample_stack(join_labels, title = 'Combined Segmentation')
        sample_stack(labels[0], title = contours[0]['organ'])
        sample_stack(labels[1], title = contours[1]['organ'])
        sample_stack(labels[2], title = contours[2]['organ'])
        sample_stack(labels[3], title = contours[3]['organ'])
        sample_stack(labels[4], title = contours[4]['organ'])

    #Save Segmentations
    for j in range(len(labels)):
        fname = d_out_label + str(i).zfill(3) + '_' + contours[j]['organ'] + '.npy'
        np.save(fname,labels[j])

    # # visualize center frames of each volume and column wise plot
    # # notice different scanner treat area outside scanner differently
    # A = CTvolume.shape[2] / 2
    # A = int(np.floor(A))
    # plt.plot(CTvolume[:,:,A])
    # plt.show()
    # plt.imshow(CTvolume[:,:,A])
    # plt.show()




# references
# https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/
# SOURCE: http://aapmchallenges.cloudapp.net/forums/3/2/
