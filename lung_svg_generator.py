import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import math
from matplotlib.patches import Ellipse, Circle, PathPatch, FancyBboxPatch
import matplotlib.path as mpath
import matplotlib.transforms as mtransforms
import matplotlib.collections as mcollections
import random
from matplotlib.colors import LinearSegmentedColormap

def create_realistic_lung_path(ax, x_center, y_center, scale=1.0, is_left=True):
    """
    Create a more anatomically accurate lung shape based on medical imaging
    """
    # This function creates a highly anatomically correct lung shape based on reference image
    if is_left:
        # Left lung has more rounded top and concave medial surface
        lung_path = [
            (x_center - 0.3*scale, y_center + 2.2*scale),  # Top point
            (x_center - 1.2*scale, y_center + 1.8*scale),  # Upper left
            (x_center - 1.7*scale, y_center + 1.0*scale),  # Upper middle left
            (x_center - 1.9*scale, y_center + 0.0*scale),  # Middle left
            (x_center - 1.8*scale, y_center - 1.0*scale),  # Lower middle left
            (x_center - 1.5*scale, y_center - 1.8*scale),  # Lower left
            (x_center - 0.8*scale, y_center - 2.3*scale),  # Bottom left
            (x_center + 0.0*scale, y_center - 2.4*scale),  # Bottom point
            (x_center + 0.4*scale, y_center - 1.8*scale),  # Bottom right (medial)
            (x_center + 0.3*scale, y_center - 0.5*scale),  # Middle right (medial)
            (x_center + 0.2*scale, y_center + 0.5*scale),  # Upper middle (medial)
            (x_center + 0.0*scale, y_center + 1.5*scale),  # Upper medial surface
            (x_center - 0.3*scale, y_center + 2.2*scale),  # Back to top
        ]
    else:
        # Right lung is shorter and wider with 3 lobes
        lung_path = [
            (x_center + 0.3*scale, y_center + 2.0*scale),  # Top point
            (x_center + 1.2*scale, y_center + 1.8*scale),  # Upper right
            (x_center + 1.8*scale, y_center + 1.0*scale),  # Upper middle right
            (x_center + 2.0*scale, y_center + 0.0*scale),  # Middle right
            (x_center + 1.9*scale, y_center - 1.0*scale),  # Lower middle right
            (x_center + 1.6*scale, y_center - 1.8*scale),  # Lower right
            (x_center + 0.9*scale, y_center - 2.3*scale),  # Bottom right
            (x_center + 0.0*scale, y_center - 2.2*scale),  # Bottom point
            (x_center - 0.4*scale, y_center - 1.8*scale),  # Bottom left (medial)
            (x_center - 0.3*scale, y_center - 0.5*scale),  # Middle left (medial)
            (x_center - 0.2*scale, y_center + 0.5*scale),  # Upper middle (medial)
            (x_center - 0.0*scale, y_center + 1.5*scale),  # Upper medial surface
            (x_center + 0.3*scale, y_center + 2.0*scale),  # Back to top
        ]
    
    # Create the path with cubic splines for smoother anatomy
    codes = [mpath.Path.MOVETO]
    for i in range(1, len(lung_path) - 1):
        codes.append(mpath.Path.CURVE4 if i % 3 == 1 else mpath.Path.CURVE4)
    codes.append(mpath.Path.CLOSEPOLY)
    
    # Make sure we have the right number of codes
    if len(codes) != len(lung_path):
        # Fall back to a simpler approach
        codes = [mpath.Path.MOVETO] + [mpath.Path.CURVE3] * (len(lung_path) - 2) + [mpath.Path.CLOSEPOLY]
    
    path = mpath.Path(lung_path, codes)
    return path

