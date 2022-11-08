import cv2 as cv2
import io as io
import multiprocessing as multiprocessing
import numpy as numpy

from kikiutils.check import isfile, isstr
from kikiutils.image import cmp_image_sim, get_image
from PIL import Image as Image


class Dun360:
    def __init__(
        self,
        bg_image: Image.Image | io.BytesIO | io.FileIO | bytes | str,
        slide_image: Image.Image | io.BytesIO | io.FileIO | bytes | str,
        multiprocessing_use_cpu: int = multiprocessing.cpu_count(),
        use_multiprocessing: bool = True
    ):
        if isstr(bg_image) and not isfile(bg_image):
            bg_image = get_image(bg_image)

        if isstr(slide_image) and not isfile(slide_image):
            slide_image = get_image(slide_image)

        if not getattr(bg_image, 'convert', False):
            bg_image = Image.open(bg_image).convert('RGB')

        if not getattr(slide_image, 'convert', False):
            slide_image = Image.open(slide_image, formats=['png'])

        self.bg_image = bg_image
        self.slide_image = slide_image
        self.mp_use_cpu = multiprocessing_use_cpu
        self.use_mp = use_multiprocessing

    def crop_bg_and_cmp_slide_image(
        self,
        bg_image: Image.Image,
        slide_dst_image: cv2.Mat,
        dx: int,
        w2: int,
        h2: int
    ):
        crop_image = bg_image.crop((dx, 0, dx + w2, h2))
        crop_cv2_image = cv2.cvtColor(
            numpy.array(crop_image),
            cv2.COLOR_RGB2GRAY
        )

        crop_dst_image = cv2.Canny(crop_cv2_image, 100, 200)
        pasted_image = cv2.add(crop_dst_image, slide_dst_image)
        sim_value = cmp_image_sim(
            crop_dst_image, pasted_image,
            resize_image=False
        )

        return {
            sim_value: dx
        }

    def get_slide_move_x(self):
        bg_image = self.bg_image.copy()
        slide_image = self.slide_image.copy()

        W1, H1 = bg_image.size
        W2, H2 = slide_image.size

        # Change slide image pixel is transparent to 0, 0, 0, 0 (RGBA)
        # If pixel is not transparent, change to 255, 255, 255, 255 (RGBA)
        for w in range(W2):
            for h in range(H2):
                R, G, B, A = slide_image.getpixel((w, h))

                if R == G == 255 or A == 0:
                    slide_image.putpixel((w, h), (0, 0, 0, 0))
                else:
                    slide_image.putpixel((w, h), (255, 255, 255, 255))

        # Get slide image bbox position and crop
        box_pos = slide_image.getbbox()
        box_pos = (
            box_pos[0] - 5,
            box_pos[1] - 5,
            box_pos[2] + 5,
            box_pos[3] + 5
        )

        bg_image = bg_image.crop((0, box_pos[1], W1, box_pos[3]))
        slide_image = slide_image.crop(box_pos)

        # Get resized bg and slide image width and height
        W1, H1 = bg_image.size
        W2, H2 = slide_image.size

        # Use cv2.Canny to process croped slide image
        slide_cv2_image = cv2.cvtColor(
            numpy.array(slide_image),
            cv2.COLOR_RGB2GRAY
        )

        slide_dst_image = cv2.Canny(slide_cv2_image, 100, 200)
        sim_results = {}

        # Crop bg image and add slide dst image, then cmp crop and pasted image hash
        if self.use_mp:
            pool = multiprocessing.Pool(self.mp_use_cpu)
            args = []

            for dx in range(W1 - W2):
                args.append((bg_image, slide_dst_image, dx, W2, H2))

            result = pool.starmap(self.crop_bg_and_cmp_slide_image, args)
            pool.close()
            pool.join()

            # Get max sim value and dx
            for r in result:
                sim_results.update(r)
        else:
            for dx in range(W1 - W2):
                r = self.crop_bg_and_cmp_slide_image(
                    bg_image,
                    slide_dst_image,
                    dx,
                    W2,
                    H2
                )

                sim_results.update(r)

        sim_list = list(sim_results.keys())
        sim_list.sort()

        max_sim_value = sim_list[-1]
        max_sim_dx = sim_results[max_sim_value] + 5

        return {
            'bgImageWidth': W1,
            'maxSim': max_sim_value,
            'maxSimDx': max_sim_dx,
            'slideBoxStartX': box_pos[0] + 5
        }
