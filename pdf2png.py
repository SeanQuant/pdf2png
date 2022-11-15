import fitz
import os
from PIL import Image


def pdf2png(filename, page_num=None, size_factor=1,):
    print(filename)
    png_filename = filename[:filename.rindex(".pdf")] + ".png"

    zoom_x, zoom_y = size_factor, size_factor
    png_list = []
    sub_png_list = []
    pdf = fitz.open(filename)

    width, height = 0, 0
    mode = None  # as flag

    if isinstance(page_num, int):
        page_num = [page_num, ]
    elif isinstance(page_num, (tuple, list)):
        pass
    else:
        page_num = []

    for i, page in enumerate(pdf.pages()):
        if i in page_num:
            trans = fitz.Matrix(zoom_x, zoom_y)
            pm = page.get_pixmap(matrix=trans, alpha=False)

            sub_filename = png_filename + "-%d.png" % i
            pm.save(sub_filename)

            png = Image.open(sub_filename)
            png_list.append(png)

            if mode is None:
                mode = png.mode

            width = max(width, png.width)
            height += png.height
            sub_png_list.append(sub_filename)

    if mode is None:
        return False

    result = Image.new(mode, (width, height))
    count_height = 0
    for i, png in enumerate(png_list):
        result.paste(png, box=(0, count_height))  # 左对齐
        count_height += png.height
    result.save(png_filename)
    for sub_f in sub_png_list:
        os.remove(sub_f)
    return True


if __name__ == '__main__':
    filename = "./phycs2018.pdf"
    pdf2png(filename, page_num=(0, 1, 2))  # 将上述pdf的第0,1,2页转成图片(拼在一起)
