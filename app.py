import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from utils import calculate_lung_health, get_lung_description, get_health_metrics
from lung_svg_generator import generate_lung_svg

# Page config
st.set_page_config(
    page_title="Lung Health Visualization",
    page_icon="🫁",
    layout="wide"
)

# Title and description
st.title("肺部退化視覺化工具")
st.markdown("""
這個互動式工具可視化展示吸菸如何隨時間影響肺部健康。
輸入您的吸菸習慣，查看肺部退化的演變過程。
""")

# Input form
with st.form("smoking_data_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        cigarettes_per_day = st.number_input(
            "每天吸菸數量", 
            min_value=0, 
            max_value=100, 
            value=10,
            help="平均每天吸菸的數量"
        )
        
        nicotine_content = st.slider(
            "尼古丁含量 (毫克/支)",
            min_value=0.1,
            max_value=2.0,
            value=0.8,
            step=0.1,
            help="每支菸的尼古丁含量（一般香菸約0.8-1.2毫克）"
        )
        
        tar_content = st.slider(
            "焦油含量 (毫克/支)",
            min_value=1.0,
            max_value=20.0,
            value=10.0,
            step=0.5,
            help="每支菸的焦油含量（一般香菸約8-12毫克）"
        )
        
    with col2:
        years_smoking = st.number_input(
            "吸菸年數", 
            min_value=0, 
            max_value=70, 
            value=5,
            help="您已經吸菸的年數"
        )
        
        cigarette_price = st.number_input(
            "菸價 (台幣/支)",
            min_value=1,
            max_value=100,
            value=5,
            help="每支菸的價格（台幣）"
        )
    
    # 計算每日和年度花費
    daily_cost = cigarettes_per_day * cigarette_price
    yearly_cost = daily_cost * 365
    
    # 計算尼古丁和焦油攝入量
    daily_nicotine = cigarettes_per_day * nicotine_content
    daily_tar = cigarettes_per_day * tar_content
    yearly_nicotine = daily_nicotine * 365
    yearly_tar = daily_tar * 365
    
    # 顯示花費和有害物質資訊
    cost_col1, cost_col2 = st.columns(2)
    with cost_col1:
        st.info(f"每日花費: {daily_cost} 台幣")
        st.warning(f"每日尼古丁攝入: {daily_nicotine:.1f} 毫克")
    with cost_col2:
        st.info(f"年度花費: {yearly_cost:,.0f} 台幣")
        st.warning(f"每日焦油攝入: {daily_tar:.1f} 毫克")
    
    submitted = st.form_submit_button("顯示肺部健康狀況")

