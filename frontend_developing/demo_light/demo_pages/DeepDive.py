import streamlit as st
import os
import base64

script_dir = os.path.dirname(os.path.abspath(__file__))
wiki_root_dir = os.path.dirname(os.path.dirname(script_dir))


def deepdive_page():
    # 添加CSS来减少页面顶部的空白
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        header {
            visibility: hidden;
        }
        #MainMenu {
            visibility: hidden;
        }
        footer {
            visibility: hidden;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    if "index" not in st.session_state:
        st.session_state["index"] = 3
    # 1) Initialize session state for the papers list if not already present
    if "papers" not in st.session_state:
        st.session_state["papers"] = [
            {
                "title": "Sample Paper 1",
                "abstract": "This is the abstract for paper 1...",
            },
            {
                "title": "Sample Paper 2",
                "abstract": "This is the abstract for paper 2...",
            },
            {
                "title": "Sample Paper 3",
                "abstract": "This is the abstract for paper 3...",
            },
        ]

    # # 1) Initialize message list if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "你好有什么关于Paper的问题想问我吗？"},
            {"role": "user", "content": "你好，我想问一下关于Paper的问题。"},
            {"role": "assistant", "content": "好的，有什么问题可以问我。"},
        ]

    # 2) Create three columns
    col1, col2, col3 = st.columns([1.7, 5, 4])
    with col1:
        papers_container = st.container()

        with papers_container:
            # 2) Add a source button, red background with white text
            st.markdown(
                """
                <style>
                .stButton>button {
                    background-color: #F62266;
                    color: white;
                    font-weight: 500;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 5px;
                }
                .stButton>button:active,
                .stButton>button:focus {
                    background-color: #F62266 !important;
                    color: white !important;
                    border: none !important;
                    outline: none !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            add_source_button = st.button("Add Source")
            if add_source_button:
                # index += 1
                st.session_state["index"] = st.session_state["index"] + 1
                st.session_state["papers"].append(
                    {
                        "title": "Sample Paper " + str(st.session_state["index"]),
                        "abstract": "This is the abstract for the new source...",
                    }
                )

            # 3) Render the updated papers list
            for paper in st.session_state["papers"]:
                paper_box = st.container()
                with paper_box:
                    html = f"""
                    <style>
                    .paper-container {{
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        margin: 5px 8px 5px 0px;
                        cursor: pointer;
                        position: relative;
                        transition: all 0.3s ease;
                    }}
                    .paper-container:hover {{
                        background-color: #f0f0f0;
                    }}
                    .paper-abstract {{
                        display: none;
                        position: absolute;
                        left: 105%;
                        top: 0;
                        width: 250px;
                        background-color: white;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        padding: 10px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                        z-index: 100;
                    }}
                    .paper-container:hover .paper-abstract {{
                        display: block;
                    }}
                    </style>
                    <div class="paper-container" 
                    onmousedown="this.style.backgroundColor='#e0e0e0'"
                    onmouseup="this.style.backgroundColor='#f0f0f0'"
                    onmouseleave="this.style.backgroundColor='transparent'">
                        <p style="margin: 0;">{paper['title']}</p>
                        <div class="paper-abstract">
                            <p><strong>Abstract:</strong></p>
                            <p>{paper['abstract']}</p>
                        </div>
                    </div>
                    """
                    st.markdown(html, unsafe_allow_html=True)
    # --------------------------
    # Middle Column (col2) - Chat
    # --------------------------
    with col2:
        # Add CSS for chat container
        st.markdown(
            """
            <style>
            .chat-container {
                height: 80vh;  /* 80% of viewport height */
                display: flex;
                flex-direction: column;
                border: 0.2px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                position: relative;
            }
            .chat-history {
                flex-grow: 1;
                overflow-y: auto;
                padding: 0px;
                margin-bottom: 60px; /* Space for the input */
            }
            .chat-input-container {
                position: absolute;
                bottom: 10px;
                left: 10px;
                right: 10px;
                padding: 10px;
                background-color: white;
            }
            .stChatInputContainer {
                position: fixed;
                bottom: 20px;
                width: calc(5/10.7 * 100%);
                background-color: white;
                padding: 0px;
                z-index: 1000;
                border-top: 1px solid #eee;
            }
            .stChatInput textarea {
                min-height: 100px !important;
                height: 100px !important;
                max-height: 100px !important;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        # 创建一个容器来包含整个聊天界面
        chat_container = st.container()

        # 在容器内创建聊天历史和输入框
        with chat_container:
            chat_history = st.container(height=610)
            with chat_history:
                for message in st.session_state["messages"]:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            # 聊天输入区域
            prompt = st.chat_input("Ask a question about the papers...")

        # Handle new user input
        if prompt:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Add a dummy assistant response
            response = f"This is a dummy response to your question: '{prompt}'"
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()  # 重新渲染页面

    # --------------------------
    # Right Column (col3)
    # --------------------------
    with col3:

        st.subheader("Panel Podcast")

        # Load and display the audio file
        audio_file_path = os.path.join(
            script_dir, "Don't Transform the Code, Code the Transforms.mp3"
        )
        st.caption("Paper: Don't Transform the Code, Code the Transforms")

        if os.path.exists(audio_file_path):
            audio_file = open(audio_file_path, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
        else:
            st.error(f"Audio file not found at: {audio_file_path}")

        st.subheader("DeepDive")
        # 确保图片路径是绝对路径
        image_file_path = os.path.join(script_dir, "test_markdown_diagram.png")

        # 检查图片是否存在
        if os.path.exists(image_file_path):
            # 读取图片并转换为base64
            with open(image_file_path, "rb") as img_file:
                img_bytes = img_file.read()
                encoded_img = base64.b64encode(img_bytes).decode()

            # 使用base64编码的图片在Markdown中
            sample_markdown = f"""
            #### Methodology
            The key innovation is the chain-of-thought process, where the model:

            ###### Generates a Natural Language Description:
            Given a few input/output code examples, the LLM is prompted to describe in natural language the underlying transformation. This step helps the model explicitly consider edge cases and nuances.

            ###### Iterative Refinement:
            The description is iteratively refined—up to 10 times—so that the model can correct its understanding and cover all required cases.

            ![Sample Image](data:image/png;base64,{encoded_img})
            ###### Synthesizing the Transform:
            Once a satisfactory description is produced, it is used along with the examples to generate a transformation function (e.g., an Abstract Syntax Tree (AST) rewrite function in Python).

            ###### Execution and Feedback Loop:
            The synthesized transform is executed on several examples (both seen and unseen). If the output is incorrect or an error is encountered, the model receives feedback (including error messages or counterexamples) and enters a further introspection phase to diagnose and correct the error.

            ###### Iteration Until Success:
            This loop continues—up to a maximum of 50 iterations—until the transformation function works correctly on all test cases.
            For more details, see [the full paper](https://arxiv.org/pdf/2410.08806).
            """
        else:
            sample_markdown = f"""
            ## Paper Summary
            
            This paper introduces a novel approach to code transformation.
            
            [Image not found: {image_file_path}]
            
            ### Key Points:
            
            * Point 1: Lorem ipsum dolor sit amet
            * Point 2: Consectetur adipiscing elit
            * Point 3: Sed do eiusmod tempor incididunt
            
            > "Important quote from the paper that highlights the main contribution."
            
            For more details, see [the full paper](https://arxiv.org/pdf/2410.08806).
            """
        analysis_container = st.container(height=500)
        with analysis_container:
            st.markdown(sample_markdown, unsafe_allow_html=True)
