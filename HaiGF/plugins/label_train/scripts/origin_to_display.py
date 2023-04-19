from PIL import Image
import os

def transpose_image(image_path, save_path):
    image = Image.open(image_path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    # image = image.transpose(Image.FLIP_LEFT_RIGHT)
    image.save(save_path)

def transpose_images(image_dir, save_dir):
    for image_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_name)
        save_path = os.path.join(save_dir, image_name)
        print(image_path, save_path)
        transpose_image(image_path, save_path)



if __name__ == '__main__':
    image_dir = 'D:/bubbleImage/origin_image'
    save_dir = 'D:/bubbleImage/pre_image'
    transpose_images(image_dir, save_dir)