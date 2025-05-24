import math
import numpy as np

def calculate_lung_health(cigarettes_per_day, years, nicotine_content=0.8, tar_content=10.0):
    """
    計算估計的肺部健康百分比，基於吸菸習慣包括尼古丁和焦油含量。
    
    參數:
    cigarettes_per_day (float): 每天平均吸菸數量
    years (float): 吸菸年數
    nicotine_content (float): 每支菸的尼古丁含量（毫克，默認: 0.8mg）
    tar_content (float): 每支菸的焦油含量（毫克，默認: 10.0mg）
    
    返回:
    float: 估計的肺部健康百分比 (0-100%)
    """
    if cigarettes_per_day == 0 or years == 0:
        return 100.0
    
    # 基本傷害係數 - 基於醫學研究的模型
    base_damage = cigarettes_per_day * years * 0.07
    
    # 尼古丁影響係數 - 尼古丁含量越高，傷害越大
    # 標準尼古丁含量約為0.8mg/支
    nicotine_factor = (nicotine_content / 0.8) * 0.5
    
    # 焦油影響係數 - 焦油是肺部黑化的主要原因
    # 標準焦油含量約為10mg/支
    tar_factor = (tar_content / 10.0) * 1.2
    
    # 組合所有因素計算總體傷害
    total_damage = base_damage * (1 + nicotine_factor + tar_factor)
    
    # 使用對數模型使傷害隨時間累積更符合實際情況
    # 長期吸菸者的肺部傷害會越來越嚴重
    log_factor = math.log(1 + years) / 2.0
    adjusted_damage = total_damage * (1 + log_factor)
    
    # 計算最終健康百分比，限制在0-100範圍內
    health_percentage = max(0, 100 - adjusted_damage)
    return health_percentage

def get_lung_description(health_percentage):
    """
    根據肺部健康百分比獲取肺部狀況的描述文字。
    
    參數:
    health_percentage (float): 肺部健康百分比 (0-100%)
    
    返回:
    str: 肺部狀況描述
    """
    if health_percentage >= 95:
        return "健康，無明顯傷害"
    elif health_percentage >= 85:
        return "輕微受損，有少量煙焦油沉積"
    elif health_percentage >= 75:
        return "中度受損，肺泡開始出現明顯損傷"
    elif health_percentage >= 65:
        return "顯著受損，肺功能降低，煙焦油沉積明顯"
    elif health_percentage >= 50:
        return "嚴重受損，呼吸功能顯著下降，持續咳嗽風險增加"
    elif health_percentage >= 35:
        return "極度受損，肺功能嚴重受限，高風險發展為慢性疾病"
    elif health_percentage >= 20:
        return "危險狀態，肺功能極度受限，可能已發展為肺部疾病"
    else:
        return "極危險狀態，肺部已有嚴重且不可逆的損傷"

def get_health_metrics(health_percentage):
    """
    根據肺部健康百分比生成健康指標。
    
    參數:
    health_percentage (float): 肺部健康百分比 (0-100%)
    
    返回:
    dict: 包含各種基於醫學研究的健康指標的字典
    """
    # 肺功能比例 (相對於同年齡非吸菸者)
    lung_function = health_percentage
    
    # 肺癌風險倍數 (相對於非吸菸者)
    # 基於醫學研究，長期吸菸者肺癌風險可達非吸菸者的15-30倍
    if health_percentage >= 90:
        cancer_risk = 1.5
    elif health_percentage >= 80:
        cancer_risk = 5
    elif health_percentage >= 70:
        cancer_risk = 10
    elif health_percentage >= 60:
        cancer_risk = 15
    elif health_percentage >= 40:
        cancer_risk = 20
    else:
        cancer_risk = 25
    
    # 預期壽命減少年數
    # 根據醫學研究，重度吸菸者平均壽命減少10-15年
    life_reduction = (100 - health_percentage) / 100 * 15
    
    # 其他健康影響 (相對風險倍數)
    other_impacts = {
        "心血管疾病": 1 + (100 - health_percentage) / 20,
        "中風": 1 + (100 - health_percentage) / 25,
        "慢性阻塞性肺病": 1 + (100 - health_percentage) / 15,
        "口腔癌": 1 + (100 - health_percentage) / 30,
        "喉癌": 1 + (100 - health_percentage) / 35,
    }
    
    return {
        "lung_function": lung_function,
        "cancer_risk": cancer_risk,
        "life_expectancy_reduction": life_reduction,
        "other_impacts": other_impacts
    }

def calculate_financial_impact(cigarettes_per_day, years, price_per_pack, cigarettes_per_pack=20):
    """
    計算吸菸的經濟影響。
    
    參數:
    cigarettes_per_day (float): 每天吸菸數量
    years (float): 吸菸年數
    price_per_pack (float): 每包菸的價格
    cigarettes_per_pack (int): 每包菸的數量，默認20支
    
    返回:
    dict: 包含各種經濟影響指標的字典
    """
    # 每日花費
    daily_cost = (cigarettes_per_day / cigarettes_per_pack) * price_per_pack
    
    # 每月花費 (假設一個月30天)
    monthly_cost = daily_cost * 30
    
    # 每年花費
    yearly_cost = daily_cost * 365
    
    # 總花費（考慮通貨膨脹和價格上漲）
    # 假設菸價平均每年上漲3%
    total_cost = 0
    for year in range(int(years)):
        yearly_inflation = yearly_cost * ((1 + 0.03) ** year)
        total_cost += yearly_inflation
    
    # 如果考慮這些錢投資而非用於吸菸，可能的收益
    # 假設平均年投資回報率為5%
    potential_investment = 0
    for year in range(int(years)):
        # 該年的花費
        yearly_inflation = yearly_cost * ((1 + 0.03) ** year)
        # 如果投資這筆錢
        future_value = yearly_inflation * ((1 + 0.05) ** (years - year))
        potential_investment += future_value
    
    return {
        "daily_cost": daily_cost,
        "monthly_cost": monthly_cost,
        "yearly_cost": yearly_cost,
        "total_cost": total_cost,
        "potential_investment": potential_investment
    }