def draw_realistic_bronchi(ax):
    """Draw a more realistic branching bronchi structure based on medical reference"""
    # Main trachea (windpipe) - more anatomically correct color
    trachea_color = '#BB8585'  # Pink/reddish color similar to real trachea
    
    # Draw trachea with slight curve like in real anatomy
    ax.plot([5, 5], [9.8, 8.5], color=trachea_color, linewidth=6)
    ax.plot([5, 5.1], [8.5, 7.8], color=trachea_color, linewidth=6)
    
    # Carina (where trachea divides)
    ax.plot([5.1, 4.3], [7.8, 7.2], color=trachea_color, linewidth=5)
    ax.plot([5.1, 5.9], [7.8, 7.2], color=trachea_color, linewidth=5)
    
    # Main bronchi - slightly curved like in human anatomy
    # Left main bronchus (longer, more horizontal)
    ax.plot([4.3, 3.6], [7.2, 6.9], color=trachea_color, linewidth=4)
    
    # Right main bronchus (shorter, more vertical)
    ax.plot([5.9, 6.4], [7.2, 6.7], color=trachea_color, linewidth=4)
    
    # Secondary bronchi - left lung (upper and lower lobe bronchi)
    ax.plot([3.6, 3.2], [6.9, 7.2], color=trachea_color, linewidth=3)  # Upper lobe
    ax.plot([3.6, 3.0], [6.9, 6.2], color=trachea_color, linewidth=3)  # Lower lobe
    
    # Secondary bronchi - right lung (upper, middle, lower lobe bronchi)
    ax.plot([6.4, 6.8], [6.7, 7.2], color=trachea_color, linewidth=3)  # Upper lobe
    ax.plot([6.4, 6.9], [6.7, 6.3], color=trachea_color, linewidth=3)  # Middle lobe
    ax.plot([6.4, 6.7], [6.7, 5.9], color=trachea_color, linewidth=3)  # Lower lobe
    
    # Tertiary bronchi with branching pattern - left upper lobe
    ax.plot([3.2, 2.8], [7.2, 7.5], color=trachea_color, linewidth=2)
    ax.plot([3.2, 2.9], [7.2, 6.9], color=trachea_color, linewidth=2)
    
    # Tertiary bronchi - left lower lobe
    ax.plot([3.0, 2.6], [6.2, 6.4], color=trachea_color, linewidth=2)
    ax.plot([3.0, 2.7], [6.2, 5.8], color=trachea_color, linewidth=2)
    ax.plot([3.0, 3.3], [6.2, 5.8], color=trachea_color, linewidth=2)
    
    # Tertiary bronchi - right upper lobe
    ax.plot([6.8, 7.2], [7.2, 7.4], color=trachea_color, linewidth=2)
    ax.plot([6.8, 7.0], [7.2, 6.9], color=trachea_color, linewidth=2)
    
    # Tertiary bronchi - right middle and lower lobes
    ax.plot([6.9, 7.3], [6.3, 6.5], color=trachea_color, linewidth=2)
    ax.plot([6.7, 7.1], [5.9, 5.6], color=trachea_color, linewidth=2)
    ax.plot([6.7, 6.9], [5.9, 5.4], color=trachea_color, linewidth=2)

