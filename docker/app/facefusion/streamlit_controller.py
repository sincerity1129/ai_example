import requests
import os
import io

from config.basic import demo

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'}

def image_resize(image):
    if image.size[0] >= image.size[1]:
        ratio = image.size[1] / image.size[0]
        width = 500
        height = int(500*ratio)
    else:
        ratio = image.size[0] / image.size[1]
        width = int(500*ratio)
        height = 500
    return width, height

def image_save(url):
    file_name=url.split("/")[-1]
    save_path = os.path.join(demo['input_root_path'], file_name)
    response = requests.get(url, headers=HEADERS)
    with open(save_path, "wb") as outfile:
        outfile.write(response.content)
    return save_path

def video_save(read_path, save_path):
    target_video_byte = io.BytesIO(read_path.read())
    with open(save_path, 'wb') as out:
        out.write(target_video_byte.read())
        
def remove_file(remove_path):
    # 폴더 안의 모든 파일 리스트 가져오기
    file_list = os.listdir(remove_path)

    # 폴더 안의 모든 파일 삭제
    for file_name in file_list:
        file_path = os.path.join(remove_path, file_name)

        if os.path.isfile(file_path):
            os.remove(file_path)