#!/usr/bin/python3

# Created by Ivan Matveev on 01.07.20
# E-mail: ivan.matveev@hs-anhalt.de

# Find an optimized camera matrix which can provide sufficient AOVs using OpenCV calibration matrix

import cv2
import yaml
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Find optimal camera calibration matrix')
parser.add_argument('calib_mtx', action='store', help="path to original calibration parameters")
parser.add_argument('dist_img', action='store', help="path to distorted image")
parser.add_argument('-a', '--alpha', action='store', default=0.5, type=float,
                    help="Free scaling parameter between 0 (when all the pixels in the undistorted image are valid) "
                         "and 1 (when all the source image pixels are retained in the undistorted image); default 0.5")
parser.add_argument('--out_img', action='store', help="path to output image")
parser.add_argument('--out_yml', action='store', help="path to output file")

args = parser.parse_args()

calib_params = yaml.safe_load(open(args.calib_mtx))
image = cv2.imread(args.dist_img, 0)
w, h = calib_params['base_res']
in_mtx = np.asarray(calib_params['camera_matrix'])
dist = np.asarray(calib_params['dist_coefs'])

new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(in_mtx, dist, (w, h), args.alpha, (w, h))
dst = cv2.undistort(image, in_mtx, dist, None, new_camera_mtx)

print('New optimized matrix:\n{}'.format(new_camera_mtx))

if args.out_img:
    cv2.imwrite(args.out_img, dst)
if args.out_yml:
    calibration = {'camera_matrix': calib_params['camera_matrix'], 'dist_coefs': calib_params['dist_coefs'],
                   'base_res': [w, h], 'optimized_res': [w, h], 'optimized_matrix': new_camera_mtx.tolist()}
    with open(args.out_yml, 'w') as fw:
        yaml.dump(calibration, fw)

cv2.imshow('Undistorted image', dst)

wait_time = 1000
while cv2.getWindowProperty('Undistorted image', cv2.WND_PROP_VISIBLE) >= 1:
    keyCode = cv2.waitKey(wait_time)
    if (keyCode & 0xFF) == ord("q"):
        cv2.destroyAllWindows()
        break
