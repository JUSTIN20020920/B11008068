#!/usr/bin/env python3
"""
工具模塊：提供廖貫呈個人作品集網站的數據處理功能
"""
import json
import os

def get_project_data():
    """
    從data.txt文件中獲取專案數據
    如果文件不存在，則返回預設專案資料
    
    Returns:
        list: 專案數據列表
    """
    try:
        # 嘗試從文件讀取數據
        if os.path.exists('data.txt'):
            with open('data.txt', 'r', encoding='utf-8') as file:
                return json.loads(file.read())
    except Exception as e:
        print(f"讀取專案數據時發生錯誤: {e}")
    
    # 如果無法讀取文件或文件不存在，返回預設數據
    return [
        {
            "title": "台泥財報及股價分析",
            "description": "深入分析台灣水泥公司的財務報表，並結合市場趨勢和技術指標對其股價進行分析和預測。",
            "technologies": ["Python", "Pandas", "NumPy", "Matplotlib", "財務分析"],
            "category": "finance",
            "icon": "chart-line"
        },
        {
            "title": "友達光電招募流程研究",
            "description": "對友達光電的人才招募流程進行全面研究，分析其招聘策略、面試流程和人才選拔標準，提出優化建議。",
            "technologies": ["問卷調查", "數據分析", "策略規劃"],
            "category": "analysis",
            "icon": "search-dollar"
        },
        {
            "title": "台積電股價人工智慧預測",
            "description": "運用機器學習和人工智慧技術對台積電股價進行預測，結合多種預測模型提高準確性，分析影響股價的關鍵因素。",
            "technologies": ["Python", "機器學習", "時間序列分析", "深度學習"],
            "category": "programming",
            "icon": "robot"
        },
        {
            "title": "韓流文化分析研究",
            "description": "研究韓流文化在台灣的影響與發展，分析其商業模式、行銷策略和文化傳播方式，探討跨文化傳播的成功因素。",
            "technologies": ["市場研究", "文化分析", "社會調查", "數據視覺化"],
            "category": "analysis",
            "icon": "globe-asia"
        }
    ]