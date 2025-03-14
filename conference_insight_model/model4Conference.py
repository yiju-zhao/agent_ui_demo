from openai import OpenAI
from system_prompts import system_prompt
import pandas as pd
import json
import re
from report_generator import (
    generate_daily_conference_report,
    generate_daily_conference_word,
    save_markdown_report
)

# 常量定义
OPENROUTER_API_KEY = "" #换成相应的api key
MODEL_NAME = "gpt-4o" 
EXCEL_INPUT_FILE = "fake_conference_data_test.csv"#"fake_conference_data.csv"
EXCEL_OUTPUT_FILE = "updated_fake_conference_data.csv"



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


def extract_expert_insights(csv_file):
    """
    读取CSV文件并返回完整的DataFrame以及符合条件的索引列表
    
    Args:
        csv_file (str): CSV文件路径
        
    Returns:
        tuple: (完整的DataFrame, 符合条件的索引列表)
    """
    # 读取CSV文件
    df = pd.read_csv(csv_file)
    
    # 创建一个列表来存储符合条件的索引
    valid_indices = []
    
    # 遍历每一行
    for index, row in df.iterrows():
        # 检查Expert Insight字段是否为空
        if pd.notna(row['Expert Insight']) and row['Expert Insight'] != "[]":
            try:
                # 解析JSON字符串
                insights = json.loads(row['Expert Insight'])
                
                # 只有当insights是列表且长度大于1时才添加索引
                if isinstance(insights, list) and len(insights) > 1:
                    valid_indices.append(index)
            except json.JSONDecodeError:
                # JSON解析错误不添加到列表中
                pass
    
    # 返回完整的DataFrame和符合条件的索引列表
    return df, valid_indices

def process_insights_with_model(client, df, valid_indices, system_prompt_text):
    """
    将每个符合条件的专家洞察喂给模型，并返回模型的响应结果
    同时在原始DataFrame的"Expert Insight merged"字段中插入模型响应
    
    Args:
        client (OpenAI): OpenAI客户端
        df (DataFrame): 完整的数据DataFrame
        valid_indices (list): 符合条件的索引列表
        system_prompt_text (str): 系统提示文本
        
    Returns:
        tuple: (更新后的DataFrame, 模型响应结果列表)
    """
    results = []
    
    # 确保DataFrame中有"Expert Insight merged"列，如果没有则创建
    if "Expert Insight merged" not in df.columns:
        df["Expert Insight merged"] = ""
    
    for idx in valid_indices:
        row = df.iloc[idx]
        
        # 获取专家洞察
        insights = json.loads(row['Expert Insight'])
        
        # 将洞察列表转换为字符串
        insights_text = json.dumps(insights, ensure_ascii=False)
        
        # 预处理提示文本
        processed_text = preprocess_prompt(insights_text)
        
        # 获取模型响应
        response = generate_model_response(client, system_prompt_text, processed_text)
        model_response = response.choices[0].message.content
        
        # 将响应添加到结果列表
        results.append({
            "index": idx,
            "original_insights": insights,
            "model_response": model_response
        })
        
        # 在DataFrame中更新"Expert Insight merged"字段
        df.at[idx, "Expert Insight merged"] = model_response
       
    
    return df


def main():
    # 创建OpenAI客户端
    client = create_openai_client()
    
    # 提取专家洞察
    df, valid_indices = extract_expert_insights(EXCEL_INPUT_FILE)
    
    # 打印符合要求的索引
    print(f"符合要求的索引列表: {valid_indices}")
    print(f"共有 {len(valid_indices)} 条符合要求的记录")
    
    # 处理专家洞察并获取模型响应，使用已导入的system_prompt
    updated_df = process_insights_with_model(client, df, valid_indices, system_prompt)

    # 保存更新后的DataFrame到CSV文件
    updated_df.to_csv(EXCEL_OUTPUT_FILE, index=False)
    print(f"更新后的数据已保存到 {EXCEL_OUTPUT_FILE}")

    # print(updated_df.columns)
    
    # 生成每日参会快报（Markdown格式）
    markdown_report = generate_daily_conference_report(updated_df)
    save_markdown_report(markdown_report)
    
    # 打印每一行的专家观点和融合后的专家观点
    print("\n===== 专家观点及融合结果 =====")
    for idx in valid_indices:
        row = updated_df.iloc[idx]
        print(f"\n--- 记录索引: {idx} ---")
        print(f"原始专家观点: {row['Expert Insight']}")
        print(f"融合后的专家观点: {row['Expert Insight merged']}")
        print("-" * 50)
    
    # 生成每日参会快报（Word格式）
    generate_daily_conference_word(updated_df)
    
if __name__ == "__main__":
    main()