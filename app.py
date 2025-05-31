import streamlit as st
import requests
import os
from dotenv import load_dotenv

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

# Page header
st.title("🍳 Smart Recipe Finder")
st.markdown("### Find delicious recipes based on ingredients you have!")

# User input for ingredients
ingredients = st.text_input(
    "Enter your ingredients (separate with commas)", 
    "chicken, tomato"
)

# Add cuisine filter
cuisines = [
    "All", "American", "Italian", "Asian", "Mexican", "Mediterranean", 
    "French", "Indian", "Chinese", "Japanese", "Thai"
]
selected_cuisine = st.selectbox("Select cuisine type (optional)", cuisines)

if st.button("Find Recipes"):
    if ingredients:
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
                st.markdown("## 🎉 Found Recipes")
                
                # Create three columns
                cols = st.columns(3)
                
                for idx, recipe in enumerate(recipes):
                    with cols[idx % 3]:
                        # Create a card-like container
                        with st.container():
                            st.image(recipe['image'], use_column_width=True)
                            st.markdown(f"### {recipe['title']}")
                            
                            # Recipe quick info
                            st.markdown(f"⏱️ Ready in: {recipe['readyInMinutes']} minutes")
                            st.markdown(f"👥 Servings: {recipe['servings']}")
                            
                            # Health info
                            if recipe.get('vegetarian'):
                                st.markdown("🥬 Vegetarian")
                            if recipe.get('vegan'):
                                st.markdown("🌱 Vegan")
                            if recipe.get('glutenFree'):
                                st.markdown("🌾 Gluten Free")
                            
                            # Get detailed recipe information
                            recipe_id = recipe['id']
                            detail_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
                            detail_params = {
                                "apiKey": API_KEY
                            }
                            
                            try:
                                detail_response = requests.get(detail_url, params=detail_params)
                                recipe_details = detail_response.json()
                                
                                # Links section
                                st.markdown("### 📚 Learn More")
                                
                                # Original source link
                                if recipe_details.get('sourceUrl'):
                                    st.markdown(f"[🔗 Original Recipe]({recipe_details['sourceUrl']})")
                                
                                # Add alternative recipe sources
                                search_query = recipe['title'].replace(" ", "+")
                                
                                st.markdown("### 🌐 Alternative Recipe Sources")
                                st.markdown(f"[▶️ YouTube Tutorials](https://www.youtube.com/results?search_query={search_query}+recipe+tutorial)")
                                st.markdown(f"[📝 AllRecipes](https://www.allrecipes.com/search?q={search_query})")
                                st.markdown(f"[🍳 Food Network](https://www.foodnetwork.com/search/{search_query}-)")
                                
                                # Display ingredients and instructions
                                with st.expander("📋 View Ingredients and Instructions"):
                                    # Ingredients
                                    st.markdown("#### Ingredients:")
                                    for ingredient in recipe_details.get('extendedIngredients', []):
                                        st.markdown(f"- {ingredient.get('original', '')}")
                                    
                                    # Instructions
                                    st.markdown("#### Instructions:")
                                    if recipe_details.get('instructions'):
                                        st.markdown(recipe_details['instructions'])
                                    else:
                                        st.markdown("_Detailed instructions available in the recipe links above._")
                                
                            except Exception as e:
                                st.warning("Couldn't load detailed recipe information. Please try the alternative sources below.")
                                # Provide alternative links even if detailed info fails
                                st.markdown("### 🌐 Find Recipe Here")
                                search_query = recipe['title'].replace(" ", "+")
                                st.markdown(f"[▶️ YouTube Tutorials](https://www.youtube.com/results?search_query={search_query}+recipe+tutorial)")
                                st.markdown(f"[📝 AllRecipes](https://www.allrecipes.com/search?q={search_query})")
                                st.markdown(f"[🍳 Food Network](https://www.foodnetwork.com/search/{search_query}-)")
                            
                            st.markdown("---")
            else:
                st.warning("No recipes found with these ingredients. Try different combinations!")
                
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
    
    3. **Recipe Sources:**
       - Multiple recipe sources are provided
       - Try YouTube tutorials for visual guidance
       - Check trusted recipe websites
    """)
    
    st.markdown("### 🎯 Features")
    st.markdown("""
    - Find recipes by ingredients
    - Filter by cuisine type
    - View cooking time and servings
    - Access multiple recipe sources
    - Watch video tutorials
    - See detailed ingredients and instructions
    """)

# Footer
st.markdown("---")
st.markdown("### About")
st.markdown("""
This recipe finder helps you discover delicious meals based on ingredients you already have. 
Each recipe comes with multiple learning resources to ensure you can find the perfect tutorial for your cooking style.
""")
