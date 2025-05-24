import google.generativeai as genai
import os
from typing import List, Dict, Any, Optional

# 設置Gemini API密鑰
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# 設置Gemini模型 - 使用最新的API格式
model = genai.GenerativeModel('gemini-1.5-pro')

# 設置生成參數
generation_config = {
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 1024,
}

def get_personalized_advice(
    cigarettes_per_day: float,
    years_smoking: float,
    health_percentage: float,
    additional_info: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    使用Gemini AI獲取個性化戒煙建議和健康分析
    
    參數:
    cigarettes_per_day: 每天吸煙數量
    years_smoking: 吸煙年數
    health_percentage: 當前肺部健康度百分比
    additional_info: 其他用戶信息(可選)
    
    返回:
    包含AI生成的建議和分析的字典
    """
    # 計算吸煙相關統計數據
    pack_years = (cigarettes_per_day / 20) * years_smoking
    total_cigarettes = int(cigarettes_per_day * 365 * years_smoking)
    
    # 構建提示詞
    prompt = f"""
    作為一名醫學專家，請分析以下吸煙者的數據並提供專業的健康建議。請提供詳細的分析、具體的戒煙建議和科學的健康恢復預測。
    
    吸煙者數據:
    - 每天吸煙數量: {cigarettes_per_day} 支
    - 吸煙年數: {years_smoking} 年
    - 總計已吸煙: {total_cigarettes} 支
    - 包年(Pack Years): {pack_years:.1f}
    - 當前肺部健康度: {health_percentage:.1f}%
    
    根據醫學文獻，請提供以下信息，並以json格式回答:
    1. 健康風險分析: 基於該吸煙者的數據，分析他/她目前面臨的主要健康風險
    2. 戒煙策略: 提供3-5個基於證據的戒煙策略建議，包括心理和生理層面的應對方法
    3. 戒煙後健康恢復預測: 分時間段(1週、1個月、3個月、6個月、1年、5年)預測戒煙後身體可能恢復的情況
    4. 醫學統計數據: 提供2-3項與該吸煙情況相關的關鍵醫學研究數據
    5. 激勵信息: 提供一段激勵性信息，鼓勵戒煙
    
    請確保回答格式為json，包含以下關鍵:
    {
      "health_risks": ["風險1", "風險2", "風險3"],
      "quit_strategies": ["策略1", "策略2", "策略3"],
      "recovery_timeline": {"一週後": "描述", "一個月後": "描述"},
      "medical_stats": ["統計1", "統計2"],
      "motivation": "激勵信息"
    }
    """
    
    try:
        # 調用Gemini API生成回應
        response = model.generate_content(prompt)
        advice_text = response.text
        
        # 嘗試解析JSON回應
        import json
        import re
        
        # 提取JSON部分(去除可能的標記和前導/尾隨文本)
        json_match = re.search(r'({[\s\S]*})', advice_text)
        if json_match:
            advice_json = json.loads(json_match.group(1))
            return advice_json
        else:
            # 如果無法解析為JSON，返回文本作為建議
            return {
                "health_risks": ["基於您的吸煙數據分析..."],
                "quit_strategies": ["根據醫學建議..."],
                "recovery_timeline": {"提示": "無法生成詳細時間表"},
                "medical_stats": ["統計數據暫時無法生成"],
                "motivation": advice_text
            }
    except Exception as e:
        # 發生錯誤時返回備用訊息
        print(f"獲取Gemini建議時出錯: {e}")
        return {
            "health_risks": ["暫時無法分析健康風險，請稍後再試"],
            "quit_strategies": ["暫時無法提供戒煙策略"],
            "recovery_timeline": {"提示": "無法生成恢復時間表"},
            "medical_stats": ["無法獲取醫學統計數據"],
            "motivation": "目前無法連接到AI服務，但請記住，戒煙永遠不會太晚，每一天不吸煙都是對健康的投資。"
        }

def get_quitting_resources() -> Dict[str, List[str]]:
    """
    獲取戒煙資源和支持服務的信息
    
    返回:
    包含各類戒煙資源的字典
    """
    # 這些資源是靜態定義的，但也可以從Gemini獲取最新建議
    return {
        "熱線服務": [
            "衛生署煙害諮詢專線: 0800-636363",
            "門診戒煙治療服務: 02-2382-0886"
        ],
        "應用程式": [
            "Quit Genius - 戒煙認知行為療法",
            "Smoke Free - 追蹤進度和節省金錢",
            "QuitNow! - 社群支持和成就系統"
        ],
        "網站資源": [
            "國民健康署戒煙資源: https://www.hpa.gov.tw/Pages/List.aspx?nodeid=444",
            "WHO戒煙指南: https://www.who.int/tobacco/quitting/en/",
            "台灣戒煙網: https://www.tsh.org.tw/"
        ],
        "治療方法": [
            "尼古丁替代療法(如貼片、口香糖)",
            "處方藥物(如Varenicline或Bupropion)",
            "專業戒煙諮詢和認知行為療法",
            "針灸和催眠治療"
        ]
    }