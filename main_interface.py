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


def featuresExtraction(event):
    _thread.start_new_thread(features_extraction_to_csv.features_extraction(), (event,))
    print("features_extraction_to_csv")


def getFaces(event):
    _thread.start_new_thread(get_faces_from_camera.get_faces(), (event,))
    print("get_faces_from_camera")


def resizeBitmap(image, width=300, height=300):
    bmp = image.Scale(width, height).ConvertToBitmap()
    return bmp


# def test(event):
#     while (1):
#         print("python get_faces_from_camera.py")
#         print("python features_extraction_to_csv.py")


class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title)
        self.InitUI()
        self.Centre()

    # def set_bmp_pic(self, pic):
    #     self.bmp.SetBitmap(self, pic)
    #     print(Example.title, pic)

    # def get_bmp(self):
    #     return self.bmp

    def faceReco(self, event):
        _thread.start_new_thread(self._faceReco, (event,))
        print("face_reco_from_camera")

    def InitUI(self):
        panel = wx.Panel(self)

        self.sizer = wx.GridBagSizer(5, 2)

        text0 = wx.StaticText(panel, label="注意: 点击按钮会弹出新界面")
        self.sizer.Add(text0, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                       border=10)

        line = wx.StaticLine(panel)
        self.sizer.Add(line, pos=(1, 0), span=(1, 3),
                       flag=wx.EXPAND | wx.BOTTOM, border=10)

        image_cover = resizeBitmap(
            wx.Image('./data/default.jpg', wx.BITMAP_TYPE_ANY))

        self.bmp = wx.StaticBitmap(panel, -1, wx.Bitmap(image_cover))
        # self.bmp = wx.StaticBitmap(panel)
        self.sizer.Add(self.bmp, pos=(2, 0))

        self.figure = wx.StaticBitmap(panel, -1, wx.Bitmap(image_cover))
        self.sizer.Add(self.figure, pos=(2, 1), flag=wx.LEFT | wx.RIGHT)

        text = wx.StaticText(panel, label="被测人")
        self.sizer.Add(text, pos=(3, 0))

        self.name = wx.StaticText(panel, label="最相似人选")
        self.sizer.Add(self.name, pos=(3, 1))

        self.ratio = wx.StaticText(panel, label="相似百分比")
        self.sizer.Add(self.ratio, pos=(4, 1))

        line2 = wx.StaticLine(panel)
        self.sizer.Add(line2, pos=(5, 0), span=(1, 3),
                       flag=wx.EXPAND | wx.BOTTOM, border=10)
        print("3")

        button1 = wx.Button(panel, label='人脸识别入口')
        self.sizer.Add(button1, pos=(6, 0))
        button1.Bind(wx.EVT_BUTTON, self.faceReco)
        print("4")

        button2 = wx.Button(panel, label='实时摄像头录入人脸')
        self.sizer.Add(button2, pos=(7, 0))
        button2.Bind(wx.EVT_BUTTON, getFaces)

        # button3 = wx.Button(panel, label='系统图片批量录入人脸')
        button3 = wx.Button(panel, label='分析数据库人脸')
        self.sizer.Add(button3, pos=(7, 1))
        button3.Bind(wx.EVT_BUTTON, featuresExtraction)

        self.sizer.AddGrowableCol(2)

        panel.SetSizer(self.sizer)
        self.SetSize((800, 400))
        self.sizer.Fit(self)

    def _faceReco(self, event):
        resultList = face_reco_from_camera.face_reco()
        distance = resultList[0]
        name = resultList[1]
        img_rd = resultList[2]
        print(img_rd)
        height, width = img_rd.shape[:2]
        print(height + width)

        height = int(300 / width * height)
        width = 300

        img_rd = cv2.resize(img_rd, (width, height), cv2.COLOR_BGR2RGB)
        image1 = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
        pic = wx.Bitmap.FromBuffer(width, height, image1)

        # 显示图片在panel上
        self.name.SetLabel(name)
        self.ratio.SetLabel(distance)
        img_figure = wx.Image("./data/data_faces_from_camera/" + name + "/img_face_1.jpg", wx.BITMAP_TYPE_ANY)
        self.figure.SetBitmap(resizeBitmap(img_figure))
        self.bmp.SetBitmap(pic)
        print("_faceReco")


def main():
    app = wx.App()
    print("2")
    ex = Example(None, title="人脸识别系统", )
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    print("1")
    path = os.path.dirname(os.path.abspath(__file__))
    print(path)
    main()