def create_lung_image(ax, health_percentage):
    """
    Create a realistic lung visualization on the given matplotlib axes.
    
    Parameters:
    ax: matplotlib axes to draw on
    health_percentage (float): Percentage of lung health (0-100)
    """
    # Set consistent random seed for consistent tar patterns at each health level
    random.seed(int(health_percentage))
    
    # Set up colors based on health percentage - 更準確地反映吸菸肺部的實際色彩變化
    # 對照醫學圖像參考，吸菸肺部會從粉紅色健康肺組織轉變為黑色沉積
    # 重新調整顏色階梯，使其更接近實際臨床觀察
    if health_percentage >= 99:
        lung_color = "#E5ACAC"  # 完全健康的粉紅色
        tar_opacity = 0.1
    elif health_percentage >= 95:
        lung_color = "#D9A09F"  # 非常輕微受損
        tar_opacity = 0.2
    elif health_percentage >= 90:
        lung_color = "#CE9594"  # 輕微受損
        tar_opacity = 0.35
    elif health_percentage >= 85:
        lung_color = "#C38B8A"  # 初期受損
        tar_opacity = 0.4
    elif health_percentage >= 80:
        lung_color = "#B87F7E"  # 明顯受損
        tar_opacity = 0.55
    elif health_percentage >= 75:
        lung_color = "#A37170"  # 中輕度受損，更深的紅褐色
        tar_opacity = 0.6
    elif health_percentage >= 70:
        lung_color = "#8E625F"  # 中度受損，朝向更暗的色調
        tar_opacity = 0.65
    elif health_percentage >= 60:
        lung_color = "#79514E"  # 中重度受損，明顯的暗褐色
        tar_opacity = 0.7
    elif health_percentage >= 50:
        lung_color = "#64413E"  # 重度受損，深褐色
        tar_opacity = 0.75
    elif health_percentage >= 40:
        lung_color = "#503130"  # 嚴重受損，朝向黑色的深褐色
        tar_opacity = 0.8
    elif health_percentage >= 30:
        lung_color = "#3C2625"  # 極嚴重受損，非常深的褐黑色
        tar_opacity = 0.85
    elif health_percentage >= 20:
        lung_color = "#2A1B1A"  # 近乎喪失功能，幾乎是黑色
        tar_opacity = 0.9
    elif health_percentage >= 10:
        lung_color = "#1C1110"  # 幾乎完全喪失功能，近黑色
        tar_opacity = 0.95
    else:
        lung_color = "#110A0A"  # 完全喪失功能 - 接近純黑色
        tar_opacity = 1.0
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Draw the bronchi tree (more realistic)
    draw_realistic_bronchi(ax)
    
    # Create custom paths for more realistic lung shapes
    left_lung_path = create_realistic_lung_path(ax, 3.5, 4, 2.5, is_left=True)
    right_lung_path = create_realistic_lung_path(ax, 6.5, 4, 2.5, is_left=False)
    
    # Draw the lungs with the realistic paths
    left_lung = PathPatch(left_lung_path, facecolor=lung_color, edgecolor='#444444', linewidth=1)
    right_lung = PathPatch(right_lung_path, facecolor=lung_color, edgecolor='#444444', linewidth=1)
    
    ax.add_patch(left_lung)
    ax.add_patch(right_lung)
    
    # Add shading to make lungs appear more 3D
    ax.add_collection(mcollections.LineCollection(
        [[(3.5-1.5, 4), (3.5, 4+1.5)]], 
        colors=[(0,0,0,0.1)], linewidths=5
    ))
    ax.add_collection(mcollections.LineCollection(
        [[(6.5+1.5, 4), (6.5, 4+1.5)]], 
        colors=[(0,0,0,0.1)], linewidths=5
    ))
    
    # Add alveoli texture
    for i in range(int(12 * health_percentage / 100)):
        # Left lung alveoli
        alv_x = 3.5 + (random.random() - 0.5) * 1.8
        alv_y = 4 + (random.random() - 0.5) * 3
        if left_lung_path.contains_point((alv_x, alv_y)):
            # Create small bubble-like circles for alveoli
            alveoli = Circle((alv_x, alv_y), 0.1, 
                           facecolor='#FFB6B6', 
                           edgecolor='#DDA0A0', 
                           linewidth=0.5,
                           alpha=0.6)
            ax.add_patch(alveoli)
            
        # Right lung alveoli
        alv_x = 6.5 + (random.random() - 0.5) * 1.8
        alv_y = 4 + (random.random() - 0.5) * 3
        if right_lung_path.contains_point((alv_x, alv_y)):
            # Create small bubble-like circles for alveoli
            alveoli = Circle((alv_x, alv_y), 0.1, 
                           facecolor='#FFB6B6', 
                           edgecolor='#DDA0A0', 
                           linewidth=0.5,
                           alpha=0.6)
            ax.add_patch(alveoli)
    
    # Add realistic tobacco-related damage based on medical research and reference images of damaged lungs
    # References: 
    # - American Cancer Society: Lung damage patterns
    # - Journal of Thoracic Imaging: Cigarette smoking-related lung changes
    # - New England Journal of Medicine: Effects of smoking on lung tissue
    # - Reference medical image showing severe tar deposition in damaged lungs
    
    if health_percentage < 100:
        # Stages of smoke damage based on medical literature
        damage_stage = 5 - int(health_percentage / 20)  # 1-5 scale (mild to severe)
        
        # 黑色焦油斑點的數量基於損傷程度
        tar_spot_count = int(50 * (5 - health_percentage/20) / 5)
        
        # =========================================================================
        # Stage 1: Early Changes (90-100% health)
        # =========================================================================
        # - Earliest changes seen in epithelium of small airways
        # - Mild inflammation in respiratory bronchioles
        # - Increased mucus production
        # =========================================================================
        if damage_stage >= 1:
            # Increased mucus production in bronchioles
            bronchiole_points = [
                (4.2, 6.2), (5.8, 6.2),  # Upper bronchioles
                (3.8, 5.5), (6.2, 5.5),  # Middle bronchioles
            ]
            
            for point in bronchiole_points:
                mucus = Ellipse(point, 0.15, 0.08, 
                             facecolor='#E2D2D2', 
                             edgecolor='#D4C2C2', 
                             alpha=0.7, 
                             linewidth=0.5)
                ax.add_patch(mucus)
            
            # Mild inflammation spots around small airways
            for i in range(8):
                if i % 2 == 0:  # Left lung
                    x = 3.5 + (random.random() - 0.5) * 1.2
                    y = 5.5 + (random.random() - 0.5) * 0.8
                else:  # Right lung
                    x = 6.5 + (random.random() - 0.5) * 1.2
                    y = 5.5 + (random.random() - 0.5) * 0.8

                if (i % 2 == 0 and left_lung_path.contains_point((x, y))) or \
                   (i % 2 == 1 and right_lung_path.contains_point((x, y))):
                    inflammation = Circle((x, y), 0.08, 
                                      facecolor='#E88A8A', 
                                      edgecolor=None, 
                                      alpha=0.6)
                    ax.add_patch(inflammation)
        
        # =========================================================================
        # Stage 2: Mild Damage (70-90% health)
        # - Accumulation of pigmented macrophages
        # - Respiratory bronchiolitis
        # - Early centrilobular emphysema
        # - Peripheral fibrosis begins
        # =========================================================================
        if damage_stage >= 2:
            # Add pigment accumulation (macrophages with tar) - 更多分布在整個肺部
            # 根據健康百分比動態調整斑點數量，即使是輕度損傷也顯示足夠多的斑點
            spot_count = int(40 + (100 - health_percentage) * 0.8)  # 健康度越低，斑點越多
            for i in range(spot_count):  # 動態調整數量
                # 徹底改變分布方式，使焦油斑點更均勻地分布在整個肺部區域
                # 不再依賴固定的分布類型，而是使用整個肺部的範圍
                if i % 2 == 0:  # Left lung
                    x_center = 3.5
                    # 計算與肺部中心的距離係數，確保更多點分布在肺部邊緣
                    distance_factor = 0.5 + random.random() * 1.0  # 0.5-1.5範圍，保證更多點在邊緣
                    
                    angle = random.random() * 2 * 3.14159  # 隨機角度 (0-2π)
                    x_offset = distance_factor * math.cos(angle) * 1.7  # x方向偏移
                    y_offset = distance_factor * math.sin(angle) * 2.3  # y方向偏移，略大一些以覆蓋縱向更長的肺部
                    
                    x = x_center + x_offset
                    y = 4 + y_offset
                else:  # Right lung
                    x_center = 6.5
                    # 計算與肺部中心的距離係數，確保更多點分布在肺部邊緣
                    distance_factor = 0.5 + random.random() * 1.0  # 0.5-1.5範圍，保證更多點在邊緣
                    
                    angle = random.random() * 2 * 3.14159  # 隨機角度 (0-2π)
                    x_offset = distance_factor * math.cos(angle) * 1.7  # x方向偏移
                    y_offset = distance_factor * math.sin(angle) * 2.3  # y方向偏移，略大一些以覆蓋縱向更長的肺部
                    
                    x = x_center + x_offset
                    y = 4 + y_offset

                if (i % 2 == 0 and left_lung_path.contains_point((x, y))) or \
                   (i % 2 == 1 and right_lung_path.contains_point((x, y))):
                    # Pigmented macrophages - 使用更暗的色調和更大的尺寸
                    tar_intensity = (100 - health_percentage) / 20  # 進一步增強視覺影響
                    # 健康度降低時增加斑點尺寸
                    macrophage_size = 0.2 + random.random() * 0.2 + (100 - health_percentage) / 100 * 0.15
                    # 提高不透明度以增強視覺效果
                    macrophage_opacity = 0.75 + (100 - health_percentage) / 100 * 0.2
                    
                    # 根據健康度動態選擇顏色，進一步強化更深的黑色
                    tar_colors = ['#443333', '#332222', '#221111', '#110000']
                    # 即使在高健康度時也使用較深顏色
                    color_index = min(3, int((100 - health_percentage) / 20))
                    tar_color = tar_colors[color_index]
                    
                    macrophage = Circle((x, y), macrophage_size, 
                                     facecolor=tar_color, 
                                     edgecolor=None, 
                                     alpha=macrophage_opacity)
                    ax.add_patch(macrophage)
            
            # Early bronchiolitis - 更廣泛分布在整個肺部
            # 動態調整數量，根據健康度增加炎症點
            inflammation_count = int(20 + (100 - health_percentage) * 0.6)  # 健康度越低，炎症點越多
            for i in range(inflammation_count):  # 動態調整數量
                # 使用相同的極坐標分布方法，確保均勻覆蓋整個肺部
                if i % 2 == 0:  # Left lung
                    x_center = 3.5
                    # 使用距離因子確保點分布在整個肺部，包括邊緣
                    distance_factor = 0.3 + random.random() * 1.2  # 0.3-1.5範圍，覆蓋從中心到邊緣
                    
                    angle = random.random() * 2 * math.pi  # 隨機角度 (0-2π)
                    x_offset = distance_factor * math.cos(angle) * 1.6  # x方向偏移
                    y_offset = distance_factor * math.sin(angle) * 2.2  # y方向偏移，略大以覆蓋縱向
                    
                    x = x_center + x_offset
                    y = 4 + y_offset
                else:  # Right lung
                    x_center = 6.5
                    # 使用距離因子確保點分布在整個肺部，包括邊緣
                    distance_factor = 0.3 + random.random() * 1.2  # 0.3-1.5範圍，覆蓋從中心到邊緣
                    
                    angle = random.random() * 2 * math.pi  # 隨機角度 (0-2π)
                    x_offset = distance_factor * math.cos(angle) * 1.6  # x方向偏移
                    y_offset = distance_factor * math.sin(angle) * 2.2  # y方向偏移
                    
                    x = x_center + x_offset
                    y = 4 + y_offset

                if (i % 2 == 0 and left_lung_path.contains_point((x, y))) or \
                   (i % 2 == 1 and right_lung_path.contains_point((x, y))):
                    # Inflamed bronchioles - 更明顯的顏色和尺寸
                    # 健康度降低時增加大小
                    bronchiolitis_size = 0.18 + random.random() * 0.12 + (100 - health_percentage) / 100 * 0.1
                    # 增強不透明度
                    bronchiolitis_opacity = 0.6 + (100 - health_percentage) / 100 * 0.35
                    
                    # 根據健康度調整顏色，即使是高健康度也使用較明顯的顏色
                    if health_percentage >= 85:
                        face_color = '#CC7777'
                        edge_color = '#BB6666'
                    elif health_percentage >= 70:
                        face_color = '#BB6666'
                        edge_color = '#AA5555'
                    else:
                        face_color = '#AA5555'
                        edge_color = '#994444'
                    
                    bronchiolitis = Circle((x, y), bronchiolitis_size,
                                        facecolor=face_color,
                                        edgecolor=edge_color,
                                        alpha=bronchiolitis_opacity,
                                        linewidth=0.7)  # 加粗線條
                    ax.add_patch(bronchiolitis)
        
        # =========================================================================
        # Stage 3: Moderate Damage (50-70% health)
        # - Diffuse centrilobular emphysema
        # - Increased fibrosis around airways
        # - Goblet cell hyperplasia
        # - Smooth muscle hypertrophy
        # =========================================================================
        if damage_stage >= 3:
            # Add emphysema patches (enlarged, damaged air spaces)
            for i in range(20):
                side = i % 2
                region = i % 5  # 0=upper, 1=upper-mid, 2=mid, 3=mid-lower, 4=lower
                
                if side == 0:  # Left lung
                    x_center = 3.5
                    x_offset = (random.random() - 0.5) * 1.6
                else:  # Right lung
                    x_center = 6.5
                    x_offset = (random.random() - 0.5) * 1.6
                
                if region == 0:  # Upper 
                    y = 4 + 1.5 + (random.random() - 0.5) * 0.8
                elif region == 1:  # Upper-mid
                    y = 4 + 0.8 + (random.random() - 0.5) * 0.8
                elif region == 2:  # Mid
                    y = 4 + (random.random() - 0.5) * 0.8
                elif region == 3:  # Mid-lower
                    y = 4 - 0.8 + (random.random() - 0.5) * 0.8
                else:  # Lower
                    y = 4 - 1.5 + (random.random() - 0.5) * 0.8

                # Position with more realistic distribution
                x = x_center + x_offset

                if (side == 0 and left_lung_path.contains_point((x, y))) or \
                   (side == 1 and right_lung_path.contains_point((x, y))):
                   
                    # Emphysema appears as abnormally enlarged air spaces
                    emphysema_size = 0.15 + random.random() * 0.1
                    emphysema = Circle((x, y), emphysema_size,
                                    facecolor='#FFDDDD',
                                    edgecolor='#E8C0C0',
                                    alpha=0.7,
                                    linewidth=0.5)
                    ax.add_patch(emphysema)
            
            # Add fibrosis (scarring) around airways
            fibrosis_areas = [
                (3.8, 6.0, 0.25), (6.2, 6.0, 0.25),  # Upper airways
                (3.5, 5.0, 0.3), (6.5, 5.0, 0.3),    # Mid airways
                (3.2, 4.0, 0.2), (6.8, 4.0, 0.2),    # Lower airways
            ]
            
            for x, y, size in fibrosis_areas:
                fibrosis = Circle((x, y), size,
                                facecolor='#AA7777',
                                edgecolor='#996666',
                                alpha=0.4,
                                linewidth=0.5)
                ax.add_patch(fibrosis)
        
        # =========================================================================
        # Stage 4: Severe Damage (25-50% health)
        # - Diffuse emphysema throughout lungs
        # - Bullae formation
        # - Bronchial wall thickening
        # - Significant fibrosis and scarring
        # - Black carbon and tar deposits
        # =========================================================================
        if damage_stage >= 4:
            # Black carbon/tar deposits throughout lungs
            # More prominent in upper lobes (per medical research)
            upper_tar_count = 25
            lower_tar_count = 15
            
            # Upper lobe deposits (heaviest concentration)
            for i in range(upper_tar_count):
                if i % 2 == 0:  # Left upper lobe
                    x = 3.5 + (random.random() - 0.5) * 1.5
                    y = 4 + 1 + random.random() * 1.5
                else:  # Right upper lobe  
                    x = 6.5 + (random.random() - 0.5) * 1.5
                    y = 4 + 1 + random.random() * 1.5
                
                if (i % 2 == 0 and left_lung_path.contains_point((x, y))) or \
                   (i % 2 == 1 and right_lung_path.contains_point((x, y))):
                    size = 0.15 + (0.1 * random.random())
                    tar_spot = Circle((x, y), size, 
                                   facecolor='#000000', 
                                   alpha=0.7)
                    ax.add_patch(tar_spot)
            
            # Lower lung tar deposits (less concentrated but still present)
            for i in range(lower_tar_count):
                if i % 2 == 0:  # Left lower areas
                    x = 3.5 + (random.random() - 0.5) * 1.5
                    y = 4 - random.random() * 2
                else:  # Right lower areas
                    x = 6.5 + (random.random() - 0.5) * 1.5
                    y = 4 - random.random() * 2
                
                if (i % 2 == 0 and left_lung_path.contains_point((x, y))) or \
                   (i % 2 == 1 and right_lung_path.contains_point((x, y))):
                    size = 0.1 + (0.1 * random.random())
                    tar_spot = Circle((x, y), size, 
                                   facecolor='#000000', 
                                   alpha=0.5)
                    ax.add_patch(tar_spot)
            
            # Add bullae (larger emphysematous areas)
            for i in range(8):
                if i % 2 == 0:  # Left lung
                    x = 3.5 + (random.random() - 0.5) * 1.4
                    y = 4 + (random.random() - 1) * 2.5
                else:  # Right lung
                    x = 6.5 + (random.random() - 0.5) * 1.4
                    y = 4 + (random.random() - 1) * 2.5
                
                if (i % 2 == 0 and left_lung_path.contains_point((x, y))) or \
                   (i % 2 == 1 and right_lung_path.contains_point((x, y))):
                    bulla_size = 0.3 + random.random() * 0.2
                    bulla = Circle((x, y), bulla_size,
                                facecolor='#F8E0E0',
                                edgecolor='#E0C0C0',
                                alpha=0.8,
                                linewidth=0.5)
                    ax.add_patch(bulla)
        
        # =========================================================================
        # Stage 5: Critical Damage (<25% health)
        # - Extensive emphysema and bullae
        # - Honeycomb lung appearance
        # - Major portions of non-functional tissue
        # - Advanced pigmentation and fibrosis
        # - Severe parenchymal destruction
        # =========================================================================
        if damage_stage >= 5:
            # Dark tar patches throughout lungs - much more extensive and darker
            # 參考圖片顯示大量焦油沉積，覆蓋整個肺部表面，而不僅僅是中間
            for i in range(160):  # 進一步增加焦油斑點的數量
                # 使用極坐標分布方法，確保斑點均勻覆蓋整個肺部
                if i % 2 == 0:  # Left lung
                    x_center = 3.5
                    # 使用距離因子確保點分布在整個肺部，與中心距離分布更均勻
                    # 增加r值範圍使更多點分布在邊緣
                    r = 0.2 + 1.5 * math.sqrt(random.random())  # 平方根分布使點更均勻分布在面積上
                    
                    angle = random.random() * 2 * math.pi  # 隨機角度 (0-2π)
                    x_offset = r * math.cos(angle) * 1.6  # x方向偏移
                    y_offset = r * math.sin(angle) * 2.2  # y方向偏移，略大以覆蓋縱向
                    
                    x = x_center + x_offset
                    y = 4 + y_offset
                else:  # Right lung
                    x_center = 6.5
                    # 使用距離因子確保點分布在整個肺部，與中心距離分布更均勻
                    # 增加r值範圍使更多點分布在邊緣
                    r = 0.2 + 1.5 * math.sqrt(random.random())  # 平方根分布使點更均勻分布在面積上
                    
                    angle = random.random() * 2 * math.pi  # 隨機角度 (0-2π)
                    x_offset = r * math.cos(angle) * 1.6  # x方向偏移
                    y_offset = r * math.sin(angle) * 2.2  # y方向偏移
                    
                    x = x_center + x_offset
                    y = 4 + y_offset
                
                if (i % 2 == 0 and left_lung_path.contains_point((x, y))) or \
                   (i % 2 == 1 and right_lung_path.contains_point((x, y))):
                    # 使用大小不一的黑色區塊，而不僅僅是小圓點
                    # 在健康度較低時使用更大的黑色區塊
                    size_factor = 1.0 + (100 - health_percentage) / 40  # 健康度越低，尺寸越大
                    # 使用更大的尺寸範圍
                    size = (0.3 + (0.5 * random.random())) * size_factor  # 更大的斑點
                    
                    # 使用更深的黑色，接近真實的煙焦油顏色
                    tar_colors = ['#100808', '#080404', '#000000']
                    tar_color = random.choice(tar_colors)
                    
                    # 使用不同形狀，有些是圓形，有些是橢圓形
                    if random.random() > 0.3:  # 70%使用圓形
                        tar_patch = Circle((x, y), size, 
                                        facecolor=tar_color, 
                                        alpha=0.9)  # 更高的不透明度
                    else:  # 30%使用橢圓形，呈現更自然的形狀
                        width = size * (0.8 + random.random() * 0.4)
                        height = size * (0.8 + random.random() * 0.4)
                        angle = random.random() * 360  # 隨機角度
                        tar_patch = Ellipse((x, y), width, height, angle=angle,
                                         facecolor=tar_color, 
                                         alpha=0.9)
                    
                    ax.add_patch(tar_patch)
            
            # 添加大片焦油覆蓋區域，模擬真實吸菸肺部中的大片黑色區域
            # 大幅增加黑色區域的數量和大小，特別是在肺部健康度低的情況下
            
            # 根據健康度動態生成黑色區域的數量
            black_areas_count = 25 + int((100 - health_percentage) / 5)  # 健康度為0時最多45個大塊區域
            
            # 隨機生成分布在整個肺部的大片黑色區域
            major_tar_areas = []
            
            # 左肺生成點
            for _ in range(black_areas_count // 2):
                # 使用極坐標方法生成點，確保均勻覆蓋
                r = 0.2 + 1.5 * math.sqrt(random.random())
                angle = random.random() * 2 * math.pi
                x = 3.5 + r * math.cos(angle) * 1.6
                y = 4 + r * math.sin(angle) * 2.2
                
                # 大小隨健康度變化，健康度越低，黑斑越大
                size = 0.6 + random.random() * 0.7 + (100 - health_percentage) / 100 * 0.9
                
                major_tar_areas.append((x, y, size))
                
            # 右肺生成點
            for _ in range(black_areas_count // 2):
                r = 0.2 + 1.5 * math.sqrt(random.random())
                angle = random.random() * 2 * math.pi
                x = 6.5 + r * math.cos(angle) * 1.6
                y = 4 + r * math.sin(angle) * 2.2
                
                # 大小隨健康度變化
                size = 0.6 + random.random() * 0.7 + (100 - health_percentage) / 100 * 0.9
                
                major_tar_areas.append((x, y, size))
            
            # 渲染所有大片黑色區域
            for x, y, size in major_tar_areas:
                if (x < 5 and left_lung_path.contains_point((x, y))) or \
                   (x >= 5 and right_lung_path.contains_point((x, y))):
                    # 使用不規則形狀創建更自然的大片焦油形狀
                    shape_type = random.choice(['ellipse', 'blob'])
                    
                    if shape_type == 'ellipse':
                        # 橢圓形狀
                        width = size * (0.8 + random.random() * 0.4)
                        height = size * (0.8 + random.random() * 0.4)
                        angle = random.random() * 360  # 完全隨機角度
                        tar_patch = Ellipse((x, y), width, height, angle=angle,
                                         facecolor='#000000', 
                                         alpha=0.95)  # 幾乎完全不透明
                    else:
                        # 圓形但更大
                        tar_patch = Circle((x, y), size * 1.1,
                                        facecolor='#000000', 
                                        alpha=0.95)
                    
                    ax.add_patch(tar_patch)
            
            # Honeycomb pattern in lower lungs (sign of end-stage lung disease)
            # 在參考圖片中，肺部有顯著的蜂窩狀結構
            for i in range(25):  # 增加蜂窩結構的數量
                if i % 2 == 0:  # Left lower lung
                    x = 3.5 + (random.random() - 0.5) * 1.5
                    y = 4 - 1 - random.random() * 1.2
                else:  # Right lower lung
                    x = 6.5 + (random.random() - 0.5) * 1.5
                    y = 4 - 1 - random.random() * 1.2
                
                if (i % 2 == 0 and left_lung_path.contains_point((x, y))) or \
                   (i % 2 == 1 and right_lung_path.contains_point((x, y))):
                    # 更深色的蜂窩結構，更接近參考圖片
                    honeycomb = Circle((x, y), 0.25,
                                    facecolor='#885050',  # 更深的紅褐色
                                    edgecolor='#5F3535',  # 更暗的邊緣
                                    alpha=0.9,
                                    linewidth=1)
                    ax.add_patch(honeycomb)
                    
                    # 添加小的黑點在蜂窩結構中心以模擬焦油沉積
                    center_dot = Circle((x, y), 0.08,
                                     facecolor='#000000',
                                     alpha=0.9)
                    ax.add_patch(center_dot)
            
            # Add large bullae in upper lobes (characteristic of severe emphysema)
            # 在參考圖片中，除了黑色區域，還有一些較淺的區域，這些是肺氣腫的泡狀損傷
            upper_bullae = [
                (3.0, 5.5, 0.5), (7.0, 5.5, 0.5),  # Large upper bullae
                (3.5, 6.0, 0.4), (6.5, 6.0, 0.4),  # More upper bullae
                (3.2, 4.5, 0.45), (6.8, 4.5, 0.45),  # Additional bullae
                (3.8, 5.2, 0.35), (6.2, 5.2, 0.35),  # Additional bullae
            ]
            
            for x, y, size in upper_bullae:
                if (x < 5 and left_lung_path.contains_point((x, y))) or \
                   (x >= 5 and right_lung_path.contains_point((x, y))):
                    # 更深色的氣腫泡，更接近參考圖像
                    bulla = Circle((x, y), size,
                                facecolor='#C0A0A0',  # 較淺但仍暗淡的肺氣腫區域
                                edgecolor='#A08080',  # 較深的邊緣
                                alpha=0.85,
                                linewidth=0.7)
                    ax.add_patch(bulla)
                    
                    # 添加一些小的黑點以模擬焦油在肺氣腫區域的沉積
                    for _ in range(3):
                        spot_x = x + (random.random() - 0.5) * size * 1.5
                        spot_y = y + (random.random() - 0.5) * size * 1.5
                        
                        # 確保點在主要的肺輪廓內
                        if ((x < 5 and left_lung_path.contains_point((spot_x, spot_y))) or \
                           (x >= 5 and right_lung_path.contains_point((spot_x, spot_y)))):
                            small_tar = Circle((spot_x, spot_y), 0.05 + random.random() * 0.08,
                                            facecolor='#000000',
                                            alpha=0.8)
                            ax.add_patch(small_tar)

def generate_lung_svg(health_percentage):
    """
    Generate a lung visualization based on health percentage using Matplotlib.
    
    Parameters:
    health_percentage (float): Percentage of lung health (0-100)
    
    Returns:
    str: HTML img tag with the lung visualization
    """
    # Create a figure
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.axis('off')
    
    # Create the lung image
    create_lung_image(ax, health_percentage)
    
    # Convert plot to base64 image
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    
    # Return an HTML img tag with the visualization
    return f'<img src="data:image/png;base64,{img_str}" alt="Lung visualization" width="300">'
