#!/usr/bin/env python3
"""
主程式模塊：廖貫呈的個人作品集
"""
from flask import Flask, render_template
import utils

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

@app.route('/')
def home():
    """渲染首頁"""
    return render_template('index.html')

@app.route('/slideshow')
def slideshow():
    """渲染幻燈片頁面"""
    return render_template('slideshow.html')

@app.route('/projects')
def projects():
    """渲染專案頁面"""
    # 從utils模塊獲取專案數據
    project_data = utils.get_project_data()
    return render_template('projects.html', projects=project_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)