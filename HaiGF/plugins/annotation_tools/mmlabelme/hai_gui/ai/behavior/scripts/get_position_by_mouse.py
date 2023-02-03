"""
获取鼠标点击图像的坐标, 直接run可以测试
"""
import os
import cv2
import time
from absl import app, flags

FLAGS = flags.FLAGS
flags.DEFINE_string('img', 'sources/fall6/000001.jpg', 'image path')
flags.DEFINE_float('scale', 1, 'show scale')
# flags.mark_flag_as_required('img')


class MouseImage(object):
    def __init__(self):
        # self.img = cv2.imread(f'../source/sansan2.jpg')
        self.xy = None
        self.clicked = None
        self.moved = None

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            # cv2.circle(self.img, (x, y), 1, (255, 0, 0), thickness=-1)
            # cv2.putText(self.img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
            #             1.0, (0, 0, 0), thickness=1)
            # cv2.imshow("image", self.img)
            self.xy = (int(x), int(y))
            self.clicked = 'left'
            # print(self.xy)
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clicked = 'right'
        elif event == cv2.EVENT_MOUSEMOVE:
            self.moved = True
            self.xy = (int(x), int(y))

    def cap_and_refresh(self, adb, image_name=None, scale=None):
        """
        不断截图刷新显示图片，左键点击就是点击，右键点击退出
        :param adb:
        :param image_name:
        :param scale:
        :return:
        """
        image_name = 'image' if image_name is None else image_name
        self.clicked = False
        self.xy = None
        while True:
            # t = time.time()
            adb.screencap()
            # print(f'sctime: {(time.time() - t) * 1000:.2f}')
            img = cv2.imread('sc.png')
            if scale is not None:
                h, w, c = img.shape
                img = cv2.resize(img, (int(scale * w), int(scale * h)))
            cv2.namedWindow(image_name)
            cv2.setMouseCallback(image_name, self.on_mouse)
            cv2.imshow(image_name, img)
            if cv2.waitKey(1) == ord('q') or self.clicked == 'left':
                cv2.destroyAllWindows()
                if scale is not None:  # scale back
                    self.xy = (int(self.xy[0] / scale), int(self.xy[1] / scale))
                adb.input.tap(xy=self.xy)  # 点击
                return self.clicked
            if self.clicked == 'right':
                cv2.destroyAllWindows()
                return self.clicked

    def get_multi_position(self, img, image_name=None, scale=1):
        image_name = 'image' if image_name is None else image_name
        if isinstance(img, str):
            assert os.path.exists(img), f'img: {img} does not exists.'
            print(f'read image: {img}')
            img = cv2.imread(img)

        print(f'image shape: {img.shape}')
        h, w, c = img.shape
        nw, nh = (int(scale * w), int(scale * h))
        img = cv2.resize(img, (nw, nh))
        self.clicked = False
        self.xy = None
        while True:
            # print(f'sctime: {(time.time() - t) * 1000:.2f}')

            cv2.namedWindow(image_name)
            cv2.setMouseCallback(image_name, self.on_mouse)
            cv2.imshow(image_name, img)
            # if cv2.waitKey(1) == ord('q') or self.clicked == 'left':
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                return self.clicked
            if self.clicked == 'left':
                if scale is not None:  # scale back
                    self.xy = (int(self.xy[0] / scale), int(self.xy[1] / scale))
                print(f'left cliked: xy: {self.xy}')
                self.clicked = False
            if self.clicked == 'right':
                cv2.destroyAllWindows()
                return self.clicked

    def __call__(self, img, image_name=None, scale=None):
        """只是基本的点击功能"""
        if isinstance(img, str):
            assert os.path.exists(img), f'img: {img} does not exists.'
            img = cv2.imread(img)
        image_name = 'image' if image_name is None else image_name
        if scale is not None:
            h, w, c = img.shape
            img = cv2.resize(img, (int(scale*w), int(scale*h)))

        self.xy = None
        self.clicked = False
        cv2.namedWindow(image_name)
        cv2.setMouseCallback(image_name, self.on_mouse)
        cv2.imshow(image_name, img)
        while True:
            if cv2.waitKey(1) == ord('q') or self.clicked:
                cv2.destroyAllWindows()
                break
        if scale is not None:  # scale back
            self.xy = (int(self.xy[0]/scale), int(self.xy[1]/scale))
        return self.xy


def main(argv):
    del argv
    mi = MouseImage()
    # xy = mi(img=FLAGS.img, scale=0.5)
    cliked = mi.get_multi_position(img=FLAGS.img, scale=FLAGS.scale)
    print(f'{cliked} clicked: {mi.xy}')


if __name__ == '__main__':
    app.run(main)