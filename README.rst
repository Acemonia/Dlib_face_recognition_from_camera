Face recognition from camera with Dlib
######################################

Added Introduction
******************
利用 Python 开发，借助 Dlib 库捕获摄像头中的人脸，提取人脸特征，通过计算特征值之间的欧氏距离，来和预存的人脸特征进行对比，判断是否匹配，达到人脸识别的目的；

- 完成的功能
    - 新的人脸数据集和识别模型
    - 做到视频识别， 实时显示人脸信息
    - 可摄像头添加人脸， 且可改名
    - 可通过文件夹方式批量添加人脸
    - GUI化， 基本无卡顿

.. image:: introduction/main_interface.png
  :align: center

.. image:: introduction/main_figure_interface.png
  :align: center

Former Introduction
*******************

Detect and recognize single/multi-faces from camera;

调用摄像头进行人脸识别，支持多张人脸同时识别;


#. 摄像头人脸录入 / Face register

   请不要离摄像头过近，人脸超出摄像头范围时会有 "OUT OF RANGE" 提醒 /
   Please do not be too close to the camera, or you can't save faces with "OUT OF RANGE" warning;

#. 提取特征建立人脸数据库 / Generate database from images captured
#. 利用摄像头进行人脸识别 / Face recognizer
   
   当单张人脸 / When single-face:

   当多张人脸 / When multi-faces:

   一张已录入人脸 + 未录入 unknown 人脸 / 1x known face + 2x unknown face:

   同时识别多张已录入人脸 / multi-faces recognition at the same time:

** 关于精度 / About accuracy:

* When using a distance threshold of ``0.6``, the dlib model obtains an accuracy of ``99.38%`` on the standard LFW face recognition benchmark.

** 关于算法 / About algorithm

* 基于 Residual Neural Network / 残差网络的 CNN 模型;

* This model is a ResNet network with 29 conv layers. It's essentially a version of the ResNet-34 network from the paper Deep Residual Learning for Image Recognition by He, Zhang, Ren, and Sun with a few layers removed and the number of filters per layer reduced by half.

Overview
********

此项目中人脸识别的实现流程 / The design of this repo:

.. image:: introduction/overview.png
   :align: center

Steps
*****

#. 安装依赖库 / Install some python packages if needed

   .. code-block:: bash

      pip3 install opencv-python
      pip3 install scikit-image
      pip3 install dlib
      pip install wxPython-4.0.0a2.dev3038+953a2e5-cp27-cp27mu-linux_x86_64.whl


#. 下载源码 / Download zip from website or via GitHub Desktop in windows, or git clone repo in Ubuntu

   .. code-block:: bash

      git clone https://github.com/coneypo/Dlib_face_recognition_from_camera

#. 进行人脸信息采集录入 / Register faces 

   .. code-block:: bash

      python3 get_face_from_camera.py

#. 提取所有录入人脸数据存入 "features_all.csv" / Features extraction and save into "features_all.csv"

   .. code-block:: bash

      python3 features_extraction_to_csv.py

#. 调用摄像头进行实时人脸识别 / Real-time face recognition

   .. code-block:: bash

      python3 face_reco_from_camera.py


About Source Code
*****************

Repo 的 tree / 树状图:

::

    .
    ├── main_interface.py               # Step0. Start First
    ├── get_faces_from_camera.py        # Step1. Faces register
    ├── features_extraction_to_csv.py   # Step2. Features extraction
    ├── face_reco_from_camera.py        # Step3. Faces recognition
    ├── how_to_use_camera.py            # Use the default camera by opencv
    ├── data
    │   ├── data_dlib                   # Dlib's model
    │   │   ├── dlib_face_recognition_resnet_model_v1.dat
    │   │   ├── shape_predictor_5_face_landmarks.dat
    │   │   └── shape_predictor_68_face_landmarks.dat
    │   ├── data_faces_from_camera      # Face images captured from camera (will generate after step 1)
    │   │   ├── person_1
    │   │   │   ├── img_face_1.jpg
    │   │   │   └── img_face_2.jpg
    │   │   └── person_2
    │   │       └── img_face_1.jpg
    │   │       └── img_face_2.jpg
    │   └── features_all.csv            # CSV to save all the features of known faces (will generate after step 2)
    ├── introduction                    # Some files for readme.rst
    │   ├── main_figure_interface.png
    │   ├── main_interface.png
    │   └── overview.png
    ├── README.md
    └── requirements.txt                # Some python packages needed

用到的 Dlib 相关模型函数:

#. Dlib 正向人脸检测器 (based on HOG), output: <class 'dlib.dlib.rectangles'>


   .. code-block:: python

      detector = dlib.get_frontal_face_detector()
      faces = detector(img_gray, 0)

	  
#. Dlib 人脸预测器, output: <class 'dlib.dlib.full_object_detection'>,
   will use shape_predictor_68_face_landmarks.dat

   .. code-block:: python

      # This is trained on the ibug 300-W dataset (https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/)
      # Also note that this model file is designed for use with dlib's HOG face detector.
      # That is, it expects the bounding boxes from the face detector to be aligned a certain way, the way dlib's HOG face detector does it.
      # It won't work as well when used with a face detector that produces differently aligned boxes,
      # such as the CNN based mmod_human_face_detector.dat face detector.

      predictor = dlib.shape_predictor("data/data_dlib/shape_predictor_68_face_landmarks.dat")
      shape = predictor(img_rd, faces[i])

	  
#. 特征描述子 Face recognition model, the object maps human faces into 128D vectors


   .. code-block:: python

      face_rec = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


Python 源码介绍如下:

#. get_face_from_camera.py: 

   进行 Face register / 人脸信息采集录入

   * 请注意存储人脸图片时，矩形框不要超出摄像头范围，要不然无法保存到本地;
   * 超出会有 "out of range" 的提醒;


#. features_extraction_to_csv.py:
     
   从上一步存下来的图像文件中，提取人脸数据存入CSV;
  
   * 会生成一个存储所有特征人脸数据的 "features_all.csv"；
   * size: n*128 , n means n people you registered and 128 means 128D features of the face


#. face_reco_from_camera.py: 

   这一步将调用摄像头进行实时人脸识别; / This part will implement real-time face recognition;
  
   * Compare the faces captured from camera with the faces you have registered which are saved in "features_all.csv"
   
   * 将捕获到的人脸数据和之前存的人脸数据进行对比计算欧式距离, 由此判断是否是同一个人;
