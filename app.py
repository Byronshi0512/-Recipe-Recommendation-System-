import streamlit as st
import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Spoonacular API密钥
API_KEY = os.getenv('SPOONACULAR_API_KEY')

# 设置页面配置
st.set_page_config(
    page_title="智能菜谱推荐",
    page_icon="🍳",
    layout="wide"
)

# 页面标题
st.title("🍳 智能菜谱推荐系统")
st.markdown("### 根据您现有的食材推荐美味菜谱")

# 用户输入食材
ingredients = st.text_input("请输入您有的食材（用逗号分隔）", "鸡肉, 西红柿")

if st.button("查找菜谱"):
    if ingredients:
        # 调用API
        url = f"https://api.spoonacular.com/recipes/findByIngredients"
        params = {
            "apiKey": API_KEY,
            "ingredients": ingredients,
            "number": 5,
            "ranking": 2,
            "ignorePantry": True
        }
        
        try:
            response = requests.get(url, params=params)
            recipes = response.json()
            
            if recipes:
                for recipe in recipes:
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.image(recipe['image'], use_column_width=True)
                    
                    with col2:
                        st.subheader(recipe['title'])
                        st.write("已匹配的食材：")
                        for used in recipe['usedIngredients']:
                            st.write(f"✅ {used['name']}")
                        
                        st.write("还需要的食材：")
                        for missing in recipe['missedIngredients']:
                            st.write(f"❌ {missing['name']}")
                        
                        # 获取详细菜谱信息
                        recipe_id = recipe['id']
                        detail_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
                        detail_params = {
                            "apiKey": API_KEY
                        }
                        detail_response = requests.get(detail_url, params=detail_params)
                        recipe_details = detail_response.json()
                        
                        if 'sourceUrl' in recipe_details:
                            st.markdown(f"[查看完整菜谱]({recipe_details['sourceUrl']})")
                    
                    st.markdown("---")
            else:
                st.warning("没有找到相关菜谱，请尝试其他食材组合。")
                
        except Exception as e:
            st.error(f"发生错误：{str(e)}")
    else:
        st.warning("请输入至少一种食材")

# 页面底部信息
st.markdown("---")
st.markdown("### 使用说明")
st.write("1. 输入您家中现有的食材，用逗号分隔")
st.write("2. 点击"查找菜谱"按钮获取推荐")
st.write("3. 系统会显示可以使用这些食材制作的菜谱")
