import streamlit as st
import os
import tempfile
from ppt_translator import PPTTranslator
import logging

# 配置页面
st.set_page_config(
    page_title="PPT 翻译工具",
    page_icon="📊",
    layout="centered"
)

# 设置日志
logging.basicConfig(level=logging.INFO)

# 在文件顶部添加
PPTX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

def main():
    st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            margin-top: 1rem;
        }
        .stProgress>div>div>div {
            background-color: #1f77b4;
        }
        .upload-text {
            text-align: center;
            padding: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📊 PPT 翻译工具")
    st.write("上传 PowerPoint 文件，选择目标语言，即可获得翻译后的文件。")
    
    # API key 从 secrets 获取或通过输入框
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "sk-dcd365bbbb254548b0624ed78c5ae504")  # 设置默认值

    # 文件上传
    uploaded_file = st.file_uploader(
        "上传 PPT 文件",
        type=["pptx"],
        help="请上传 .pptx 格式的文件"
    )
    
    # 语言选择
    languages = {
        "中文": "zh-CN",
        "英语": "en",
        "日语": "ja",
        "韩语": "ko",
        "法语": "fr",
        "德语": "de",
        "西班牙语": "es",
        "俄语": "ru"
    }
    target_language = st.selectbox(
        "选择目标语言",
        options=list(languages.keys()),
        format_func=lambda x: x
    )
    
    # 添加开始翻译按钮
    if uploaded_file:  # 只要有文件上传就显示按钮
        if st.button("开始翻译", type="primary", key="translate_button"):
            try:
                # 创建进度条
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 创建临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pptx') as temp_input:
                    temp_input.write(uploaded_file.getvalue())
                    input_path = temp_input.name
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pptx') as temp_output:
                    output_path = temp_output.name
                
                # 初始化翻译器
                translator = PPTTranslator(api_key=api_key)
                
                # 更新状态
                status_text.text("正在提取文本...")
                progress_bar.progress(20)
                
                # 执行翻译
                translator.translate_ppt(
                    input_path=input_path,
                    output_path=output_path,
                    target_lang=languages[target_language]
                )
                
                # 更新进度
                progress_bar.progress(100)
                status_text.text("翻译完成！")
                
                # 提供下载
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 下载翻译后的文件",
                        data=file,
                        file_name=f"translated_{uploaded_file.name}",
                        mime=PPTX_MIME_TYPE,
                        key="download_button"
                    )
                    
            except Exception as e:
                st.error(f"翻译过程中出现错误: {str(e)}")
                
            finally:
                # 清理临时文件
                try:
                    os.unlink(input_path)
                    os.unlink(output_path)
                except:
                    pass

if __name__ == "__main__":
    main() 
