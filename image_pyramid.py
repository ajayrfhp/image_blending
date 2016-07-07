def blend(img_2,img_1):
	'''
	Returns the blended image of 2 images with same size
	'''
	print 'hahahahalalal'
	img_blended = np.hstack((img_1_l,img_2_r))
	return img_blended

def laplacian_pyramid(img_1,n):
	'''
		Returns laplacian pyramid
	'''
	g_pyr = []
	l_pyr = []
	g_pyr.append(img_1.copy())
	for i in range(n-1):
		this_gpr = cv2.pyrDown(g_pyr[i],dstsize = (g_pyr[i].shape[1]/2, g_pyr[i].shape[0]/2))
		g_pyr.append(this_gpr)
	
	l_pyr.append(g_pyr[-1])
	for i in reversed(range(0,n-1)):
		next_up = cv2.pyrUp(g_pyr[i+1],dstsize = (g_pyr[i].shape[1],g_pyr[i].shape[0]))
		this_lpr = cv2.subtract(g_pyr[i],next_up)		
		l_pyr.append(this_lpr)

	return l_pyr


def laplacian_reconstruction(img_1,n):
	'''
		Reconstructs image using laplacian pyramid
	'''
	l_pyr = laplacian_pyramid(img_1,n)
	answer = l_pyr[0]
	for i in range(0,n-1):
		answer = cv2.pyrUp(answer,dstsize = (l_pyr[i+1].shape[1],l_pyr[i+1].shape[0]))
		answer = cv2.add(answer,l_pyr[i+1])
	return answer

		
def image_blend_pyramid(img_1,img_2,n):
	l_pyr_1 = laplacian_pyramid(img_1,n)
	l_pyr_2 = laplacian_pyramid(img_2,n)
	l_pyr_mixed = l_pyr_1
	print len(l_pyr_1)	
	for i in range(n):
		left_half = l_pyr_1[i][:,0:l_pyr_1[i].shape[1]/2,:]
		right_half =  l_pyr_2[i][:,l_pyr_2[i].shape[1]/2:,:]
		l_pyr_mixed[i] = np.concatenate((left_half,right_half),axis = 1)
		print left_half.shape,right_half.shape, l_pyr_mixed[i].shape
	answer = l_pyr_mixed[0]
	for i in range(0,n-1):
		answer = cv2.pyrUp(answer,dstsize = (l_pyr_mixed[i+1].shape[1],l_pyr_mixed[i+1].shape[0]))
		answer = cv2.add(answer,l_pyr_mixed[i+1])
	return answer
	

				
	
import cv2
import numpy as np

#img = cv2.imread('./images/obama.jpg')
#img_1 = img[:,0:img.shape[1]/2,:]
#img_2 = img[:,img.shape[1]/2:,:]
img_1 = cv2.imread('./images/apple_512.jpg')
img_2 = cv2.imread('./images/orange_512.jpg')

img_1_l = img_1[:,0:img_1.shape[1]/2,:]
img_2_r = img_2[:,img_2.shape[1]/2:,:]

img_blended_complex = image_blend_pyramid(img_1,img_2,6)[:,:-50,:]
img_blended_simple = np.concatenate((img_1_l,img_2_r),axis=1)
cv2.imshow('simpleblend',img_blended_simple)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./images/simple_blend_orapple.jpg',img_blended_simple)

cv2.imshow('complexblend',img_blended_complex)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./images/complex_blend_orapple.jpg',img_blended_complex)


