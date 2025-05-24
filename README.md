# 吸菸肺部健康視覺化工具

這是一個基於科學依據的互動式應用程式，旨在向用戶展示吸菸對肺部健康的影響。通過視覺化技術，用戶可以清楚看到基於其吸菸習慣，肺部健康受損的程度。

## 專案說明

本專案旨在通過直觀的視覺化方式展示吸菸對肺部健康的影響，幫助用戶了解吸菸的危害，並提供個性化的戒菸建議。應用程式採用科學研究數據，結合先進的視覺化技術，呈現逼真的肺部健康變化效果。

## 功能特點

- **真實肺部視覺化**：基於醫學研究的肺部視覺效果，隨著健康度變化顯示煙焦油沉積
- **健康評估**：根據吸菸量、年限、尼古丁和焦油含量計算肺部健康度
- **癌症風險評估**：提供與非吸菸者相比的癌症風險數據
- **個性化戒菸建議**：使用Gemini AI生成適合用戶情況的戒菸計劃
- **經濟影響分析**：計算吸菸的累計花費並與其他消費選擇進行比較
- **繁體中文介面**：完全本地化的使用體驗

## 技術實現

- **前端**：Streamlit互動式介面
- **視覺化**：Matplotlib生成的動態肺部圖像
- **AI整合**：Google Gemini API提供個性化建議
- **數據處理**：基於科學研究的肺部健康計算模型

## 檔案結構

- `main.py`: 主程式入口，包含Streamlit界面設計
- `utils.py`: 工具函數，包含健康計算模型
- `lung_svg_generator.py`: 肺部視覺化生成器
- `gemini_assistant.py`: Gemini AI整合功能
- `data.txt`: 參考數據和科學依據

## 安裝與使用

1. 克隆此專案:
```
git clone https://github.com/JUSTIN20020920/B11008068.git
cd B11008068
```

2. 安裝依賴:
```
pip install streamlit google-generativeai matplotlib numpy pandas
```

3. 設置環境變數:
將`GEMINI_API_KEY`添加到您的環境變數中

4. 運行應用程式:
```
streamlit run main.py
```

## 科學依據

本應用程式的視覺化和計算模型基於以下醫學研究:

- [美國癌症協會研究](https://www.cancer.org/cancer/lung-cancer/causes-risks-prevention/what-causes.html)
- [新英格蘭醫學期刊吸菸研究](https://www.nejm.org/doi/full/10.1056/NEJMra1308383)
- [世界衛生組織煙草影響報告](https://www.who.int/news-room/fact-sheets/detail/tobacco)
- [美國國家衛生研究院資料](https://www.nhlbi.nih.gov/health-topics/smoking-and-your-heart)

## 貢獻者

- 開發者: JUSTIN20020920

## 授權

此專案採用MIT授權條款 - 詳情請參閱LICENSE文件