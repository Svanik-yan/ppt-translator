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
            background-color: #FF4B4B;
            color: white;
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
    
    # API key 设置为默认值
    api_key = "sk-dcd365bbbb254548b0624ed78c5ae504"
    
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
        options=list(languages.keys())
    )
    
    # 翻译按钮
    translate_button = st.button(
        "开始翻译",
        type="primary",
        key="translate_button",
        disabled=not uploaded_file  # 只有上传文件后才能点击
    )
    
    if uploaded_file and translate_button:
        try:
            # 创建状态显示区域
            col1, col2 = st.columns([3, 1])
            with col1:
                status_text = st.empty()
                progress_text = st.empty()
                progress_bar = st.progress(0)
            with col2:
                percentage_text = st.empty()
            
            # 显示初始状态
            status_text.text("🚀 准备开始翻译...")
            progress_bar.progress(0)
            percentage_text.markdown("<h2 style='text-align: right'>0%</h2>", unsafe_allow_html=True)
            
            # 创建临时文件
            status_text.text("📂 正在处理上传文件...")
            progress_bar.progress(10)
            percentage_text.markdown("<h2 style='text-align: right'>10%</h2>", unsafe_allow_html=True)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pptx') as temp_input:
                temp_input.write(uploaded_file.getvalue())
                input_path = temp_input.name
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pptx') as temp_output:
                output_path = temp_output.name
            
            # 初始化翻译器
            status_text.text("🔧 正在初始化翻译器...")
            progress_bar.progress(20)
            percentage_text.markdown("<h2 style='text-align: right'>20%</h2>", unsafe_allow_html=True)
            translator = PPTTranslator(api_key=api_key)
            
            # 提取文本
            status_text.text("📄 正在提取 PPT 文本...")
            progress_bar.progress(30)
            percentage_text.markdown("<h2 style='text-align: right'>30%</h2>", unsafe_allow_html=True)
            
            # 设置翻译进度回调函数
            def translation_progress_callback(current, total):
                progress = int(30 + (current / total) * 40)  # 30-70% 用于翻译过程
                progress_bar.progress(progress)
                percentage_text.markdown(f"<h2 style='text-align: right'>{progress}%</h2>", unsafe_allow_html=True)
                progress_text.markdown(f"""
                    <div style='padding: 10px; border-radius: 5px; background-color: #f0f2f6'>
                        📊 翻译进度: {current}/{total} 个文本片段 ({int(current/total*100)}%)
                    </div>
                """, unsafe_allow_html=True)
            
            # 执行翻译
            status_text.text("🌐 正在翻译文本...")
            translator.translate_ppt(
                input_path=input_path,
                output_path=output_path,
                target_lang=languages[target_language],
                progress_callback=translation_progress_callback
            )
            
            # 保存文件
            status_text.text("💾 正在生成翻译后的 PPT...")
            progress_bar.progress(90)
            percentage_text.markdown("<h2 style='text-align: right'>90%</h2>", unsafe_allow_html=True)
            
            # 完成
            progress_bar.progress(100)
            percentage_text.markdown("<h2 style='text-align: right'>100%</h2>", unsafe_allow_html=True)
            status_text.markdown("✅ **翻译完成！**")
            progress_text.empty()
            
            # 提供下载
            with open(output_path, "rb") as file:
                st.success("🎉 文件已准备就绪，请点击下方按钮下载！")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="📥 下载翻译后的文件",
                        data=file,
                        file_name=f"translated_{uploaded_file.name}",
                        mime=PPTX_MIME_TYPE,
                        key="download_button",
                        use_container_width=True,
                    )
                
        except Exception as e:
            st.error(f"❌ 翻译过程中出现错误: {str(e)}")
            status_text.markdown("🚫 **翻译失败**")
            progress_text.empty()
            
        finally:
            # 清理临时文件
            try:
                os.unlink(input_path)
                os.unlink(output_path)
            except:
                pass

if __name__ == "__main__":
    main() 
