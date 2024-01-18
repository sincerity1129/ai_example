import streamlit as st
from PIL import Image
import jwt
import bcrypt
import os 

from config.basic import demo
from handlers import Logger
from facefusion import core 
from facefusion.streamlit_controller import image_resize, image_save, video_save

logging = Logger.set_logger(log_name='Server', filename='logs/streamlit.log')

source_image=None
target_image=None    
target_video=None  
image_url=None
result_video=None
mode_selected = None

st.set_page_config(page_title="Face Fusion", layout='wide')

_, title,_ = st.columns([1.4,1.0,1.0])
with title:
    st.title("Face Fusion")
#     if not 'login' in st.session_state:
#         st.session_state['id'] = st.text_input("ID를 입력하세요")
#         st.session_state['password'] = st.text_input("발급된 TOKEN를 입력하세요(다음으로 넘어가지 않으면 로그인 실패)")

# user_password = bcrypt.hashpw(st.session_state['password'].encode("utf-8"), bcrypt.gensalt())
# if bcrypt.checkpw(st.session_state['password'].encode('utf-8'), user_password):
# logging.info(f"접속아이디: {st.session_state['id']}")
st.session_state['login'] = 'success'
_, mode_selected_col,_ = st.columns([1.2,1.0,1.0])
with mode_selected_col:
    mode_selected_item = st.selectbox('face_swapper(default), face_swapper+face_enhancer', 
    ("=================Mode Select=================", "face_swapper", "face_swapper+face_enhancer"))
    if mode_selected_item == "face_swapper":
        mode_selected = "face_swapper"
    elif mode_selected_item == "face_swapper+face_enhancer":
        mode_selected = "face_enhancer"

if mode_selected:
    source_col, _,target_col = st.columns([1.0,0.3,1.0])
    with source_col:
        st.header("Source Image Load")
        source_selected_item = st.selectbox('Source 파일 또는 URL 선택하세요', 
        ("=====================Upload 유형 선택=====================", "Image File", "Image Url"))
        if source_selected_item == "Image File":
            source_image = source_col.file_uploader("Source Upload File", type=["png", "jpg", "jpeg"])

        elif source_selected_item == "Image Url":
            image_url = st.text_input("Source Image URL Select")
            if image_url:
                source_image = image_save(image_url)
    with target_col:
        st.header("Target Image Load")
        target_selected_item = st.selectbox('Target 파일 또는 URL 선택하세요', 
        ("=====================Upload 유형 선택=====================", "Image File", "Image Url"))
        # ("=====================Upload 유형 선택=====================", "Image File","Video File", "Image Url"))
        if target_selected_item == "Image File":
            target_image = target_col.file_uploader("Target image Upload File", type=["png", "jpg", "jpeg"])
        elif target_selected_item == "Image Url":
            image_url = st.text_input("Target Image URL Select")
            if image_url:
                target_image = image_save(image_url)
        # elif target_selected_item == "Video File":
        #     target_video = target_col.file_uploader("Target video Upload File", type=["avi", "mp4"])
            

if source_image and target_image:
    source_image_col, _, target_image_col = st.columns([0.7,1.0,0.7])
    with source_image_col:
        st.header("Source Image")
        image_source=Image.open(source_image)
        width,height = image_resize(image_source)
        image_source_resize=image_source.resize((width,height))
        if source_selected_item =="Image Url":
            image_source_save_path = source_image.split(".")[0] + ".jpg"
            source_name = source_image.split(".")[0]
        else:    
            image_source_save_path=os.path.join(demo['input_root_path'],source_image.name)
            source_name = source_image.name.split(".")[0]
        image_source.save(image_source_save_path)
        source_image_col.image(image_source_resize)

    with target_image_col:
        st.header("Target Image")
        image_target=Image.open(target_image)
        width,height = image_resize(image_target)
        image_target_resize=image_target.resize((width,height))
        if target_selected_item =="Image Url":
            image_target_save_path = target_image.split(".")[0] + ".jpg"
            target_name = target_image.split("/")[-1].split(".")[0] + ".jpg"
        else:
            image_target_save_path=os.path.join(demo['input_root_path'],target_image.name)
            target_name = target_image.name
        image_target.save(image_target_save_path)
        target_image_col.image(image_target_resize)
        
    _, result_image_col, _ = st.columns([0.7,1.0,0.7])
    with result_image_col:
        core.cli(image_source_save_path, image_target_save_path, face_enhancer_mode=mode_selected)
        st.header("Face Swap Result Image")
        output_path = os.path.join(demo['output_path'], f"{source_name}-{target_name}")
        result_image_col.image(output_path, width=600)


# video controller GPU 쓸 때만            
# if source_image:
#     source_image_col, _, _ = st.columns([0.7, 0.5, 1.0])
#     with source_image_col:
#         st.header("Source Image")
#         image_source=Image.open(source_image)
#         width,height = image_resize(image_source)
#         image_source_resize=image_source.resize((width,height))
#         if source_selected_item =="Image Url":
#             image_source_save_path = source_image.split(".")[0] + ".jpg"
#             source_name = source_image.split(".")[0]
#         else:    
#             image_source_save_path=os.path.join(demo['input_root_path'],source_image.name)
#             source_name = source_image.name.split(".")[0]
#         image_source.save(image_source_save_path)
        # source_image_col.image(image_source_resize)

    # with target_video_col:
    #     st.header("Source Video")
    #     image_target_origin_path = os.path.join(demo['origin_root_path'],target_video.name)
    #     image_target_save_path=os.path.join(demo['input_root_path'],target_video.name)
    #     video_save(target_video, image_target_save_path)
    #     target_video_name = target_video.name.split(".")[0]
    #     st.video(target_video, format="video/mp4")

    # _, result_image_col, _ = st.columns([0.7,1.0,0.7])
    # with result_image_col:
    #     core.cli(image_source_save_path, image_target_save_path, mode_selected)
    #     st.header("Face Swap Result Video")
    #     output_path = os.path.join(demo['output_path'],f"{source_name}-{target_video_name}.mp4")
    #     result_image_col.video(output_path, format="video/mp4")
