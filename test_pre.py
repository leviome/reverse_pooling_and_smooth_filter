#coding:utf-8
"""
@author: liaoliwei

"""
#1、对图像做去噪处理，提取有效信息
#2、用最大池化法对图像尺寸进行缩小，缩至28×28
#3、反向池化，将图像放大到224×224
#4、平滑滤波，使图像边缘更圆润，恢复自然性
#5、本程序通过可视化方式，展示反向池化以及平滑滤波效果

import Image
import numpy as np
import matplotlib.pyplot as plt


SHOW_VALUE = 255
def prehandle(imgname):
	img = Image.open(imgname)
	img1 = binary(img)
	img2 = Image.fromarray(max_pool(np.array(thin_pic(np.array(img1)))))
	#img2.show()
	na224 = reverse_pool(np.array(img2))
	img3 = Image.fromarray(na224)
	img4 = Image.fromarray(erzhihua(filter1(na224)))

	fig=plt.figure(u"预处理数字图像")

	ax0 = fig.add_subplot(5,5,11)
	ax0.set_xlabel(u"img28*28")
	ax0.imshow(img2)

	ax1 = fig.add_subplot(132)
	ax1.set_xlabel(u"reverse_pool")
	ax1.imshow(img3)

	ax2 = fig.add_subplot(133)
	ax2.set_xlabel(u"smooth_filter")
	ax2.imshow(img4)
	plt.show()



def binary(img):
	itarr = np.array(img)
	#print(itarr)
	a,b,d = np.shape(itarr)
	#print(a,b,d)
	for aa in range(a):
		for bb in range(b):
			if qiucha(itarr[aa][bb][0],150,50) and qiucha(itarr[aa][bb][1],149,50) and qiucha(itarr[aa][bb][2],145,50):
				itarr[aa][bb][0] = SHOW_VALUE
				itarr[aa][bb][1] = SHOW_VALUE
				itarr[aa][bb][2] = SHOW_VALUE
			else:
				itarr[aa][bb][0] = 0
				itarr[aa][bb][1] = 0
				itarr[aa][bb][2] = 0
	it1 = Image.fromarray(itarr)
	return it1


def erzhihua(na):
	a,b = np.shape(na)
	for i in range(a):
		for j in range(b):
			if na[i][j]>=135:
				na[i][j]=SHOW_VALUE
			else:	na[i][j]=0
	return na


#反向池化
def reverse_pool(na28):
        na224 = np.zeros((224,224))
        a,b = np.shape(na28)
        for i in range(a):
                for j in range(b):
                        for m in range(8):
                                for n in range(8):
                                        na224[i*8+m][j*8+n] = na28[i][j]
        return na224

#平滑滤波
def filter1(na):
	a,b = np.shape(na)
	for i in range(8,a-8):
		for j in range(8,b-8):
			l=[]
			for m in range(-8,9):
				for n in range(-8,9):
					l.append(na[i+m][j+n])
			na[i][j] = int(sum(l)/len(l))
	return na
			


def qiucha(x,y,cha):
	if x-y < cha and x-y> cha*(-1):
		return True
	else:
		return False


def write_array(na):
	wr = open('x.py', 'a')
	wr.write('x=[\n')
	a,b = np.shape(na)
	for i in range(a):
		wr.write('[')
		for j in range(b):
			if j==b-1:
				wr.write(str(int(na[i][j]))+' ')
			else:
				wr.write(str(int(na[i][j]))+', ')
		if i==a-1 and j==b-1:
			wr.write(']]\n')
		else:
			wr.write('],\n')
	wr.close()
	print('write successfully!')

#最大池化
def max_pool(na):
	na = kuoda(na)
	na28 = np.zeros((28,28))
	#Image.fromarray(na).show()
	for i in range(28):
		for j in range(28):
			l = []
			for m in range(16):
				for n in range(16):
					l.append(na[i*16+m][j*16+n])
			na28[i][j] = min(l)

	return na28
	

#扩大图片尺寸至28的整数倍，有利于直接池化
def kuoda(na):
	na448 = np.zeros((448,448))
	a,b = np.shape(na)
	for i in range(448):
		for j in range(448):
			if i<=a-1 and j<=b-1:
				na448[i][j] = na[i][j]
			else:	na448[i][j] = SHOW_VALUE
	return na448

#将3D转为2D，RGB转灰度图
def thin_pic(img):
	na = np.array(img)
	a,b,c= np.shape(na)
	no = np.zeros((a,b))
	for i in range(a):
		for j in range(b):
			no[i][j] = na[i][j][0]
	no_pic = Image.fromarray(no)
	return no_pic



if __name__=='__main__':
	imgname = input("input filename : ")
	prehandle(imgname)
