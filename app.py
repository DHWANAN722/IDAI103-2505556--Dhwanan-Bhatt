import streamlit as st
import google.generativeai as genai

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="CoachBot AI",
    page_icon="🏃",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.markdown('<div class="main-header">🏃 CoachBot AI - Your Virtual Sports Coach</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # API Key input
    api_key = st.text_input(
        "Enter Gemini API Key",
        type="password",
        help="Get from: https://aistudio.google.com/app/apikey"
    )
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("✅ API Key Valid!")
        except:
            st.error("❌ Invalid API Key")
    
    st.divider()
    temperature = st.slider("Creativity", 0.3, 0.9, 0.7, 0.1)
    
    st.divider()
    st.info("**10+ AI Features:**\n- Workout Plans\n- Recovery\n- Nutrition\n- Mental Coaching")

# Main tabs
tab1, tab2 = st.tabs(["🎯 Features", "📜 History"])

with tab1:
    st.markdown("## 👤 Your Profile")
    
    # Profile inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        sport = st.selectbox("Sport", ["Football", "Cricket", "Basketball", "Tennis", "Athletics"])
    with col2:
        position = st.text_input("Position", "Midfielder")
    with col3:
        age = st.number_input("Age", 10, 25, 15)
    
    col4, col5 = st.columns(2)
    with col4:
        injury = st.text_input("Injury History", "None")
    with col5:
        goal = st.text_input("Goal", "Build stamina")
    
    st.divider()
    st.markdown("## 🌟 Choose Feature")
    
    # Features in columns
    features = {
        "💪 Workout Plan": "workout",
        "❤️ Recovery": "recovery",
        "🎯 Tactical": "tactical",
        "🍎 Nutrition": "nutrition",
        "⚡ Warmup": "warmup",
        "🧠 Mental": "mental",
        "📈 Stamina": "stamina",
        "💧 Hydration": "hydration",
        "🤸 Mobility": "mobility",
        "🏆 Match Day": "matchday"
    }
    
    # 2 rows x 5 columns
    for i in range(0, 10, 5):
        cols = st.columns(5)
        items = list(features.items())[i:i+5]
        for j, (name, fid) in enumerate(items):
            with cols[j]:
                if st.button(name, key=fid):
                    st.session_state.selected = fid
    
    # Generate response
    if 'selected' in st.session_state and api_key:
        fid = st.session_state.selected
        
        # Prompts
        prompts = {
            "workout": f"Create detailed workout plan for {age}yr old {position} in {sport}. Include warmup, exercises with sets/reps, cooldown. Consider: {injury}",
            
            "recovery": f"Design safe recovery plan for {age}yr athlete with {injury}. Include phases, exercises, timeline, safety tips for {sport}",
            
            "tactical": f"Give tactical coaching for {position} in {sport}. Include skills, drills, game awareness. Goal: {goal}",
            
            "nutrition": f"Create 7-day nutrition plan for {age}yr {sport} athlete. Include meals, timing, portions. Goal: {goal}",
            
            "warmup": f"Design warmup and cooldown for {position} in {sport}. Include stretches, movements, duration. Consider: {injury}",
            
            "mental": f"Develop mental training for {age}yr {sport} athlete. Include visualization, breathing, confidence building for competition",
            
            "stamina": f"Create stamina program for {sport}. Include cardio, intervals, progression. Age: {age}, Goal: {goal}",
            
            "hydration": f"Provide hydration strategy for {sport} athlete. Include timing, amounts, electrolytes for training and match days",
            
            "mobility": f"Design mobility program for {position}. Include stretches, exercises, progression. Consider: {injury}",
            
            "matchday": f"Create complete match-day routine for {age}yr {position} in {sport}. Include meals, warmup, mental prep, timing"
        }
        
        prompt = prompts[fid]
        
        with st.spinner("🤖 Generating..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-pro')
                response = model.generate_content(
                    prompt,
                    generation_config={
                        'temperature': temperature,
                        'max_output_tokens': 1500
                    }
                )
                
                result = response.text
                
                # Show result
                st.success("✅ Ready!")
                st.markdown(result)
                
                # Save history
                st.session_state.history.append({
                    'feature': fid,
                    'sport': sport,
                    'result': result
                })
                
                # Download
                st.download_button(
                    "📥 Download",
                    result,
                    f"coachbot_{fid}.txt"
                )
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Check API key and try again")
    
    elif 'selected' in st.session_state and not api_key:
        st.warning("⚠️ Enter API key in sidebar!")

with tab2:
    st.markdown("## 📜 History")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history):
            with st.expander(f"Session {i+1}: {item['feature']} - {item['sport']}"):
                st.markdown(item['result'])
    else:
        st.info("No sessions yet!")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><b>CoachBot AI</b> - Powered by Gemini 1.5 Pro 🏆</p>
    <p style='font-size: 0.8rem;'>⚠️ Consult professionals for serious training/injuries</p>
</div>
""", unsafe_allow_html=True)