if submitted or ('cigarettes_per_day' in st.session_state and 'years_smoking' in st.session_state):
    # Store values in session state to persist across reruns
    st.session_state['cigarettes_per_day'] = cigarettes_per_day
    st.session_state['years_smoking'] = years_smoking
    
    # Calculate total cigarettes smoked and total cost
    total_cigarettes = cigarettes_per_day * 365 * years_smoking
    total_cost = total_cigarettes * cigarette_price
    
    # 根據總花費生成可以購買的物品對比
    comparable_items = []
    
    # 首先創建價格區間與對應物品的映射，按價格從高到低排序，並符合實際市場價格
    price_ranges = [
        (650000, "一台Toyota Corolla Cross中階休旅車"),  # 實際市場價格約65萬台幣
        (80000, "一趟美國洛杉磯或紐約旅行"),  # 含機票、住宿和基本花費
        (45000, "一台MacBook Pro筆記型電腦"),  # 入門款價格
        (35000, "一台iPhone Pro Max最新款智慧型手機"),  # 高配置款
        (18000, "一台iPad Air平板電腦"),  # Apple平板實際價格
        (6000, "一雙Nike或Adidas高級運動鞋"),  # 品牌運動鞋實際價格
        (3600, "一個月健身房高級會籍"),  # 知名連鎖健身房月費
        (2500, "一頓王品或乾杯等高級餐廳晚餐")  # 每人均消
    ]
    
    # 找出最接近總成本的3個物品
    items_to_display = []
    remaining_cost = total_cost
    
    # 首先找出可完全購買的物品
    for price, item in price_ranges:
        if remaining_cost >= price:
            # 計算可購買的數量
            count = remaining_cost // price
            if count > 0:
                if count == 1:
                    items_to_display.append(f"{item} (約 NT${price:,})")
                else:
                    # 最多顯示3件相同物品，避免重複太多
                    display_count = min(count, 3)
                    if display_count > 1:
                        # 根據不同物品使用適當的量詞
                        if "旅行" in item:
                            items_to_display.append(f"{display_count}趟{item.replace('一趟', '')} (約 NT${price*display_count:,})")
                        elif "台" in item:
                            items_to_display.append(f"{display_count}台{item.replace('一台', '')} (約 NT${price*display_count:,})")
                        elif "個" in item:
                            items_to_display.append(f"{display_count}個{item.replace('一個', '')} (約 NT${price*display_count:,})")
                        elif "雙" in item:
                            items_to_display.append(f"{display_count}雙{item.replace('一雙', '')} (約 NT${price*display_count:,})")
                        elif "頓" in item:
                            items_to_display.append(f"{display_count}頓{item.replace('一頓', '')} (約 NT${price*display_count:,})")
                        else:
                            items_to_display.append(f"{display_count}個{item.replace('一', '')} (約 NT${price*display_count:,})")
                    else:
                        items_to_display.append(f"{item} (約 NT${price:,})")
                # 更新剩餘成本
                remaining_cost = remaining_cost % price
            
            # 最多選擇3項物品
            if len(items_to_display) >= 3:
                break
    
    # 如果沒有找到足夠的物品，添加最便宜的選項
    if len(items_to_display) == 0 and total_cost > 0:
        lowest_price = min(price for price, _ in price_ranges)
        for price, item in price_ranges:
            if price == lowest_price:
                items_to_display.append(f"{item} (約 NT${price:,})")
                break
    
    # 生成可比較文本
    comparable_text = ""
    if items_to_display:
        comparable_text = f"相當於可以購買: {', '.join(items_to_display)}"
    
    # Display the total cigarettes smoked and cost
    st.metric("總共吸菸數量", f"{total_cigarettes:,} 支")
    st.metric("總花費", f"NT$ {total_cost:,}")
    
    if comparable_text:
        st.markdown(f"""
        <div style="background-color:#ffeaeb; padding:12px; border-radius:8px; margin-bottom:15px; border-left:5px solid #f44336;">
            <p style="color:#b71c1c; margin:0; font-weight:500;">{comparable_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate timeline data (yearly) with nicotine and tar content consideration
    timeline_years = list(range(0, int(years_smoking) + 1))
    health_percentages = [calculate_lung_health(cigarettes_per_day, year, nicotine_content, tar_content) for year in timeline_years]
    
    # Create dataframe for timeline
    timeline_df = pd.DataFrame({
        'Year': timeline_years,
        'Lung Health (%)': health_percentages
    })
    
    # 肺部健康時間線部分已刪除
    
    # 保留一個清晰的大標題
    st.subheader("肺部從健康到受損的階段變化")
    
    # Import necessary libraries
    import matplotlib.pyplot as plt
    import io
    import base64
    from lung_svg_generator import create_lung_image
    
    # Create discrete year steps
    max_years = int(years_smoking)
    
    # 如果吸菸年數超過5年，則用5個階段顯示，否則按年數顯示
    if max_years > 5:
        year_steps = [0]
        step_size = max_years / 5
        for i in range(1, 5):
            year_steps.append(int(i * step_size))
        year_steps.append(max_years)
    else:
        year_steps = list(range(max_years + 1))
    
    # 確保至少有兩個階段（開始和結束）
    if len(year_steps) < 2:
        year_steps = [0, max(1, max_years)]
    
    # 創建肺部階段圖像
    lung_images = []
    health_percentages = []
    
    # 進度條
    progress_text = "正在生成肺部視覺化階段圖..."
    progress_bar = st.progress(0)
    
    # 為每個階段創建圖像
    for i, year in enumerate(year_steps):
        # 計算這個年份的健康度（考慮尼古丁和焦油含量）
        health = calculate_lung_health(cigarettes_per_day, year, nicotine_content, tar_content)
        health_percentages.append(health)
        
        # 創建圖像
        fig, ax = plt.subplots(figsize=(8, 8))
        create_lung_image(ax, health)
        # 不在圖像中顯示中文標題，改為在Streamlit界面中顯示
        ax.set_title("")
        ax.axis('off')
        
        # 轉換為base64字符串
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        lung_images.append(img_str)
        progress_bar.progress((i + 1) / len(year_steps))
    
    progress_bar.empty()
    
    # 已刪除重複標題
    
    # 創建圖像滑塊
    selected_index = st.slider("選擇查看階段", 0, len(year_steps)-1, 0)
    
    # 顯示選中階段的信息（不含小數點的年數）
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="font-size: 20px; font-weight: bold;">第 {selected_index+1} 階段: 吸菸 {int(year_steps[selected_index])} 年後</div>
        <div style="font-size: 16px; color: #555;">肺部健康度: {health_percentages[selected_index]:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 顯示選中的階段圖像
    st.markdown(f"""
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <img src="data:image/png;base64,{lung_images[selected_index]}" style="max-width: 500px; width: 100%; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    </div>
    """, unsafe_allow_html=True)
    
    # 顯示所有階段的小圖像
    st.markdown("### 所有階段總覽")
    
    # 計算每行顯示的列數
    cols = st.columns(len(lung_images))
    
    # 在每列中顯示一個階段
    for i, col in enumerate(cols):
        with col:
            # 顯示帶高亮的小圖像（選中的會更亮）
            highlight = "border: 3px solid #FF5252;" if i == selected_index else ""
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{lung_images[i]}" 
                     style="width: 100%; border-radius: 5px; {highlight} cursor: pointer;"
                     onclick="document.getElementById('slider').value={i}; document.getElementById('slider').dispatchEvent(new Event('change'));">
                <div style="font-size: 12px; margin-top: 5px;">{int(year_steps[i])} 年</div>
            </div>
            """, unsafe_allow_html=True)
    
    # 提供詳細的階段肺部變化醫學信息
    if selected_index == 0:
        stage_description = "健康肺部：粉紅色，支氣管清晰，沒有焦油沉積。"
        medical_details = """
        <ul>
            <li><strong>微觀結構：</strong>約3億個肺泡處於健康狀態，可有效進行氣體交換</li>
            <li><strong>肺活量：</strong>成人平均約4-6升，氧氣交換效率達95%以上</li>
            <li><strong>細胞健康度：</strong>纖毛功能完整，能有效清除吸入的微粒</li>
            <li><strong>肺部防禦機制：</strong>巨噬細胞和免疫系統正常運作，可抵禦病原體</li>
        </ul>
        """
        medical_research = "根據《新英格蘭醫學雜誌》研究，健康非吸菸者的肺活量通常比同齡吸菸者高15-20%。"
        recovery_info = "維持戒菸狀態，肺部將保持健康狀態。"
        
    elif selected_index < len(lung_images) // 4:
        stage_description = "早期損傷：小氣道上皮細胞變化，輕微炎症，增加黏液產生。"
        medical_details = """
        <ul>
            <li><strong>微觀變化：</strong>支氣管粘膜組織增厚，上皮細胞開始變形</li>
            <li><strong>臨床表現：</strong>可能出現輕微咳嗽，尤其是早晨，偶有痰液</li>
            <li><strong>纖毛功能：</strong>纖毛運動減慢33%，清除能力下降</li>
            <li><strong>炎症標記物：</strong>IL-6、IL-8和TNF-α水平輕度上升</li>
        </ul>
        """
        medical_research = "《胸部醫學》期刊研究發現，即使少量吸菸(每天3-5支菸)也會導致小氣道功能測量值下降約10%。"
        recovery_info = "戒菸1-2個月後，纖毛功能可恢復至接近正常，咳嗽症狀明顯緩解。"
        
    elif selected_index < len(lung_images) // 2:
        stage_description = "中度損傷：色素沉著巨噬細胞積累，呼吸性細支氣管炎，早期中央小葉肺氣腫。"
        medical_details = """
        <ul>
            <li><strong>氣道病變：</strong>慢性炎症使氣道壁增厚約25-40%，肌肉層肥厚</li>
            <li><strong>肺泡損傷：</strong>每立方毫米肺組織中約有2000-3000個肺泡開始破裂</li>
            <li><strong>肺功能下降：</strong>FEV1(第一秒用力呼氣量)較預期值下降15-25%</li>
            <li><strong>氧氣交換：</strong>血氧飽和度可能在活動時下降至93-95%</li>
        </ul>
        """
        medical_research = "《美國呼吸與重症醫學雜誌》研究顯示，10-15年吸菸史的人群呼吸道阻力增加40%，彈性回縮力下降20%。"
        recovery_info = "戒菸6-12個月後，支氣管炎症狀可減輕50%以上，但肺氣腫早期損傷可能難以完全逆轉。"
        
    elif selected_index < 3 * len(lung_images) // 4:
        stage_description = "嚴重損傷：瀰漫性肺氣腫，氣道纖維化增加，支氣管壁增厚，黑色焦油沉積。"
        medical_details = """
        <ul>
            <li><strong>肺結構改變：</strong>肺泡壁大量破壞，形成異常氣腔，彈性組織減少60-70%</li>
            <li><strong>臨床症狀：</strong>明顯呼吸困難(MRC呼吸困難量表3-4級)，尤其在活動時</li>
            <li><strong>肺功能數據：</strong>FEV1下降至預期值的35-50%，FEV1/FVC比值<70%</li>
            <li><strong>併發症風險：</strong>呼吸道感染風險增加3倍，肺炎住院率增加2.5倍</li>
        </ul>
        """
        medical_research = "《柳葉刀-呼吸醫學》研究發現，20年以上的吸菸者中，約60%會發展為COPD，且有18%的患者需要長期氧療。"
        recovery_info = "戒菸後，肺功能下降速度可減慢至正常老化水平，但已造成的肺氣腫和纖維化難以恢復。"
        
    else:
        stage_description = "危重損傷：大面積肺氣腫和肺大泡，蜂窩肺外觀，非功能性組織，嚴重色素沉著和纖維化。"
        medical_details = """
        <ul>
            <li><strong>肺臟病理：</strong>超過70%的肺組織呈現不可逆病變，肺大泡占據肺容積25-40%</li>
            <li><strong>呼吸力學：</strong>橫膈肌壓平，胸廓過度膨脹，呼吸功增加2-3倍</li>
            <li><strong>呼吸衰竭：</strong>動脈血氧分壓(PaO2)低於60mmHg，二氧化碳滯留</li>
            <li><strong>心血管併發症：</strong>肺動脈壓力升高，右心室負荷增加，可發展為肺心病</li>
        </ul>
        """
        medical_research = "《COPD雜誌》研究表明，重度COPD患者5年存活率約為50%，這與某些類型的癌症生存率相當。"
        recovery_info = "此階段即使戒菸，大部分損傷也不可逆轉，但仍能減緩進一步惡化，並減少急性加重次數。"
    
    # 使用Streamlit原生組件顯示詳細的醫學信息
    with st.container():
        st.subheader("當前階段肺部狀態")
        st.write(stage_description)
        
        st.markdown("#### 📊 醫學詳情")
        if selected_index == 0:
            st.markdown("- **微觀結構：** 約3億個肺泡處於健康狀態，可有效進行氣體交換")
            st.markdown("- **肺活量：** 成人平均約4-6升，氧氣交換效率達95%以上")
            st.markdown("- **細胞健康度：** 纖毛功能完整，能有效清除吸入的微粒")
            st.markdown("- **肺部防禦機制：** 巨噬細胞和免疫系統正常運作，可抵禦病原體")
        elif selected_index < len(lung_images) // 4:
            st.markdown("- **微觀變化：** 支氣管粘膜組織增厚，上皮細胞開始變形（是非吸菸者細胞結構的1.5倍厚度）")
            st.markdown("- **臨床表現：** 可能出現輕微咳嗽，尤其是早晨，偶有痰液（咳嗽頻率是非吸菸者的2倍）")
            st.markdown("- **纖毛功能：** 纖毛運動減慢33%，清除能力下降（相比非吸菸者肺部清潔能力降低40%）")
            st.markdown("- **炎症標記物：** IL-6、IL-8和TNF-α水平輕度上升（比非吸菸者高出50-70%）")
        elif selected_index < len(lung_images) // 2:
            st.markdown("- **肺部變化：** 小氣道變窄約40%，黏液分泌增加2-3倍（相比非吸菸者）")
            st.markdown("- **吸菸者咳嗽：** 咳痰量增加，尤其是早晨第一支菸後（咳嗽頻率是非吸菸者的3倍）")
            st.markdown("- **肺功能數據：** FEV1下降約20-30%，小氣道阻力增加3倍（相比非吸菸者）")
            st.markdown("- **炎症程度：** 中度系統性炎症反應，炎症細胞浸潤顯著（發炎標記物濃度是非吸菸者的5倍）")
        elif selected_index < len(lung_images) * 3 // 4:
            st.markdown("- **結構變化：** 肺氣腫區域占肺容積15-30%，支氣管壁增厚2-3倍（相比同齡非吸菸者肺組織厚度增加200%）")
            st.markdown("- **症狀表現：** 慢性咳嗽，呼吸困難(MRC量表2-3級)，運動耐量下降（運動能力比非吸菸者降低40-50%）")
            st.markdown("- **血氧水平：** 休息時氧飽和度可能低於95%，運動時更低（同等運動量下，氧飽和度比非吸菸者低3-5%）")
            st.markdown("- **免疫功能：** 局部免疫防禦機制破壞，易感染風險增加3-4倍（相比非吸菸者易患肺炎機率增加300%）")
        else:
            st.markdown("- **肺臟病理：** 超過70%的肺組織呈現不可逆病變，肺大泡占據肺容積25-40%（相比同齡非吸菸者肺部健康組織少70-80%）")
            st.markdown("- **呼吸力學：** 橫膈肌壓平，胸廓過度膨脹，呼吸功增加2-3倍（呼吸所需能量是非吸菸者的3倍）")
            st.markdown("- **呼吸衰竭：** 動脈血氧分壓(PaO2)低於60mmHg，二氧化碳滯留（需要外部供氧的風險是非吸菸者的25倍）")
            st.markdown("- **心血管併發症：** 肺動脈壓力升高，右心室負荷增加，可發展為肺心病（心臟負荷比非吸菸者增加200%）")
        
        # 根據階段計算癌症風險
        if selected_index == 0:
            lung_cancer_risk = "< 1%"
            copd_risk = "< 2%"
            throat_cancer_risk = "< 0.5%"
        elif selected_index < len(lung_images) // 4:
            lung_cancer_risk = "3-5%"
            copd_risk = "8-12%"
            throat_cancer_risk = "2-3%"
        elif selected_index < len(lung_images) // 2:
            lung_cancer_risk = "8-12%"
            copd_risk = "15-25%"
            throat_cancer_risk = "5-8%"
        elif selected_index < len(lung_images) * 3 // 4:
            lung_cancer_risk = "15-20%"
            copd_risk = "30-40%"
            throat_cancer_risk = "8-12%"
        else:
            lung_cancer_risk = "20-25%"
            copd_risk = "40-60%"
            throat_cancer_risk = "12-18%"

        st.markdown("#### 📊 癌症風險機率")
        st.markdown(f"""
        <div style="background-color: #ffebee; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
            <div style="font-weight: bold; margin-bottom: 10px; color: #d32f2f;">根據目前肺部狀況，估計罹患以下疾病的終身風險：</div>
            <ul style="margin-bottom: 0; color: #212121;">
                <li><strong style="color: #b71c1c;">肺癌風險：</strong> <span style="color: #d32f2f; font-weight: bold;">{lung_cancer_risk}</span></li>
                <li><strong style="color: #b71c1c;">慢性阻塞性肺病(COPD)風險：</strong> <span style="color: #d32f2f; font-weight: bold;">{copd_risk}</span></li>
                <li><strong style="color: #b71c1c;">喉/咽癌風險：</strong> <span style="color: #d32f2f; font-weight: bold;">{throat_cancer_risk}</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(f"🔬 **研究發現**\n{medical_research}")
        st.success(f"💡 **恢復可能性**\n{recovery_info}")
    
    # 尼古丁和焦油含量參考資訊
    st.markdown("#### ⚠️ 尼古丁和焦油影響分析")
    st.markdown(f"""
    <div style="background-color: #e0f7fa; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
        <div style="font-weight: bold; margin-bottom: 10px; color: #00838f;">目前尼古丁含量({nicotine_content}毫克)和焦油含量({tar_content}毫克)對健康的影響：</div>
        <ul style="margin-bottom: 0; color: #006064;">
            <li><strong>尼古丁影響：</strong> 尼古丁含量每降低0.3毫克，對肺部的傷害可減少約5-10%</li>
            <li><strong>焦油影響：</strong> 焦油含量每降低5毫克，肺部健康度可提高約10-15%</li>
            <li><strong>綜合評估：</strong> 以上計算已將您提供的尼古丁({nicotine_content}毫克)和焦油({tar_content}毫克)含量納入考慮</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Add some space
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 添加個性化戒菸計畫部分
    st.subheader("📝 個性化戒菸計畫生成器")
    
    # 增加解釋文字
    st.markdown("""
    根據您的吸菸習慣，我們可以為您生成一個量身定制的戒菸計畫，幫助您逐步減少吸菸，直至完全戒除。
    這個計畫基於醫學研究和臨床證據，但僅供參考，不能替代專業醫生的建議。
    """)
    
    # 增加更多用戶輸入
    with st.expander("填寫更多吸菸習慣資訊", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            smoking_duration = st.number_input("平均一支菸吸多久？(分鐘)", min_value=1, max_value=30, value=5, help="平均每支菸的吸食時間")
            smoking_times = st.number_input("一天抽菸的次數", min_value=1, max_value=50, value=int(cigarettes_per_day), help="一天中點菸的次數")
            
        with col2:
            # 使用單行簡短的尼古丁含量選項
            nicotine_options = ["低尼古丁 (0.1-0.6毫克)", "中尼古丁 (0.7-1.2毫克)", "高尼古丁 (1.3-2.0毫克)"]
            nicotine_type = st.selectbox("菸的尼古丁含量", options=nicotine_options, index=1,
                                         help="菸的尼古丁含量影響戒菸的困難度")
            
            quit_attempts = st.number_input("過去戒菸嘗試次數", min_value=0, max_value=20, value=0, help="過去曾經嘗試戒菸的次數")
    
    # 添加常見吸菸觸發因素選擇
    st.markdown("### 您的吸菸觸發因素")
    st.markdown("選擇適用於您的吸菸觸發因素（可多選）：")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trigger_stress = st.checkbox("壓力/焦慮", value=True)
        trigger_social = st.checkbox("社交場合", value=True)
        trigger_after_meals = st.checkbox("飯後習慣性吸菸", value=True)
        trigger_boredom = st.checkbox("無聊/打發時間", value=False)
    
    with col2:
        trigger_alcohol = st.checkbox("飲酒時", value=False)
        trigger_coffee = st.checkbox("喝咖啡時", value=False)
        trigger_morning = st.checkbox("早晨起床後", value=False)
        trigger_craving = st.checkbox("尼古丁渴望時", value=True)
    
    # 添加按鈕獲取戒菸計畫
    if st.button("生成我的戒菸計畫", type="primary"):
        with st.spinner("正在生成您的個性化戒菸計畫..."):
            try:
                # 計算當前健康度和收集吸菸信息
                current_health = calculate_lung_health(cigarettes_per_day, years_smoking)
                
                # 收集觸發因素
                triggers = []
                if trigger_stress:
                    triggers.append("壓力/焦慮")
                if trigger_social:
                    triggers.append("社交場合")
                if trigger_after_meals:
                    triggers.append("飯後習慣性吸菸")
                if trigger_boredom:
                    triggers.append("無聊/打發時間")
                if trigger_alcohol:
                    triggers.append("飲酒時")
                if trigger_coffee:
                    triggers.append("喝咖啡時")
                if trigger_morning:
                    triggers.append("早晨起床後")
                if trigger_craving:
                    triggers.append("尼古丁渴望時")
                
                # 判斷尼古丁依賴程度和設定尼古丁含量數值
                if cigarettes_per_day <= 10 and years_smoking <= 2 and quit_attempts == 0:
                    dependence_level = "輕度"
                elif cigarettes_per_day <= 20 and years_smoking <= 10 and quit_attempts <= 2:
                    dependence_level = "中度"
                else:
                    dependence_level = "重度"
                    
                # 將尼古丁類型轉換為具體數值，用於階段性目標
                if nicotine_type == "低尼古丁 (0.1-0.6毫克)":
                    nicotine_level = 0.5
                    nicotine_desc = "輕菸 (0.5毫克)"
                elif nicotine_type == "中尼古丁 (0.7-1.2毫克)":
                    nicotine_level = 1.0
                    nicotine_desc = "普通菸 (1.0毫克)"
                else:
                    nicotine_level = 1.5
                    nicotine_desc = "濃菸 (1.5毫克)"
                
                # 生成戒菸計畫時長 - 依據依賴程度和歷史
                if dependence_level == "輕度":
                    plan_duration_weeks = 4
                elif dependence_level == "中度":
                    plan_duration_weeks = 8
                else:
                    plan_duration_weeks = 12
                
                # 生成戒菸計畫
                st.success("您的個性化戒菸計畫已生成！")
                
                # 計畫概述
                st.markdown(f"""
                <div style="background-color:#f0f7ff; padding:20px; border-radius:10px; margin-bottom:20px; border-left:5px solid #2196F3;">
                    <h3 style="color:#0d47a1; margin-top:0;">戒菸計畫概述</h3>
                    <p><strong style="color:#0d47a1;">尼古丁依賴程度:</strong> <span style="color:#1565c0; font-weight:500;">{dependence_level}</span></p>
                    <p><strong style="color:#0d47a1;">目前尼古丁含量:</strong> <span style="color:#1565c0; font-weight:500;">{nicotine_level}毫克 ({nicotine_desc})</span></p>
                    <p><strong style="color:#0d47a1;">計畫時長:</strong> <span style="color:#1565c0; font-weight:500;">{plan_duration_weeks}週</span></p>
                    <p><strong style="color:#0d47a1;">目前肺部健康度:</strong> <span style="color:#1565c0; font-weight:500;">{current_health:.1f}%</span></p>
                    <p><strong style="color:#0d47a1;">主要觸發因素:</strong> <span style="color:#1565c0; font-weight:500;">{', '.join(triggers)}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                # 階段性目標
                st.markdown("### 階段性減菸目標")
                
                # 根據依賴程度和當前吸菸量生成遞減計畫
                weekly_targets = []
                current_target = cigarettes_per_day
                
                # 計算每週減少量
                if dependence_level == "輕度":
                    reduction_rate = 0.25  # 每週減少25%
                elif dependence_level == "中度":
                    reduction_rate = 0.15  # 每週減少15%
                else:
                    reduction_rate = 0.1   # 每週減少10%
                
                # 生成每週目標
                remaining = cigarettes_per_day
                for week in range(1, plan_duration_weeks + 1):
                    if week == plan_duration_weeks:
                        target = 0  # 最後一週目標為0
                    else:
                        reduction = max(1, round(cigarettes_per_day * reduction_rate))
                        if week > plan_duration_weeks * 0.7:  # 後30%時間加速減少
                            reduction = max(1, round(reduction * 1.5))
                        remaining = max(0, remaining - reduction)
                        target = remaining
                    
                    weekly_targets.append((week, target))
                
                # 生成尼古丁級別的階段性轉換
                nicotine_targets = []
                current_nicotine = nicotine_level
                
                # 根據減菸進度同步降低尼古丁含量
                for week, target in weekly_targets:
                    # 計算尼古丁減少的比例 - 與吸菸數量減少比例相關但稍慢
                    if target == 0:
                        nicotine_target = 0  # 最終完全無尼古丁
                    else:
                        # 尼古丁降低速度稍慢於數量降低
                        reduction_ratio = 1 - (target / cigarettes_per_day)
                        nicotine_reduction = reduction_ratio * 0.8  # 80%的減菸比例
                        nicotine_target = round(nicotine_level * (1 - nicotine_reduction), 1)
                        nicotine_target = max(0.1, nicotine_target)  # 最低不小於0.1
                    
                    # 映射尼古丁數值到描述
                    if nicotine_target <= 0.2:
                        nic_desc = "超輕菸/尼古丁替代品"
                    elif nicotine_target <= 0.5:
                        nic_desc = "極輕菸"
                    elif nicotine_target <= 0.8:
                        nic_desc = "輕菸"
                    elif nicotine_target <= 1.0:
                        nic_desc = "普通菸"
                    else:
                        nic_desc = "濃菸"
                    
                    nicotine_targets.append((nicotine_target, nic_desc))
                
                # 創建階段性目標表格
                target_data = {
                    "週次": [f"第{week}週" for week, _ in weekly_targets],
                    "每日吸菸目標數量": [target for _, target in weekly_targets],
                    "建議尼古丁含量(毫克)": [nic[0] for nic in nicotine_targets],
                    "建議菸種": [nic[1] for nic in nicotine_targets],
                    "相比當前減少比例": [f"{round((1 - target/cigarettes_per_day) * 100)}%" for _, target in weekly_targets]
                }
                
                target_df = pd.DataFrame(target_data)
                st.dataframe(target_df, use_container_width=True)
                
                # 生成第一週詳細計畫
                st.markdown("### 第一週詳細戒菸計畫")
                
                # 針對個人觸發因素的替代策略
                trigger_strategies = {
                    "壓力/焦慮": ["練習深呼吸技巧 (吸氣4秒，屏息4秒，呼氣6秒)", "使用冥想應用程式每天5-10分鐘", "短暫離開壓力環境進行5分鐘步行"],
                    "社交場合": ["事先告知朋友您正在戒菸尋求支持", "手持無酒精飲料避免空手", "與其他非吸菸者待在一起"],
                    "飯後習慣性吸菸": ["飯後立即刷牙或使用漱口水改變口味", "飯後立即換環境（如散步或洗碗）", "準備水果或無糖口香糖作為飯後替代品"],
                    "無聊/打發時間": ["下載手機遊戲轉移注意力", "準備簡短的家務任務清單", "學習新技能或愛好"],
                    "飲酒時": ["暫時減少飲酒場合", "限制酒精攝入量", "選擇無酒精替代品"],
                    "喝咖啡時": ["改變咖啡飲用地點", "嘗試不同類型的茶替代部分咖啡", "使用較小的咖啡杯減少停留時間"],
                    "早晨起床後": ["改變早晨日常順序", "準備健康早餐作為替代獎勵", "晨間冥想或輕度運動"],
                    "尼古丁渴望時": ["使用尼古丁替代品（如貼片或口香糖）", "使用「渴望日誌」記錄並觀察渴望持續時間", "準備5分鐘分心活動清單"]
                }
                
                # 加入降低尼古丁的建議策略
                first_week_nicotine = nicotine_targets[0][0]
                first_week_nicotine_desc = nicotine_targets[0][1]
                
                st.markdown(f"""
                <div style="background-color:#e1f5fe; padding:15px; border-radius:10px; margin-bottom:20px; border-left:5px solid #0277bd;">
                    <h4 style="color:#01579b; margin-top:0; font-size:18px;">第一週尼古丁降低策略</h4>
                    <p style="color:#01579b; font-weight:500; font-size:16px;">目標尼古丁含量: <strong>{first_week_nicotine}毫克</strong> ({first_week_nicotine_desc})</p>
                    <ul style="color:#0288d1; font-size:15px;">
                        <li><span style="color:#0277bd; font-weight:500;">逐步將您常用的{nicotine_desc}換成{first_week_nicotine_desc}</span></li>
                        <li><span style="color:#0277bd; font-weight:500;">可考慮使用尼古丁貼片作為輔助，幫助控制尼古丁攝入</span></li>
                        <li><span style="color:#0277bd; font-weight:500;">每日記錄實際吸菸數量和尼古丁含量，監控進度</span></li>
                        <li><span style="color:#0277bd; font-weight:500;">嘗試延長吸菸間隔時間，減少尼古丁依賴</span></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # 如果用戶沒有選擇任何觸發因素，提示選擇
                if not triggers:
                    st.info("請在上方選擇您的吸菸觸發因素，以獲得個性化的戒菸建議。")
                
                # 顯示每日具體應對策略 - 直接顯示用戶選擇的觸發因素應對策略
                if triggers:  # 只有當用戶選擇了觸發因素時才顯示
                    st.markdown("### 您的觸發因素的每日具體應對策略")
                    strategy_content = "<div style='background-color:#f5f5f5; padding:15px; border-radius:10px;'>"
                    strategy_content += "<ul style='color:#424242; margin: 0;'>"
                    
                    for trigger in triggers:
                        if trigger in trigger_strategies:
                            strategy_content += f"<li style='margin-bottom:15px;'><strong style='color:#1976d2; font-size:16px;'>{trigger}:</strong><ul style='margin-top:5px;'>"
                            for strat in trigger_strategies[trigger]:
                                strategy_content += f"<li style='margin-bottom:8px;'>{strat}</li>"
                            strategy_content += "</ul></li>"
                    
                    strategy_content += "</ul></div>"
                    st.markdown(strategy_content, unsafe_allow_html=True)
                
                # 每日時間表建議
                st.markdown("### 建議每日時間表")
                
                # 產生推薦的吸菸時間（平均分布，逐漸減少）
                first_week_target = weekly_targets[0][1]
                
                if first_week_target > 0:
                    wake_hour = 7
                    sleep_hour = 23
                    waking_hours = sleep_hour - wake_hour
                    
                    if first_week_target <= waking_hours:
                        # 如果吸菸次數少於清醒小時數，平均分布
                        interval = waking_hours / (first_week_target + 1)
                        smoking_times = [wake_hour + interval * (i+1) for i in range(first_week_target)]
                    else:
                        # 否則按關鍵時刻分配
                        key_times = [7, 10, 12, 15, 18, 21]  # 關鍵時刻
                        smoking_times = key_times + [wake_hour + i * waking_hours / (first_week_target - len(key_times)) 
                                                   for i in range(first_week_target - len(key_times))]
                        smoking_times.sort()
                    
                    # 格式化時間
                    formatted_times = [f"{int(hour)}:{int((hour - int(hour)) * 60):02d}" for hour in smoking_times]
                    
                    # 創建時間表
                    time_html = "<div style='background-color:#f5f5f5; padding:15px; border-radius:10px;'>"
                    time_html += f"<p style='color:#444; font-weight:500;'>以下是建議的第一週吸菸時間表（每天{first_week_target}次）：</p>"
                    time_html += "<ul style='columns: 2; -webkit-columns: 2; -moz-columns: 2; color:#424242;'>"
                    
                    for i, time_str in enumerate(formatted_times):
                        time_html += f"<li style='margin-bottom:5px; color:#0d47a1; font-weight:500;'>{time_str}</li>"
                    
                    time_html += "</ul>"
                    time_html += "<p style='color:#444; margin-top:15px; font-style:italic;'><b>提示:</b> 將這些時間設定為手機提醒，幫助您遵循計畫並逐漸減少。在非計畫時間出現的渴望，運用上方的替代策略。</p>"
                    time_html += "</div>"
                    
                    st.markdown(time_html, unsafe_allow_html=True)
                
                # 尼古丁替代療法建議
                if dependence_level in ["中度", "重度"]:
                    st.markdown("### 尼古丁替代療法建議")
                    
                    nrt_html = "<div style='background-color:#e3f2fd; padding:15px; border-radius:10px; border-left:4px solid #2196F3;'>"
                    nrt_html += "<p style='color:#01579b; font-weight:500;'>基於您的尼古丁依賴程度，建議考慮以下尼古丁替代療法：</p><ul style='color:#0277bd;'>"
                    
                    if nicotine_content == "高尼古丁 (濃菸)":
                        nrt_html += "<li style='margin-bottom:8px;'><strong style='color:#01579b;'>尼古丁貼片（高劑量）:</strong> 前4週使用21mg/24小時，接著4週使用14mg/24小時，最後4週使用7mg/24小時</li>"
                    elif nicotine_content == "中等尼古丁 (普通菸)":
                        nrt_html += "<li style='margin-bottom:8px;'><strong style='color:#01579b;'>尼古丁貼片（中劑量）:</strong> 前4週使用14mg/24小時，接著4週使用7mg/24小時</li>"
                    else:
                        nrt_html += "<li style='margin-bottom:8px;'><strong style='color:#01579b;'>尼古丁貼片（低劑量）:</strong> 使用7mg/24小時的貼片4-8週</li>"
                    
                    nrt_html += """
                    <li style='margin-bottom:8px;'><strong style='color:#01579b;'>尼古丁口香糖:</strong> 在強烈渴望時使用，每天不超過20片2mg口香糖</li>
                    <li style='margin-bottom:8px;'><strong style='color:#01579b;'>尼古丁吸入器:</strong> 對於手口習慣強的吸菸者特別有效</li>
                    </ul>
                    <p style='color:#01579b; font-style:italic; margin-top:10px; border-top:1px solid #90caf9; padding-top:10px;'><strong>注意:</strong> 請在使用任何尼古丁替代療法前諮詢醫生或藥劑師。</p>
                    """
                    nrt_html += "</div>"
                    
                    st.markdown(nrt_html, unsafe_allow_html=True)
                
                # 戒菸的財務收益計算
                st.markdown("### 戒菸的財務收益")
                
                # 假設每包菸價格為100元，每包20支
                price_per_cigarette = 100 / 20
                daily_cost = cigarettes_per_day * price_per_cigarette
                monthly_cost = daily_cost * 30
                yearly_cost = daily_cost * 365
                five_year_cost = yearly_cost * 5
                
                financial_html = f"""
                <div style="background-color:#e8f5e9; padding:15px; border-radius:10px; border-left:4px solid #4caf50;">
                    <h4 style="color:#1b5e20;">戒菸後您將節省的金錢：</h4>
                    <table style="width:100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding:8px; border-bottom:1px solid #2e7d32; font-weight:bold; color:#2e7d32;">一個月</td>
                            <td style="padding:8px; border-bottom:1px solid #2e7d32; text-align:right; color:#2e7d32; font-weight:bold;">{monthly_cost:.0f}元</td>
                        </tr>
                        <tr>
                            <td style="padding:8px; border-bottom:1px solid #2e7d32; font-weight:bold; color:#2e7d32;">一年</td>
                            <td style="padding:8px; border-bottom:1px solid #2e7d32; text-align:right; color:#2e7d32; font-weight:bold;">{yearly_cost:.0f}元</td>
                        </tr>
                        <tr>
                            <td style="padding:8px; border-bottom:1px solid #2e7d32; font-weight:bold; color:#2e7d32;">五年</td>
                            <td style="padding:8px; border-bottom:1px solid #2e7d32; text-align:right; color:#2e7d32; font-weight:bold;">{five_year_cost:.0f}元</td>
                        </tr>
                    </table>
                    <p style="color:#1b5e20; margin-top:10px;">您可以考慮將這些節省下來的錢存入特別的「獎勵帳戶」，並在達成戒菸里程碑時犒賞自己！</p>
                </div>
                """
                
                st.markdown(financial_html, unsafe_allow_html=True)
                
                # 添加進度追蹤工具建議
                st.markdown("### 追蹤進度的工具")
                
                # 使用原生Streamlit組件代替HTML顯示追蹤工具
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 推薦的戒菸應用程式")
                    st.markdown("- QuitNow!")
                    st.markdown("- Smoke Free")
                    st.markdown("- Quitzilla")
                    st.markdown("- EasyQuit")
                
                with col2:
                    st.markdown("#### 戒菸日記建議內容")
                    st.markdown("- 每日吸菸數量記錄")
                    st.markdown("- 渴望強度 (1-10分)")
                    st.markdown("- 觸發情境紀錄")
                    st.markdown("- 成功應對策略")
                    
                # 添加戒菸日記範例
                st.markdown("#### 戒菸日記範例")
                diary_example = """
                | 日期 | 吸菸數量 | 渴望強度 | 觸發情境 | 應對方法 | 感受 |
                |------|----------|----------|----------|----------|------|
                | 5/23 | 15支 | 8分 | 早會後壓力大 | 深呼吸5分鐘 | 渴望減輕但仍吸菸 |
                | 5/24 | 14支 | 7分 | 與朋友聚餐 | 告知朋友正在戒菸 | 成功減少1支 |
                | 5/25 | 13支 | 9分 | 工作壓力 | 改喝茶而非咖啡 | 下午渴望特別強 |
                | 5/26 | 12支 | 6分 | 習慣性飯後吸菸 | 飯後立即刷牙 | 開始感受到進步 |
                | 5/27 | 12支 | 6分 | 早晨起床 | 先喝水再做5分鐘伸展 | 維持昨天的成果 |
                """
                st.markdown(diary_example)
                
                # 獲取戒煙資源
                from gemini_assistant import get_quitting_resources
                resources = get_quitting_resources()
                
                # 顯示戒煙資源
                st.markdown("### 戒菸資源與支援服務")
                
                # 建立選項卡
                resource_tabs = st.tabs(list(resources.keys()))
                
                # 在每個選項卡中顯示對應資源
                for i, (category, resource_list) in enumerate(resources.items()):
                    with resource_tabs[i]:
                        for resource in resource_list:
                            st.markdown(f"• {resource}")
            
            except Exception as e:
                st.error(f"獲取AI建議時出錯: {str(e)}")
                st.info("請稍後再試，或聯繫專業醫生獲取戒菸建議。")
    
    # 肺部比較部分已刪除
    
    # 健康影響部分已刪除
    
    # 教育資訊部分已刪除

# Add sidebar with additional information
with st.sidebar:
    st.header("About This Tool")
    st.markdown("""
    This visualization tool uses medical research and statistical models to estimate the progression of lung deterioration based on smoking habits.
    
    The visualization is based on averages and individual results may vary based on:
    - Genetic factors
    - Environmental conditions
    - Overall health status
    - Depth of inhalation
    - Type of cigarettes
    
    **Note**: This tool is for educational purposes only and does not constitute medical advice. Consult a healthcare professional for personalized guidance.
    """)
    
    st.divider()
    
    st.markdown("""
    **Sources**:
    - World Health Organization
    - American Lung Association
    - Centers for Disease Control and Prevention
    """)
