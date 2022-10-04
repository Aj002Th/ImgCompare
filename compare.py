from paddleocr import PaddleOCR
from PIL import Image
from PIL import ImageDraw
from string import punctuation as punctuationEnglish
from zhon.hanzi import punctuation as punctuationChinese
import re

ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def print_diff(i, origin, origin_text, scan, scan_text):
    print(f'file: {origin}')
    print(f'data: {origin_text}')
    print(f'file: {scan}')
    print(f'data: {scan_text}')
    print(f'i: {i}')
    print()

def compare(origin, scan, save):
    """核心函数, 实现两图片文字内容的比对分析以及结果输出"""
    origin_result = ocr.ocr(origin, cls=True)
    scan_result = ocr.ocr(scan, cls=True)

    # 去除空格、中英文符号
    for xx in origin_result:
        xx[1] = str.replace(xx[1][0], ' ', '')
        xx[1] = re.sub(r'[{}]+'.format(punctuationEnglish),'',xx[1])
        xx[1] = re.sub(r'[{}]+'.format(punctuationChinese),'',xx[1])
    for xx in scan_result:
        xx[1] = str.replace(xx[1][0], ' ', '')
        xx[1] = re.sub(r'[{}]+'.format(punctuationEnglish),'',xx[1])
        xx[1] = re.sub(r'[{}]+'.format(punctuationChinese),'',xx[1])


    # 识别内容->存储数组的index 的映射.
    scan_set = {}
    origin_set = {}
    for i in range(len(origin_result)):
        if origin_result[i][1] in origin_set:
            origin_set[origin_result[i][1]].append(i)
        else:
            origin_set[origin_result[i][1]] = [i]
    for i in range(len(scan_result)):
        if scan_result[i][1] in scan_set:
            scan_set[scan_result[i][1]].append(i)
        else:
            scan_set[scan_result[i][1]] = [i]


    diff_pos_org = []
    diff_pos_scan = []
    # 检查是否有对应的相同字符
    for xx in origin_result:
        if xx[1] not in scan_set:
            diff_pos_org.append(xx[0])
            print(xx)
        else:
            # 位置差异太大也要标注出来
            mn = 1000
            for i in scan_set[xx[1]]:
                yy = scan_result[i]
                mn = min(mn, abs(xx[0][0][0] - yy[0][0][0]) + abs(xx[0][0][1] - yy[0][0][1]))
            if mn > 100:
                diff_pos_org.append(xx[0])
    for xx in scan_result:
        if xx[1] not in origin_set:
            diff_pos_scan.append(xx[0])
            print(xx)
        else:
            # 位置差异太大也要标注出来
            mn = 1000
            for i in origin_set[xx[1]]:
                yy = origin_result[i]
                mn = min(mn, abs(xx[0][0][0] - yy[0][0][0]) + abs(xx[0][0][1] - yy[0][0][1]))
            if mn > 100:
                diff_pos_scan.append(xx[0])

    # 打印内容
    img_origin = Image.open(origin)
    img_draw_origin = ImageDraw.ImageDraw(img_origin)
    img_scan = Image.open(scan)
    img_draw_scan = ImageDraw.ImageDraw(img_scan)

    for diff in diff_pos_scan:
        img_draw_scan.rectangle((diff[0][0], diff[0][1], diff[2][0], diff[2][1]), fill=None, outline='red', width=3)
    for diff in diff_pos_org:
        img_draw_origin.rectangle((diff[0][0], diff[0][1], diff[2][0], diff[2][1]), fill=None, outline='red', width=3)

    result = Image.new("RGB", (img_origin.size[0] + img_scan.size[0], img_origin.size[1]))
    loc1, loc2 = (0, 0), (img_origin.size[0], 0)
    result.paste(img_origin, loc1)
    result.paste(img_scan, loc2)
    result.save(save + 'result.jpg')

# 直接运行 compare.py 可处理 img 中所有图片比对任务
if __name__ == "__main__":
    target_dir = ['南京银行录音设备', '宁波影像设备采购', '上海市分行验印摄像仪', '深圳分行验印', '信用合作清算中心验印', '亚太财险']
    img_filename = ['1', '2', '3', '4', '5']
    for t_dir in target_dir:
        for i_name in img_filename:
            origin = './img/' + t_dir + '/origin/' + i_name + '.jpg'
            scan = './img/' + t_dir + '/scan/' + i_name + '.JPG'
            save = './img/' + t_dir + '/' + i_name
            compare(origin, scan, save)