# !/usr/bin/env python3

from argparse import ArgumentParser
from copy import deepcopy

import cv2
import numpy as np

from config import main_config
from models import gmcnn_gan
from utils import training_utils

from utils import constants  # lzx增加

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os


log = training_utils.get_logger()

MAIN_CONFIG_FILE = './config/main_config.ini'


def preprocess_image(image, model_input_height, model_input_width):
    image = image[..., [2, 1, 0]]
    image = (image - 127.5) / 127.5
    image = cv2.resize(image, (model_input_height, model_input_width))
    image = np.expand_dims(image, 0)
    return image


def preprocess_mask(mask, model_input_height, model_input_width):
    mask[mask < 128] = 0  # mzh增加
    mask[mask >= 128] = 1  # mzh增加
    mask = cv2.resize(mask, (model_input_height, model_input_width))
    mask = np.expand_dims(mask, 0)
    return mask


def postprocess_image(image):
    image = (image + 1) * 127.5
    return image


def main(picture_address,mask_address,save_address):
    parser = ArgumentParser()
    print(picture_address)
    print('\n')
    print(mask_address)
    print('\n')
    print(save_address)
    print('\n')

    args = parser.parse_args()
    args.image = picture_address
    args.mask = mask_address
    args.save_to = save_address+"/output.jpg"
    output_paths = constants.OutputPaths(experiment_name="train12000_128")  # lzx增加

    config = main_config.MainConfig(MAIN_CONFIG_FILE)

    gmcnn_model = gmcnn_gan.GMCNNGan(batch_size=config.training.batch_size,
                                     img_height=config.training.img_height,
                                     img_width=config.training.img_width,
                                     num_channels=config.training.num_channels,
                                     warm_up_generator=False,
                                     config=config,
                                     output_paths=output_paths)  # lzx增加
    log.info('Loading GMCNN model...')
    gmcnn_model.load()
    log.info('GMCNN model successfully loaded.')

    image = cv2.imread(args.image)
    mask = cv2.imread(args.mask)

    image = preprocess_image(image, config.training.img_height, config.training.img_width)
    mask = preprocess_mask(mask, config.training.img_height, config.training.img_width)

    log.info('Making prediction...')
    predicted = gmcnn_model.predict([image, mask])
    predicted = postprocess_image(predicted)

    masked = deepcopy(image)
    masked = postprocess_image(masked)
    masked[mask == 1] = 255

    constructed = deepcopy(masked)
    constructed[mask == 1] = predicted[mask == 1]

    result_image = np.concatenate((masked[0][..., [2, 1, 0]],
                                   # predicted[0][..., [2, 1, 0]],
                                   constructed[0][..., [2, 1, 0]],
                                   image[0][..., [2, 1, 0]] * 127.5 + 127.5),
                                  axis=1)

    cv2.imwrite(args.save_to, result_image)
    log.info('Saved results to: %s', args.save_to)

#_______________UI_events_design__________________________

