import json
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import pandas as pd

def save_markdown_report(markdown_text, output_file="conference_daily_report.md"):
    """
    将Markdown文本保存到文件
    
    Args:
        markdown_text (str): Markdown格式的文本
        output_file (str): 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_text)
    print(f"每日参会快报已保存到 {output_file}")


def generate_daily_conference_report(df):
    """
    根据DataFrame生成每日参会快报的Markdown格式文本
    
    Args:
        df (DataFrame): 包含会议数据的DataFrame
        
    Returns:
        str: Markdown格式的每日参会快报
    """
    # 获取第一行的日期作为大标题
    date = df.iloc[0]['Date'] if 'Date' in df.columns else "会议快报"
    
    # 创建Markdown文本
    markdown_text = f"# {date}每日参会快报\n\n"
    
    # 遍历每一行生成报告内容
    for _, row in df.iterrows():
        title = row.get('Title', '未知标题')
        session_type = row.get('Session Type', '未知会话类型')
        
        # 优先使用Expert Insight merged，如果没有则使用Expert Insight
        insight = row.get('Expert Insight merged', '')
        if (pd.isna(insight) or (isinstance(insight, str) and insight.isspace())) and 'Expert Insight' in row:
            insight = row['Expert Insight']
            print("insightinsightinsightinsightinsightinsightinsightinsightinsightinsightinsightinsight")
            print(insight)
            try:
                insight_data = json.loads(insight)
                if isinstance(insight_data, list):
                    insight = "\n".join([f"- {item}" for item in insight_data])
            except:
                pass
        
        # 处理撰稿人格式
        composer = row.get('Composer', '')
        formatted_composer = format_composer(composer)
        
        # 处理关键人物或公司信息
        speakers = row.get('Speaker', '')
        formatted_speakers = format_speakers(speakers)
        
        # 添加到Markdown文本
        markdown_text += f"## 【{session_type}】{title}\n\n"
        markdown_text += f"### 关键人物或公司\n{formatted_speakers}\n\n"
        markdown_text += f"### 洞察观点\n{insight}\n\n"
        markdown_text += f"撰稿人：{formatted_composer}\n\n"
        markdown_text += "---\n\n"
    
    return markdown_text


def generate_daily_conference_word(df, output_file="conference_daily_report.docx"):
    """
    根据DataFrame生成每日参会快报的Word文档
    
    Args:
        df (DataFrame): 包含会议数据的DataFrame
        output_file (str): 输出的Word文件路径
    """
    doc = Document()
    
    # 获取第一行的日期作为大标题
    date = df.iloc[0]['Date'] if 'Date' in df.columns else "会议快报"
    
    # 添加大标题
    title = doc.add_heading(f"{date}每日参会快报", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 遍历每一行生成报告内容
    for _, row in df.iterrows():
        title = row.get('Title', '未知标题')
        session_type = row.get('Session Type', '未知会话类型')
        
        # 添加小标题
        doc.add_heading(f"【{session_type}】{title}", level=1)
        
        # 处理关键人物或公司信息
        speakers = row.get('Speaker', '')
        formatted_speakers = format_speakers(speakers)
        
        # 添加关键人物或公司段落
        doc.add_heading("关键人物或公司", level=2)
        doc.add_paragraph(formatted_speakers)
        
        # 添加洞察观点
        doc.add_heading("洞察观点", level=2)
        insight = row.get('Expert Insight merged', '')
        if (pd.isna(insight) or (isinstance(insight, str) and insight.isspace())) and 'Expert Insight' in row:
            insight = row['Expert Insight']
            try:
                insight_data = json.loads(insight)
                if isinstance(insight_data, list):
                    insight = "\n".join([f"• {str(item)}" for item in insight_data])
            except:
                pass
        
        # 确保 insight 是字符串类型
        insight = str(insight) if insight is not None else ""
        doc.add_paragraph(insight)
        
        # 处理撰稿人
        composer = row.get('Composer', '')
        formatted_composer = format_composer(composer)
            
        # 添加撰稿人
        composer_para = doc.add_paragraph("撰稿人：")
        composer_para.add_run(formatted_composer)
        
        # 添加分隔线
        doc.add_paragraph("_" * 40)
    
    # 保存文档
    doc.save(output_file)
    print(f"Word格式的每日参会快报已保存到 {output_file}")


def format_composer(composer):
    """
    格式化撰稿人信息
    
    Args:
        composer: 原始撰稿人数据
        
    Returns:
        str: 格式化后的撰稿人字符串
    """
    formatted_composer = ""
    if composer:
        try:
            composer_data = json.loads(composer) if isinstance(composer, str) else composer
            if isinstance(composer_data, list):
                composer_items = []
                for person in composer_data:
                    if isinstance(person, dict):
                        name = person.get('name', '')
                        id_num = person.get('id', '')
                        if name and id_num:
                            composer_items.append(f"{name} {id_num}")
                formatted_composer = "、".join(composer_items)
            elif isinstance(composer_data, dict):
                name = composer_data.get('name', '')
                id_num = composer_data.get('id', '')
                if name and id_num:
                    formatted_composer = f"{name} {id_num}"
        except:
            formatted_composer = composer
    
    return formatted_composer if formatted_composer else "未知撰稿人"


def format_speakers(speakers):
    """
    格式化演讲者信息
    
    Args:
        speakers: 原始演讲者数据
        
    Returns:
        str: 格式化后的演讲者字符串
    """
    formatted_speakers = "无"
    if speakers:
        try:
            speaker_data = json.loads(speakers) if isinstance(speakers, str) else speakers
            if isinstance(speaker_data, list):
                speaker_items = []
                for person in speaker_data:
                    if isinstance(person, dict):
                        name = person.get('name', '')
                        position = person.get('position', '')
                        company = person.get('company', '')
                        
                        other_info = []
                        if position:
                            other_info.append(position)
                        if company:
                            other_info.append(company)
                        
                        if name:
                            if other_info:
                                speaker_items.append(f"{name}（{', '.join(other_info)}）")
                            else:
                                speaker_items.append(name)
                
                if speaker_items:
                    formatted_speakers = "、".join(speaker_items)
            elif isinstance(speaker_data, dict):
                name = speaker_data.get('name', '')
                position = speaker_data.get('position', '')
                company = speaker_data.get('company', '')
                
                other_info = []
                if position:
                    other_info.append(position)
                if company:
                    other_info.append(company)
                
                if name:
                    if other_info:
                        formatted_speakers = f"{name}（{', '.join(other_info)}）"
                    else:
                        formatted_speakers = name
        except:
            formatted_speakers = speakers
    
    return formatted_speakers 