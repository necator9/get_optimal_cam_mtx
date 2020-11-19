# Get optimal camera matrix

Find an optimized camera matrix which can provide sufficient AOVs using OpenCV calibration matrix.
Change alpha value in interval [0, 1] to achieve desired scaling and to get as result the optimized matrix.

input image -> 
to relative coordinates using original matrix -> 
undistort -> 
project back using optimized martix 


## Usage

```shell
usage: get_optimal_cam_mtx.py [-h] [-a ALPHA] [--out_img OUT_IMG] [--out_yml OUT_YML] calib_mtx dist_img

Find optimal camera calibration matrix

positional arguments:
  calib_mtx             path to original calibration parameters
  dist_img              path to distorted image

optional arguments:
  -h, --help            show this help message and exit
  -a ALPHA, --alpha ALPHA
                        Free scaling parameter between 0 (when all the pixels 
                        in the undistorted image are valid) and 1 (when all the 
                        source image pixels are retained in the undistorted image); 
                        default 0.5
  --out_img OUT_IMG     path to output image
  --out_yml OUT_YML     path to output file

```
## Example
```shell
python get_optimal_cam_mtx.py \
examples/input/calibration.yml \
examples/input/distorted_2.png \
-a 0.56 \
--out_yml examples/output/calibration_opt.yml \
--out_img examples/output/undistorted_2.png
```