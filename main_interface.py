#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZetCode wxPython tutorial

In this example we create a new class layout
with wx.GridBagSizer.

author: Jan Bodnar
website: www.zetcode.com
last modified: April 2018
"""
import os

import cv2

import wx

import _thread
import face_reco_from_camera
import get_faces_from_camera
import features_extraction_to_csv





def resizeImage(self, image):
    # bmp = image.Scale(width, height).ConvertToBitmap()
    cliWidth, cliHeight = self.GetClientSize()
    if not cliWidth or not cliHeight:
        return
    fw = cliWidth / 3
    fh = fw * self.imgh / self.imgw

    resizedImg = image.Scale(fw, fh)

    return resizedImg

def openFolder(self):
    os.system("start explorer %s" % '.\data\data_faces_from_camera')

class Example(wx.Frame):
    def featuresExtraction(self, event):
        _thread.start_new_thread(features_extraction_to_csv.features_extraction, (event,))
        print("features_extraction_to_csv")

    def getFaces(self, event):
        _thread.start_new_thread(get_faces_from_camera.get_faces, (event,))
        print("get_faces_from_camera")

    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)  # 设置对话框的大小
        self.Center()  # 设置弹窗在屏幕中间

        panel = wx.Panel(self)
        self.box1 = wx.BoxSizer()  # 定义横向的box1
        self.img = wx.Image('./data/default.jpg', wx.BITMAP_TYPE_ANY)
        self.imgh = self.img.GetHeight()
        self.imgw = self.img.GetWidth()

        resizedImg = resizeImage(self, self.img)

        self.bmp = wx.StaticBitmap(panel, -1, wx.Bitmap(resizedImg))
        self.box1.Add(self.bmp, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        self.figure = wx.StaticBitmap(panel, -1, wx.Bitmap(resizedImg))
        self.box1.Add(self.figure, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        self.box2 = wx.BoxSizer()  # 定义横向的box1
        text = wx.StaticText(panel, label="被测人")
        self.box2.Add(text, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        self.name = wx.StaticText(panel, label="最相似人选")
        self.box2.Add(self.name, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        self.ratio = wx.StaticText(panel, label="欧氏距离")
        self.box2.Add(self.ratio, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        self.box3 = wx.BoxSizer()  # 定义横向的box1
        button1 = wx.Button(panel, label='人脸识别入口')
        self.box3.Add(button1, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        button1.Bind(wx.EVT_BUTTON, self.faceReco)

        button2 = wx.Button(panel, label='实时摄像头录入人脸')
        self.box3.Add(button2, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        button2.Bind(wx.EVT_BUTTON, self.getFaces)

        self.box4 = wx.BoxSizer()  # 定义横向的box1
        # button3 = wx.Button(panel, label='系统图片批量录入人脸')
        button3 = wx.Button(panel, label='打开数据库存储路径')
        self.box4.Add(button3, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        button3.Bind(wx.EVT_BUTTON, openFolder)

        button4 = wx.Button(panel, label='分析数据库人脸')
        self.box4.Add(button4, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        button4.Bind(wx.EVT_BUTTON, self.featuresExtraction)

        self.v_box = wx.BoxSizer(wx.VERTICAL)  # 定义一个纵向的v_box
        self.v_box.Add(self.box1, proportion=6, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box1，比例为1
        self.v_box.Add(self.box2, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box2，比例为7
        self.v_box.Add(self.box3, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box3，比例为1
        self.v_box.Add(self.box4, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box4，比例为1

        panel.SetSizer(self.v_box)
        self.Show()

    def faceReco(self, event):
        _thread.start_new_thread(self._faceReco, (event,))
        print("face_reco_from_camera")

    def _faceReco(self, event):
        resultList = face_reco_from_camera.face_reco()
        distance = resultList[0]
        name = resultList[1]
        cnt = 0
        for person in os.listdir("data/data_faces_from_camera/"):
            print(person)
            cnt = cnt + 1
            # sub_path = os.path.join("data/data_faces_from_camera/", person)
            if cnt == name:
                name = person
                break
        btm_rd = resultList[2]
        height, width = btm_rd.shape[:2]


        # height = int(300 / width * height)
        # width = 300

        btm_rd = cv2.resize(btm_rd, (width, height), cv2.COLOR_BGR2RGB)
        btm_rd = cv2.cvtColor(btm_rd, cv2.COLOR_BGR2RGB)
        btm_rd = wx.Bitmap.FromBuffer(width, height, btm_rd)

        # 显示图片在panel上
        self.name.SetLabel(name)
        self.ratio.SetLabel(distance)
        img_figure = wx.Image("./data/data_faces_from_camera/" + name + "/img_face_1.jpg", wx.BITMAP_TYPE_ANY)
        self.figure.SetBitmap(resizeImage(self, img_figure).ConvertToBitmap())
        self.bmp.SetBitmap(resizeImage(self, btm_rd.ConvertToImage()).ConvertToBitmap())
        self.SetSize(751, 501)



def main():
    app = wx.App()
    ex = Example(None, -1, title="监所人脸识别系统", size=(750, 500))
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    main()
