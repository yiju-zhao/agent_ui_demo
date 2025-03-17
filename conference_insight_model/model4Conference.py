from openai import OpenAI
from system_prompts import system_prompt_for_merge_insights, system_prompt_for_daily_highlights
import pandas as pd
import json
import re
from report_generator import (
    generate_daily_conference_report,
    save_markdown_report,
    markdown_to_word
)

# 常量定义
OPENROUTER_API_KEY = "" #换成相应的api key
MODEL_NAME = "gpt-4o" 
CSV_INPUT_FILE = "GTC_2025_CARI - 2025-03-16.csv"# test.csv
CSV_OUTPUT_FILE = "GTC_2025_CARI - 2025-03-16_updated.csv" # test_updated.csv
OUTPUT_MARKDOWN_FOR_DAILY_HIGHLIGHTS = "daily_highlights.md" # 模型总结的每日精选内容-markdown格式  
OUTPUT_WORD_FOR_DAILY_HIGHLIGHTS = "daily_highlights.docx" # 模型总结的每日精选内容-word格式
OUTPUT_MARKDOWN_FOR_CONFERENCE_REPORT = "conference_report.md" # 每日参会快报-markdown格式
OUTPUT_WORD_FOR_CONFERENCE_REPORT = "conference_report.docx" # 每日参会快报-word格式


def preprocess_prompt(prompt_text):
    """
    预处理提示文本，替换特定词汇
    - 将"华为"替换为"企业"
    - 将"Huawei"替换为"company"（不区分大小写）
    
    Args:
        prompt_text (str): 原始提示文本
        
    Returns:
        str: 处理后的提示文本
    """
    # 替换中文词汇
    processed_text = prompt_text.replace("华为", "企业")
    
    # 不区分大小写替换英文词汇
    pattern = re.compile(r'Huawei', re.IGNORECASE)
    processed_text = pattern.sub('company', processed_text)
    
    return processed_text



def create_openai_client(api_key=OPENROUTER_API_KEY):
    """
    创建OpenAI客户端
    """
    return OpenAI(api_key=api_key)


def generate_model_response(client, system_prompt, user_prompt, temperature=0, model=MODEL_NAME):
    """
    生成模型响应
    
    Args:
        client (OpenAI): OpenAI客户端
        system_prompt (str): 系统提示
        user_prompt (str): 用户提示
        temperature (float): 温度参数
        model (str): 模型名称
        
    Returns:
        Completion: 模型完成对象
    """
    return client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )


def extract_expert_insights(csv_file, field_name):
    """
    读取CSV文件并返回完整的DataFrame以及符合条件的索引列表
    
    Args:
        csv_file (str): CSV文件路径
        field_name (str): 要处理的字段名称 ("实事描述\nDescription of Facts" 或 "对公司启示\nInsights for Company")
        
    Returns:
        tuple: (完整的DataFrame, 符合条件的索引列表)
    """
    # 读取CSV文件
    df = pd.read_csv(csv_file)
    
    # 创建一个列表来存储符合条件的索引
    valid_indices = []
    
    # 遍历每一行
    for index, row in df.iterrows():
        # 检查指定字段是否为空
        if pd.notna(row[field_name]):
            try:
                # 将字符串转换为Python列表
                insights = eval(row[field_name])
                
                # 只有当insights是列表且长度大于0时才添加索引
                if isinstance(insights, list) and len(insights) > 1:
                    valid_indices.append(index)
            except:
                # 解析错误不添加到列表中
                pass
    
    return df, valid_indices

