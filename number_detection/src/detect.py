#!/usr/bin/env python

#encoding='utf-8'

import sys

print(sys.version_info)

import os

import numpy as np
import cv2
import torch
import random

# ROS imports
import rospy
from rospkg import RosPack
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from number_detection.msg import BoundingBox, BoundingBoxes
from utils.torch_utils import select_device, load_classifier
from utils.general import check_img_size
from models.experimental import attempt_load

# get the path to package
package = RosPack()
package_path = package.get_path('number_detection')


class NumberDetectionROSNode:
    """
    Number detection ROS node.
    """
    def __init__(self):
        
        # get weight parameter from launch file
        self.weights_path = rospy.get_param('~weights_path')

        if not os.path.isfile(self.weights_path):
            rospy.loginfo('[WARN] Weights not found. Downloading...')
        else:
            rospy.loginfo("[INFO] Weights found, loading %s", self.weights_path)
            
            # download weights from dropbox or google drive


        # Load image parameter and confidence threshold
        self.image_topic = rospy.get_param(
            '~image_topic', '/camera/rgb/image_raw')

        self.conf_thres = rospy.get_param('~confidence', 0.5)

        print(f"The CONFIDENCE VALUE IS: {self.conf_thres}")

        # Load other parameters
        self.device_name = 'cpu'
        self.device = select_device(self.device_name)
        self.gpu_id = rospy.get_param('~gpu_id', 0)
        self.network_img_size = rospy.get_param('~img_size', 416)
        self.publish_image = rospy.get_param('~publish_image')
        self.iou_thres = 0.45
        self.augment = True

        self.classes = None
        self.agnostic_nms = False

        self.w = 0
        self.h = 0

        # Second-stage classifier
        self.classify = False

        # Initialize
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA        

        # Load model
        self.model = attempt_load(
            self.weights_path, map_location=self.device)  # load FP32 model
        self.stride = int(self.model.stride.max())      # model stride
        self.network_img_size = check_img_size(
            self.network_img_size, s=self.stride)  # check img_size

        if self.half:
            self.model.half()  # to FP16

        if self.classify:
            self.modelc = load_classifier(name='resnet101', n=2)  # initialize
            self.modelc.load_state_dict(torch.load(
                'weights/resnet101.pt', map_location=self.device)['model']).to(self.device).eval()

        # Get names and colors
        self.names = self.model.module.names if hasattr(
            self.model, 'module') else self.model.names
        self.colors = [[random.randint(0, 255)
                        for _ in range(3)] for _ in self.names]

        # Run inference
        if self.device.type != 'cpu':
            self.model(torch.zeros(1, 3, self.network_img_size, self.network_img_size).to(
                self.device).type_as(next(self.model.parameters())))  # run once

        # Load CvBridge
        self.bridge = CvBridge()

        # Load publisher topic
        self.detected_objects_topic = rospy.get_param(
            '~detected_objects_topic')
        self.published_image_topic = rospy.get_param('~detections_image_topic')

        # Define subscribers
        self.image_sub = rospy.Subscriber(
            self.image_topic, Image, self.image_cb, queue_size=1, buff_size=2**24)

        # Define publishers
        self.pub_ = rospy.Publisher(
            self.detected_objects_topic, BoundingBoxes, queue_size=10)
        self.pub_viz_ = rospy.Publisher(
            self.published_image_topic, Image, queue_size=10)
        rospy.loginfo("Launched node for object detection")


    def callback(self, ros_msg):
        pass


    def main(self):
        rospy.spin()


if __name__ == '__main__':
    
    rospy.init_node('number_detection', anonymous=True)
    det_ros = NumberDetectionROSNode()
    det_ros.main()
    
    print("[INFO] Node run successful!")