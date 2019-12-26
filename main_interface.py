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

import wx
import _thread
import face_reco_from_camera
import get_faces_from_camera
import features_extraction_to_csv


def faceReco(event):
    _thread.start_new_thread(face_reco_from_camera.face_reco(), (event, ))
    print("face_reco_from_camera")

def featuresExtraction(event):
    _thread.start_new_thread(features_extraction_to_csv.features_extraction(), (event, ))
    print("features_extraction_to_csv")

def getFaces(event):
    _thread.start_new_thread(get_faces_from_camera.get_faces(), (event, ))
    print("get_faces_from_camera")
    featuresExtraction


def test(event):
    while(1):
        print("python get_faces_from_camera.py")
        print("python features_extraction_to_csv.py")

class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title)

        self.InitUI()
        self.Centre()

    def InitUI(self):
        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(5, 3)

        text0 = wx.StaticText(panel, label="注意: 点击按钮会弹出新界面")
        sizer.Add(text0, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM,
                  border=10)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 3),
                  flag=wx.EXPAND | wx.BOTTOM, border=10)

        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('./data/data_faces_from_camera/person_1/img_face_1.jpg'))
        sizer.Add(icon, pos=(2, 0))

        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('./data/data_faces_from_camera/person_1/img_face_1.jpg'))
        sizer.Add(icon, pos=(2, 1))

        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('./data/data_faces_from_camera/person_1/img_face_1.jpg'))
        sizer.Add(icon, pos=(2, 2))

        text1 = wx.StaticText(panel, label="被测人")
        sizer.Add(text1, pos=(3, 0))

        text2 = wx.StaticText(panel, label="最相似人选")
        sizer.Add(text2, pos=(3, 1))

        text3 = wx.StaticText(panel, label="次相似人选")
        sizer.Add(text3, pos=(3, 2))

        text4 = wx.StaticText(panel, label="相似百分比")
        sizer.Add(text4, pos=(4, 1))

        text5 = wx.StaticText(panel, label="相似百分比")
        sizer.Add(text5, pos=(4, 2))

        line2 = wx.StaticLine(panel)
        sizer.Add(line2, pos=(5, 0), span=(1, 3),
                  flag=wx.EXPAND | wx.BOTTOM, border=10)

        button1 = wx.Button(panel, label='人脸识别入口')
        sizer.Add(button1, pos=(6, 0))
        button1.Bind(wx.EVT_BUTTON, faceReco)

        button2 = wx.Button(panel, label='实时摄像头录入人脸')
        sizer.Add(button2, pos=(6, 1))
        button2.Bind(wx.EVT_BUTTON, getFaces)

        button3 = wx.Button(panel, label='系统图片批量录入人脸')
        sizer.Add(button3, pos=(6, 2))
        button3.Bind(wx.EVT_BUTTON, getFaces)

        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)
        self.SetSize((1250,650))




def main():
    app = wx.App()
    ex = Example(None, title="人脸识别系统")
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
