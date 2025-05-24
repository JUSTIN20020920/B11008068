import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from utils import calculate_lung_health, get_lung_description, get_health_metrics
from lung_svg_generator import generate_lung_svg
from gemini_assistant import get_personalized_advice, get_quitting_resources

# 頁面配置
st.set_page_config(
    page_title="吸菸肺部健康視覺化",
    page_icon="🫁",
    layout="wide"
)

# 標題和介紹
st.title("🫁 吸菸肺部健康視覺化工具")
st.markdown("### 了解吸菸對您肺部健康的影響以及個性化戒菸建議")

# 側邊欄 - 用戶輸入
with st.sidebar:
    st.header("📝 輸入您的吸菸習慣")
    
    cigarettes_per_day = st.slider("每日吸菸數量（支）", 0, 60, 10, 1)
    years_smoking = st.slider("吸菸年數", 0, 50, 5, 1)
    
    st.subheader("詳細參數設定")
    with st.expander("尼古丁和焦油含量"):
        nicotine_content = st.slider("尼古丁含量 (mg/支)", 0.1, 2.0, 0.8, 0.1)
        tar_content = st.slider("焦油含量 (mg/支)", 1.0, 20.0, 10.0, 0.5)
    
    with st.expander("經濟影響"):
        cigarette_price = st.number_input("一包菸的價格 (NT$)", 0, 1000, 100, 10)
        cigarettes_per_pack = st.slider("一包菸的數量 (支)", 1, 25, 20, 1)

# 計算肺部健康度
health_percentage = calculate_lung_health(cigarettes_per_day, years_smoking, 
                                         nicotine_content, tar_content)

# 主要內容區域
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("肺部健康視覺化")
    
    # 顯示肺部圖像
    lung_html = generate_lung_svg(health_percentage)
    st.markdown(lung_html, unsafe_allow_html=True)
    
    # 健康度儀表板
    st.metric("肺部健康度", f"{health_percentage:.1f}%", 
              delta=None if health_percentage > 95 else f"{health_percentage-100.0:.1f}%")
    
    # 肺部狀況描述
    st.markdown(f"**肺部狀況**: {get_lung_description(health_percentage)}")

with col2:
    st.subheader("健康風險評估")
    
    # 獲取健康指標
    health_metrics = get_health_metrics(health_percentage)
    
    # 顯示健康風險
    st.info(f"**肺功能**: 與同年齡非吸菸者相比降低了 {100.0-health_metrics['lung_function']:.1f}%")
    st.warning(f"**肺癌風險**: 比非吸菸者高 {health_metrics['cancer_risk']:.1f} 倍")
    st.error(f"**預期壽命減少**: 約 {health_metrics['life_expectancy_reduction']:.1f} 年")
    
    # 其他健康影響
    st.markdown("#### 其他健康影響")
    impacts_dict = health_metrics['other_impacts']
    for impact, value in impacts_dict.items():
        if value > 3:
            st.markdown(f"- {impact}: 高風險 ⚠️")
        elif value > 1.5:
            st.markdown(f"- {impact}: 中等風險 ⚠️")
        else:
            st.markdown(f"- {impact}: 輕微風險")

# 經濟影響分析
st.header("💰 經濟影響分析")
col3, col4 = st.columns(2)

with col3:
    # 計算花費
    daily_cost = (cigarettes_per_day / cigarettes_per_pack) * cigarette_price
    monthly_cost = daily_cost * 30
    yearly_cost = daily_cost * 365
    lifetime_cost = yearly_cost * years_smoking
    
    st.subheader("吸菸花費")
    st.metric("每日花費", f"NT$ {daily_cost:.1f}")
    st.metric("每月花費", f"NT$ {monthly_cost:.1f}")
    st.metric("每年花費", f"NT$ {yearly_cost:.1f}")
    st.metric("累計花費", f"NT$ {lifetime_cost:.1f}")

with col4:
    st.subheader("等值消費比較")
    # 可替代消費項目及其價格 (NT$)
    alternatives = {
        "高級咖啡": 150,
        "電影票": 300,
        "健身房月費": 1500,
        "平板電腦": 10000,
        "國內旅遊": 15000,
        "國際旅遊": 50000,
        "頂級智能手機": 35000,
        "筆記型電腦": 30000
    }
    
    # 計算可購買的數量
    for item, price in alternatives.items():
        if lifetime_cost >= price:
            count = int(lifetime_cost / price)
            st.markdown(f"- 您可以購買 **{count}** 個/次 **{item}**")

# 個性化戒菸建議
st.header("🌱 個性化戒菸計劃")

if st.button("獲取個性化戒菸建議"):
    with st.spinner("正在生成您的個性化戒菸計劃..."):
        # 收集額外信息
        additional_info = {
            "nicotine_content": nicotine_content,
            "tar_content": tar_content,
            "daily_spending": daily_cost,
            "health_metrics": health_metrics
        }
        
        # 獲取個性化建議
        advice = get_personalized_advice(
            cigarettes_per_day, 
            years_smoking, 
            health_percentage, 
            additional_info
        )
        
        # 顯示建議
        st.subheader("您的個性化戒菸建議")
        st.markdown(advice["summary"])
        
        with st.expander("階段性戒菸計劃"):
            for stage in advice["stages"]:
                st.markdown(f"**階段 {stage['stage']}**: {stage['description']}")
                st.markdown(f"目標: {stage['goal']}")
                st.markdown(f"時間: {stage['timeframe']}")
                st.markdown("---")
        
        with st.expander("應對吸菸欲望的策略"):
            for strategy in advice["coping_strategies"]:
                st.markdown(f"- **{strategy['trigger']}**: {strategy['strategy']}")

# 戒菸資源
st.header("🔍 戒菸資源與支持")
resources = get_quitting_resources()

for category, items in resources.items():
    with st.expander(f"{category}"):
        for item in items:
            st.markdown(f"- {item}")

# 頁腳
st.markdown("---")
st.markdown("💙 此工具僅提供參考，請諮詢醫療專業人員獲取個人化的健康建議。")