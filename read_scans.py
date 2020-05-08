
import os
import pydicom
import matplotlib.pyplot as plt
import numpy as np

# data_directory = 'C:/Users/19095/Documents/ECE228/NBIA_CT_Data/LCTSC/LCTSC-Test-S1-101/03-03-2004-08186/79262'


# scan_files = os.listdir(data_directory)

# for file in scan_files:
#     scan = data_directory + '/' + file
#     data = pydicom.dcmread(scan)
#     plt.imshow(data.pixel_array, cmap = plt.cm.bone)
#     plt.show()
    



# SOURCE: http://aapmchallenges.cloudapp.net/forums/3/2/
def read_structure(structure):
    contours = []
    for i in range(len(structure.ROIContourSequence)):
        contour = {}
        contour['color'] = structure.ROIContourSequence[i].ROIDisplayColor
        contour['number'] = structure.ROIContourSequence[i].ReferencedROINumber 
        contour['contours'] = [s.ContourData for s in structure.ROIContourSequence[i].ContourSequence]
        contours.append(contour)
    return contours


# def get_mask(contours, slices):
#     z = [s.ImagePositionPatient[2] for s in slices]
#     pos_r = slices[0].ImagePositionPatient[1]
#     spacing_r = slices[0].PixelSpacing[1]
#     pos_c = slices[0].ImagePositionPatient[0]
#     spacing_c = slices[0].PixelSpacing[0]


#     label = np.zeros_like(image, dtype=np.uint8)
#     for con in contours:
#         num = int(con['number'])
#         for c in con['contours']:
#             nodes = np.array(c).reshape((-1, 3))
#             assert np.amax(np.abs(np.diff(nodes[:, 2]))) == 0
#             z_index = z.index(nodes[0, 2])
#             r = (nodes[:, 1] - pos_r) / spacing_r
#             c = (nodes[:, 0] - pos_c) / spacing_c
#             rr, cc = polygon(r, c)
#             label[rr, cc, z_index] = num
    
#     colors = tuple(np.array([con['color'] for con in contours]) / 255.0)
    
#     return label, colors





segmentation_directory = "C:/Users/19095/Documents/ECE228/NBIA_CT_Data/LCTSC/LCTSC-Test-S1-101/03-03-2004-08186/1.000000-56597/1-1.dcm"

slice_directory = "C:/Users/19095/Documents/ECE228/NBIA_CT_Data/LCTSC/LCTSC-Test-S1-101/03-03-2004-08186/79262/1-001.dcm"


slices = [pydicom.dcmread(slice_directory)]

image = np.stack([s.pixel_array for s in slices], axis=-1)

contour_structure = pydicom.dcmread(segmentation_directory)
contours = read_structure(contour_structure)


# get_mask(contours,slices)


con = contours[0]
c = con['contours'][0]
nodes = np.array(c).reshape((-1, 3))

from mpl_toolkits import mplot3d
fig = plt.figure()
ax = plt.axes(projection='3d')

ax.scatter3D(nodes[:,0], nodes[:,1], nodes[:,2], cmap='Blues');
plt.show()





#             elif len(dcms) > 1:
#                 slices = [dicom.read_file(dcm) for dcm in dcms]
#                 slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
#                 image = np.stack([s.pixel_array for s in slices], axis=-1)
#                 label, colors = get_mask(contours, slices)



# slices = [dicom.read_file(dcm) for dcm in dcms]







