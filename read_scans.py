import glob
import pydicom
import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import polygon

# https://www.raddq.com/dicom-processing-segmentation-visualization-in-python/
def sample_stack(stack, rows=6, cols=6, start_with=10, show_every=3, title = ''):
    fig,ax = plt.subplots(rows,cols,figsize=[12,12])
    if title != '':
        fig.suptitle(title)
    for i in range(rows*cols):
        ind = start_with + i*show_every
        ax[int(i/rows),int(i % rows)].set_title('slice %d' % ind)
        ax[int(i/rows),int(i % rows)].imshow(stack[:,:,ind],cmap='gray')
        ax[int(i/rows),int(i % rows)].axis('off')
    plt.show()

# SOURCE: http://aapmchallenges.cloudapp.net/forums/3/2/
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

def get_mask(contours, slices):
    z = [round(s.ImagePositionPatient[2],1) for s in slices]
    pos_r = slices[0].ImagePositionPatient[1]
    spacing_r = slices[0].PixelSpacing[1]
    pos_c = slices[0].ImagePositionPatient[0]
    spacing_c = slices[0].PixelSpacing[0]

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

def get_mask_combined(contours, slices):
    z = [round(s.ImagePositionPatient[2],1) for s in slices]
    pos_r = slices[0].ImagePositionPatient[1]
    spacing_r = slices[0].PixelSpacing[1]
    pos_c = slices[0].ImagePositionPatient[0]
    spacing_c = slices[0].PixelSpacing[0]

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


# read in CT volume
slice_directory = "C:/Users/19095/Documents/ECE228/NBIA_CT_Data/LCTSC/LCTSC-Test-S1-101/03-03-2004-08186/79262/*"
dcms = glob.glob(slice_directory)
slices = [pydicom.dcmread(dcm) for dcm in dcms]
CTvolume = np.stack([s.pixel_array for s in slices], axis = -1)
# visualize
sample_stack(CTvolume, title = 'CT images')

# read in segmentation file
seg_dir = "C:/Users/19095/Documents/ECE228/NBIA_CT_Data/LCTSC/LCTSC-Test-S1-101/03-03-2004-08186/1.000000-56597/1-1.dcm"
seg_file = pydicom.dcmread(seg_dir)
contours = read_structure(seg_file)

# generate masks
labels, colors = get_mask(contours, slices)             # individual organ labels
label, colors = get_mask_combined(contours, slices)     # combined label

# visualize labels
sample_stack(label, title = 'Combined')
sample_stack(labels[0], title = contours[0]['organ'])
sample_stack(labels[1], title = contours[1]['organ'])
sample_stack(labels[2], title = contours[2]['organ'])
sample_stack(labels[3], title = contours[3]['organ'])
sample_stack(labels[4], title = contours[4]['organ'])





# need to iterate though all volumes
# Store Masks somewhere



