def process_insights_with_model(client, df, valid_indices, system_prompt_text, field_name):
    """
    处理指定字段的内容并返回模型的响应结果
    
    Args:
        client (OpenAI): OpenAI客户端
        df (DataFrame): 完整的数据DataFrame
        valid_indices (list): 符合条件的索引列表
        system_prompt_text (str): 系统提示文本
        field_name (str): 要处理的字段名称
        
    Returns:
        DataFrame: 更新后的DataFrame
    """
    # 创建合并后的字段名称
    merged_field_name = f"{field_name} merged"
    
    # 确保DataFrame中有合并后的列
    if merged_field_name not in df.columns:
        df[merged_field_name] = ""
    
    for idx in valid_indices:
        row = df.iloc[idx]
        
        try:
            # 获取原始内容并转换为Python列表
            insights = eval(row[field_name])
            
            # 将列表转换为字符串
            insights_text = json.dumps(insights, ensure_ascii=False)
            
            # 预处理提示文本
            processed_text = preprocess_prompt(insights_text)
            
            # 获取模型响应
            response = generate_model_response(client, system_prompt_text, processed_text)
            model_response = response.choices[0].message.content
            
            # 在DataFrame中更新合并后的字段
            df.at[idx, merged_field_name] = model_response
            
        except Exception as e:
            print(f"处理索引 {idx} 时发生错误: {str(e)}")
            continue
    
    return df

def process_fields(df, fields, client, system_prompt):
    """
    处理一个或多个字段的完整逻辑
    
    Args:
        df (DataFrame): 数据DataFrame
        fields (list or str): 要处理的字段名称列表或单个字段名称
        client (OpenAI): OpenAI客户端
        system_prompt (str): 系统提示文本
        
    Returns:
        DataFrame: 更新后的DataFrame
    """
    # 如果传入的是单个字段名称，转换为列表
    if isinstance(fields, str):
        fields = [fields]
    
    # 依次处理每个字段
    for field_name in fields:
        print(f"\n处理字段: {field_name}")
        
        # 提取符合条件的记录
        valid_indices = []
        for index, row in df.iterrows():
            if pd.notna(row[field_name]):
                try:
                    insights = eval(row[field_name])
                    if isinstance(insights, list) and len(insights) > 1:
                        valid_indices.append(index)
                except:
                    pass
        
        print(f"字段 {field_name} 中符合要求的记录数: {len(valid_indices)}")
        
        # 处理内容并获取模型响应
        df = process_insights_with_model(client, df, valid_indices, system_prompt, field_name)
        
        # 打印处理结果
        print(f"\n===== {field_name} 处理结果 =====")
        for idx in valid_indices:
            row = df.iloc[idx]
            print(f"\n--- 记录索引: {idx} ---")
            print(f"原始内容: {row[field_name]}")
            print(f"融合后的内容: {row[f'{field_name} merged']}")
            print("-" * 50)
    
    return df

def main():
    # 创建OpenAI客户端
    client = create_openai_client()
    
    # 定义要处理的字段
    fields = ["实事描述\nDescription of Facts", "对公司启示\nInsights for Company"]
    
    # 读取原始数据（只读取一次）
    df = pd.read_csv(CSV_INPUT_FILE)
    
    # 处理所有字段
    df_updated = process_fields(df, fields, client, system_prompt_for_merge_insights)
    
    # 保存更新后的DataFrame到CSV文件
    df_updated.to_csv(CSV_OUTPUT_FILE, index=False)
    print(f"\n更新后的数据已保存到 {CSV_OUTPUT_FILE}")
    
    # 生成每日参会快报（Markdown格式）
    markdown_report = generate_daily_conference_report(df_updated)
    save_markdown_report(markdown_report, OUTPUT_MARKDOWN_FOR_CONFERENCE_REPORT)

    #生成每日参会快报（Word格式）
    markdown_to_word(markdown_report, OUTPUT_WORD_FOR_CONFERENCE_REPORT)

    # 让模型根据每日参会快报生成一个每日精选内容
    daily_highlights = generate_model_response(client, system_prompt_for_daily_highlights, user_prompt=markdown_report).choices[0].message.content
    # print(daily_highlights)
    
    # 保存每日精选内容到Markdown文件
    with open(OUTPUT_MARKDOWN_FOR_DAILY_HIGHLIGHTS, 'w', encoding='utf-8') as f:
        f.write(daily_highlights)
    print(f"\n每日精选内容已保存到 {OUTPUT_MARKDOWN_FOR_DAILY_HIGHLIGHTS}")
    
    # 将每日精选内容转换为Word文档
    markdown_to_word(daily_highlights, OUTPUT_WORD_FOR_DAILY_HIGHLIGHTS)
    print(f"\n每日精选内容已转换为Word文档并保存到 {OUTPUT_WORD_FOR_DAILY_HIGHLIGHTS}")



if __name__ == "__main__":
    main()