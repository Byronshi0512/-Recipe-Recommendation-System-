import streamlit as st
import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Spoonacular API key
API_KEY = os.getenv('SPOONACULAR_API_KEY')

# Page configuration
st.set_page_config(
    page_title="Smart Recipe Finder",
    page_icon="🍳",
    layout="wide"
)

# Loading animation
with st.spinner("🚀 Starting up the app... Please wait a moment..."):
    time.sleep(2)
st.snow()

# Welcome message
st.info("""
💡 **Welcome!** If this is your first visit in a while, the app may take a few moments to start up. 
Please be patient while we prepare your recipe finder!
""")

# Page header with custom styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5em;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 1em;
    }
    .sub-header {
        font-size: 1.5em;
        color: #666666;
        text-align: center;
        margin-bottom: 2em;
    }
    .recipe-card {
        background-color: #FFFFFF;
        padding: 1.5em;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 1em;
    }
    .youtube-link {
        display: inline-block;
        background-color: #FF0000;
        color: white !important;
        padding: 0.5em 1em;
        text-decoration: none;
        border-radius: 5px;
        margin-top: 1em;
        text-align: center;
        width: 100%;
        transition: background-color 0.3s ease;
    }
    .youtube-link:hover {
        background-color: #CC0000;
    }
    .health-badge {
        display: inline-block;
        padding: 0.2em 0.6em;
        margin: 0.2em;
        border-radius: 15px;
        font-size: 0.9em;
        color: white;
    }
    .vegetarian {
        background-color: #4CAF50;
    }
    .vegan {
        background-color: #8BC34A;
    }
    .gluten-free {
        background-color: #FF9800;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🍳 Smart Recipe Finder</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Find delicious recipes based on ingredients you have!</p>', unsafe_allow_html=True)

# Create two columns for input
col1, col2 = st.columns([2, 1])

with col1:
    # User input for ingredients
    ingredients = st.text_input(
        "Enter your ingredients (separate with commas)", 
        placeholder="e.g., chicken, tomato, onion"
    )

with col2:
    # Add cuisine filter
    cuisines = [
        "All", "American", "Italian", "Asian", "Mexican", "Mediterranean", 
        "French", "Indian", "Chinese", "Japanese", "Thai"
    ]
    selected_cuisine = st.selectbox("Select cuisine type (optional)", cuisines)

# Search button with loading state
if st.button("🔍 Find Recipes", type="primary"):
    if ingredients:
        with st.spinner("🍳 Searching for delicious recipes..."):
            # Call API
            url = "https://api.spoonacular.com/recipes/complexSearch"
            
            params = {
                "apiKey": API_KEY,
                "includeIngredients": ingredients,
                "addRecipeInformation": True,
                "instructionsRequired": True,
                "fillIngredients": True,
                "number": 6,
                "sort": "max-used-ingredients",
            }
            
            # Add cuisine filter if not "All"
            if selected_cuisine != "All":
                params["cuisine"] = selected_cuisine
            
            try:
                response = requests.get(url, params=params)
                recipes = response.json()['results']
                
                if recipes:
                    st.success(f"🎉 Found {len(recipes)} recipes for you!")
                    
                    # Create three columns
                    cols = st.columns(3)
                    
                    for idx, recipe in enumerate(recipes):
                        with cols[idx % 3]:
                            # Create a card-like container
                            with st.container():
                                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                                
                                # Recipe image
                                st.image(recipe['image'], use_container_width=True)
                                st.markdown(f"### {recipe['title']}")
                                
                                # Recipe quick info with icons
                                st.markdown(f"⏱️ Ready in: {recipe['readyInMinutes']} minutes")
                                st.markdown(f"👥 Servings: {recipe['servings']}")
                                
                                # Health info with colored badges
                                health_info = []
                                if recipe.get('vegetarian'):
                                    health_info.append('<span class="health-badge vegetarian">🥬 Vegetarian</span>')
                                if recipe.get('vegan'):
                                    health_info.append('<span class="health-badge vegan">🌱 Vegan</span>')
                                if recipe.get('glutenFree'):
                                    health_info.append('<span class="health-badge gluten-free">🌾 Gluten Free</span>')
                                if health_info:
                                    st.markdown(" ".join(health_info), unsafe_allow_html=True)
                                
                                # YouTube Tutorial Link
                                search_query = recipe['title'].replace(" ", "+") + "+recipe+tutorial"
                                st.markdown(f'<a href="https://www.youtube.com/results?search_query={search_query}" target="_blank" class="youtube-link">▶️ Watch Tutorial on YouTube</a>', unsafe_allow_html=True)
                                
                                # Recipe details in expander
                                with st.expander("📋 View Ingredients and Instructions"):
                                    # Get detailed recipe information
                                    recipe_id = recipe['id']
                                    detail_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
                                    detail_params = {
                                        "apiKey": API_KEY
                                    }
                                    
                                    try:
                                        detail_response = requests.get(detail_url, params=detail_params)
                                        recipe_details = detail_response.json()
                                        
                                        # Ingredients
                                        st.markdown("#### 📝 Ingredients:")
                                        for ingredient in recipe_details.get('extendedIngredients', []):
                                            st.markdown(f"- {ingredient.get('original', '')}")
                                        
                                        # Instructions
                                        st.markdown("#### 👩‍🍳 Instructions:")
                                        if recipe_details.get('instructions'):
                                            st.markdown(recipe_details['instructions'])
                                        else:
                                            st.markdown("_Please check the YouTube tutorial for detailed instructions._")
                                            
                                    except Exception as e:
                                        st.markdown("_Please check the YouTube tutorial for ingredients and instructions._")
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("😕 No recipes found with these ingredients. Try different combinations!")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter at least one ingredient")

# Sidebar with tips
with st.sidebar:
    st.markdown("### 💡 Tips for Better Results")
    st.markdown("""
    1. **Ingredient Tips:**
       - Use common ingredient names
       - Separate ingredients with commas
       - Be specific (e.g., 'chicken breast' instead of just 'chicken')
    
    2. **Search Tips:**
       - Start with 2-3 main ingredients
       - Try different cuisine types
       - Include both proteins and vegetables
    
    3. **Tutorial Tips:**
       - Click on YouTube link for video instructions
       - Watch full tutorials for best results
       - Save your favorite videos for future reference
    """)
    
    st.markdown("### 🎯 Features")
    st.markdown("""
    - Find recipes by ingredients
    - Filter by cuisine type
    - View cooking time and servings
    - Watch video tutorials on YouTube
    - See detailed ingredients list
    - Check dietary information
    """)

# Footer
st.markdown("---")
st.markdown("### About")
st.markdown("""
This recipe finder helps you discover delicious meals based on ingredients you already have. 
Each recipe comes with a direct link to video tutorials on YouTube to help you master the dish.
""")