class Ui_GAN(object):
    Picture_Address = ''
    Mask_Address = ''
    Save_Address = ''
    def setupUi(self, GAN):
        GAN.setObjectName("GAN")
        GAN.resize(1114, 637)
        GAN.setMinimumSize(1114,657)
        GAN.setMaximumSize(1114,657)
        #GAN.setSizeGripEnabled(False)
        self.create = QtWidgets.QPushButton(GAN)
        self.create.setGeometry(QtCore.QRect(460, 540, 191, 61))
        self.create.setObjectName("create")

        self.picture_address = QtWidgets.QPushButton(GAN)
        self.picture_address.setGeometry(QtCore.QRect(110, 20, 191, 51))
        self.picture_address.setObjectName("picture_address")
        self.mask_address = QtWidgets.QPushButton(GAN)
        self.mask_address.setGeometry(QtCore.QRect(460, 20, 191, 51))
        self.mask_address.setObjectName("mask_address")
        self.save_address = QtWidgets.QPushButton(GAN)
        self.save_address.setGeometry(QtCore.QRect(820, 20, 191, 51))
        self.save_address.setObjectName("save_address")

        self.picture_text = QtWidgets.QPushButton(GAN)
        self.picture_text.setGeometry(QtCore.QRect(40, 110, 321, 31))
        self.picture_text.setText("")
        self.picture_text.setObjectName("picture_text")

        self.mask_text = QtWidgets.QPushButton(GAN)
        self.mask_text.setGeometry(QtCore.QRect(410, 110, 321, 31))
        self.mask_text.setText("")
        self.mask_text.setObjectName("mask_text")

        self.save_text = QtWidgets.QPushButton(GAN)
        self.save_text.setGeometry(QtCore.QRect(780, 110, 321, 31))
        self.save_text.setText("")
        self.save_text.setObjectName("save_text")

        self.output = QtWidgets.QLabel(GAN)
        self.output.setGeometry(QtCore.QRect(19, 185, 1075, 303))
        self.output.setText("")
        self.output.setObjectName("output")

        self.retranslateUi(GAN)
        QtCore.QMetaObject.connectSlotsByName(GAN)

    def retranslateUi(self, GAN):
        _translate = QtCore.QCoreApplication.translate
        GAN.setWindowTitle(_translate("GAN", "Gan图像"))
        self.create.setText(_translate("GAN", "生成结果"))
        self.picture_address.setText(_translate("GAN", "原图地址"))
        self.mask_address.setText(_translate("GAN", "遮罩地址"))
        self.save_address.setText(_translate("GAN", "保存地址"))

    def get_picture(self):
        picture_address = QtWidgets.QFileDialog.getOpenFileName(None, "选取图片地址", 'd:/')
        picture_address = picture_address[0]
        # global Picture_Address
        # Picture_Address = picture_address
        self.Picture_Address=picture_address
        temp=picture_address.split('/')
        temp=temp[-1]
        self.picture_text.setText(temp)

    def get_mask(self):
        mask_address = QtWidgets.QFileDialog.getOpenFileName(None, "选取遮蔽图片地址", 'd:/')
        mask_address = mask_address[0]
        # global Mask_Address
        # Mask_Address = mask_address
        self.Mask_Address=mask_address
        temp = mask_address.split('/')
        temp = temp[-1]
        self.mask_text.setText(temp)

    def get_save(self):
        save_address = QtWidgets.QFileDialog.getExistingDirectory(None, "选取生成图片保存地址", 'd:/')
        self.Save_Address=save_address
        self.save_text.setText(save_address)


    def get_output(self):
        ok=True
        if self.Picture_Address=='':
            ok=False
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '没有选择原图地址!')
            msg_box.exec_()
        elif self.Mask_Address=='':
            ok=False
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '没有选择遮罩地址!')
            msg_box.exec_()
        elif self.Save_Address=='':
            ok=False
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '没有选择结果保存地址!')
            msg_box.exec_()

        if ok:
            main(self.Picture_Address, self.Mask_Address, self.Save_Address)
            if os.path.exists(self.Save_Address + '/output.jpg'):
                picture = QPixmap(self.Save_Address + '/output.jpg')
                # wsize = picture.width()
                # hsize = picture.height()
                # picture = picture.scaled(wsize * 2, hsize * 2)
                output_w=self.output.width()
                output_h=self.output.height()
                picture = picture.scaled(output_w, output_h)

                self.output.setAlignment(Qt.AlignVCenter)
                self.output.setPixmap(picture)
                msg_box = QMessageBox(QMessageBox.Information, '成功!', '已生成结果!')
                msg_box.exec_()

                # self.setScaledContents (True)
            else:
                msg_box = QMessageBox(QMessageBox.Warning, '失败', '结果生成失败!')
                msg_box.exec_()

        # else:





