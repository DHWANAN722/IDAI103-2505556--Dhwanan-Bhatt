import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="CoachBot AI - Your Virtual Sports Coach",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.markdown('<div class="main-header">🏃 CoachBot AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Personal AI Sports Coach - Empowering Young Athletes</div>', unsafe_allow_html=True)

# Sidebar for API key and settings
with st.sidebar:
    st.image("https://api.dicebear.com/7.x/bottts/svg?seed=coachbot", width=150)
    st.title("⚙️ Settings")
    
    api_key = st.text_input(
        "Enter Gemini API Key",
        type="password",
        value=st.session_state.api_key,
        help="Get your API key from https://aistudio.google.com/app/apikey"
    )
    
    if api_key:
        st.session_state.api_key = api_key
        try:
            genai.configure(api_key=api_key)
            st.success("✅ API Key configured!")
        except Exception as e:
            st.error(f"❌ Invalid API Key: {str(e)}")
    
    st.divider()
    
    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.7, 0.1,
                           help="Higher = more creative responses")
    
    st.divider()
    st.markdown("### 📊 About")
    st.info("""
    **CoachBot AI** provides:
    - 10+ AI-powered features
    - Personalized training plans
    - Injury recovery guidance
    - Nutrition & mental coaching
    """)

# Main content area
tab1, tab2, tab3 = st.tabs(["🎯 Features", "📝 Custom Query", "📜 History"])

with tab1:
    st.markdown("## 🌟 Choose Your Coaching Feature")
    
    # User profile inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sport = st.selectbox(
            "Sport",
            ["Football/Soccer", "Cricket", "Basketball", "Tennis", "Athletics", 
             "Swimming", "Badminton", "Volleyball", "Hockey"]
        )
    
    with col2:
        position = st.text_input("Position/Role", placeholder="e.g., Striker, Bowler, Point Guard")
    
    with col3:
        age = st.number_input("Age", min_value=10, max_value=25, value=15)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        injury_history = st.text_input("Injury History (if any)", placeholder="e.g., Ankle sprain, None")
    
    with col5:
        diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan", "No Preference"])
    
    with col6:
        goal = st.text_input("Training Goal", placeholder="e.g., Build stamina, Improve speed")
    
    st.divider()
    
    # Feature buttons in grid
    features = [
        ("💪 Position-Based Workout", "workout"),
        ("❤️ Injury Recovery Plan", "recovery"),
        ("🎯 Tactical Coaching", "tactical"),
        ("🍎 Nutrition Guide", "nutrition"),
        ("⚡ Warm-up Routine", "warmup"),
        ("🧠 Mental Focus Training", "mental"),
        ("📈 Stamina Building", "stamina"),
        ("💧 Hydration Strategy", "hydration"),
        ("🤸 Mobility Training", "mobility"),
        ("🏆 Match-Day Preparation", "matchday")
    ]
    
    # Create 2 rows of 5 columns each
    for i in range(0, 10, 5):
        cols = st.columns(5)
        for j, (feature_name, feature_id) in enumerate(features[i:i+5]):
            with cols[j]:
                if st.button(feature_name, key=feature_id):
                    if not st.session_state.api_key:
                        st.error("⚠️ Please enter your Gemini API key in the sidebar first!")
                    else:
                        st.session_state.selected_feature = feature_id
                        st.session_state.feature_name = feature_name
    
    # Generate response when feature is selected
    if 'selected_feature' in st.session_state:
        feature_id = st.session_state.selected_feature
        feature_name = st.session_state.feature_name
        
        st.markdown(f"### {feature_name}")
        
        # Create detailed prompts for each feature
        prompts = {
            "workout": f"""Create a comprehensive position-based workout plan for a {age}-year-old {position} in {sport}. 
            Include warm-up, main workout with specific exercises, sets, reps, and cool-down. 
            Consider their injury history: {injury_history}. Make it safe and age-appropriate.""",
            
            "recovery": f"""Design a safe recovery training plan for a {age}-year-old athlete recovering from {injury_history or 'general fatigue'}. 
            Include phases of recovery, specific low-impact exercises, timeline, and safety precautions. 
            Focus on gradual return to {sport} activities.""",
            
            "tactical": f"""Provide tactical coaching advice for a {position} in {sport}. 
            Include position-specific skills, decision-making tips, game awareness drills, and weekly practice schedule. 
            Goal: {goal}. Make it practical and actionable.""",
            
            "nutrition": f"""Create a week-long nutrition guide for a {age}-year-old {sport} athlete following a {diet_type} diet. 
            Include daily meal plans, timing, portion sizes, and hydration. Consider their training goal: {goal}.""",
            
            "warmup": f"""Generate a personalized warm-up and cool-down routine for a {position} in {sport}. 
            Include dynamic stretches, sport-specific movements, duration, and injury prevention tips considering: {injury_history}.""",
            
            "mental": f"""Develop a mental focus and pre-match preparation routine for a {age}-year-old {sport} athlete. 
            Include visualization techniques, breathing exercises, confidence building, and tournament mindset strategies.""",
            
            "stamina": f"""Create a stamina and endurance building program for {sport}. 
            Include cardio workouts, interval training, progressive overload schedule, and recovery periods. 
            Current goal: {goal}. Age: {age}.""",
            
            "hydration": f"""Provide a detailed hydration and electrolyte strategy for a {sport} athlete. 
            Include pre-training, during-training, and post-training hydration schedules, recommended drinks, and signs of dehydration.""",
            
            "mobility": f"""Design a mobility and flexibility training program for a {position} recovering from {injury_history or 'general tightness'}. 
            Include specific stretches, yoga poses, foam rolling techniques, and progression timeline.""",
            
            "matchday": f"""Create a complete match-day preparation routine for a {age}-year-old {position} in {sport}. 
            Include pre-match meal (considering {diet_type} diet), warm-up sequence, mental preparation, and in-game tips."""
        }
        
        prompt = prompts.get(feature_id, "")
        
        with st.spinner("🤖 CoachBot is preparing your personalized plan..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-pro')
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=2048,
                    )
                )
                
                result = response.text
                
                # Display result
                st.success("✅ Your personalized coaching plan is ready!")
                st.markdown(result)
                
                # Save to history
                st.session_state.history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'feature': feature_name,
                    'sport': sport,
                    'position': position,
                    'response': result
                })
                
                # Download button
                st.download_button(
                    label="📥 Download Plan",
                    data=result,
                    file_name=f"coachbot_{feature_id}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Please check your API key and try again.")

with tab2:
    st.markdown("## 💬 Ask CoachBot Anything")
    st.write("Have a specific question? Ask your AI coach directly!")
    
    custom_query = st.text_area(
        "Your Question",
        placeholder="e.g., How can I improve my speed for a 100m sprint?",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Coaching Advice", key="custom"):
            if not st.session_state.api_key:
                st.error("⚠️ Please enter your Gemini API key in the sidebar first!")
            elif not custom_query:
                st.warning("Please enter your question first!")
            else:
                with st.spinner("🤖 Thinking..."):
                    try:
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        full_prompt = f"""You are CoachBot AI, a professional sports coach for young athletes.
                        
                        Athlete Profile:
                        - Sport: {sport}
                        - Position: {position}
                        - Age: {age}
                        - Injury History: {injury_history}
                        - Goal: {goal}
                        
                        Question: {custom_query}
                        
                        Provide detailed, safe, and age-appropriate coaching advice."""
                        
                        response = model.generate_content(
                            full_prompt,
                            generation_config=genai.types.GenerationConfig(
                                temperature=temperature,
                                max_output_tokens=2048,
                            )
                        )
                        
                        st.success("✅ Here's your answer:")
                        st.markdown(response.text)
                        
                        st.session_state.history.append({
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'feature': 'Custom Query',
                            'sport': sport,
                            'position': position,
                            'response': response.text
                        })
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

with tab3:
    st.markdown("## 📜 Your Coaching History")
    
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"🏅 {item['feature']} - {item['timestamp']}"):
                st.markdown(f"**Sport:** {item['sport']} | **Position:** {item['position']}")
                st.markdown("---")
                st.markdown(item['response'])
        
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No coaching sessions yet. Try some features to get started!")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>CoachBot AI</strong> - Empowering the Next Generation of Athletes 🏆</p>
    <p>Built with Streamlit • Powered by Gemini 1.5 Pro</p>
    <p style='font-size: 0.8rem;'>⚠️ Always consult with professional coaches and medical professionals for serious training and injury concerns.</p>
</div>
""", unsafe_allow_html=True)
