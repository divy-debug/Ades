import os, streamlit as st
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq

load_dotenv()
MODEL_70B, MODEL_8B = "llama-3.3-70b-versatile", "llama-3.1-8b-instant"
groq_model = Groq(id=MODEL_70B, api_key=os.getenv("GROQ_API_KEY"))

def cd(name, stance):
    return Agent(name=name, model=groq_model, instructions=[f"Start with: 'I am {stance} the motion.'", "Max 150 words.", "Be logical."])

def stream(agent, task, container, theme):
    colors = {"p": ("#9e7ae5", "#5e27d6"), "c": ("#6bb1e7", "#1f69e8"), "j": ("#c92d83", "#ea8bcf")}
    bg, border = colors[theme]
    res = ""
    for chunk in agent.run(task, stream=True):
        res += chunk.content
        container.markdown(f"<div style='background:{bg}; border-left:6px solid {border}; padding:15px; border-radius:8px; color:white;'><strong>{agent.name}</strong><br>{res} ▌</div>", unsafe_allow_html=True)
    return res

pro, con = cd("PRO", "for"), cd("CON", "against")
judge = Agent(name="JUDGE", model=Groq(id=MODEL_8B), instructions=["Provide Scorecard for both PRO and CON in (X/10) format on basis of logic and evidence.","Then Declare winner and give why in 1 sentence. "])

st.set_page_config(layout="wide")
st.title("Automated Debate Evaluation System")
topic = st.text_input("ENTER DEBATE TOPIC:")

if st.button("GO LIVE", type="primary") and topic:
    cols, data = st.columns(2), {}
    
    # ROUND 1
    data["p1"] = stream(pro, topic, cols[0].empty(), "p")
    data["c1"] = stream(con, topic, cols[1].empty(), "c")

    # ROUND 2
    st.divider()
    data["p2"] = stream(pro, f"REBUT: {data['c1']}", st.empty(), "p")
    data["c2"] = stream(con, f"REBUT: {data['p1']}", st.empty(), "c")

    # EVALUATION
    st.divider()
    history = f"Topic: {topic}\nPRO: {data['p1']} {data['p2']}\nCON: {data['c1']} {data['c2']}"
    stream(judge, history, st.empty(), "j")