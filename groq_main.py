import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq

load_dotenv()
MODEL_ID = "llama-3.3-70b-versatile"
groq_model = Groq(id=MODEL_ID, api_key=os.getenv("GROQ_API_KEY"))

#creating function 
def cd(name, stance):
    return Agent(
        name=name,
        model=groq_model,
        instructions=[
            f"Start exactly with: 'I am {stance} the motion.'",
            "Keep responses under 150 words.",
            "Focus on logical consistency and sharp rebuttals."
        ]
    )

# defining agents
pro_agent = cd("PRO", "for")
con_agent = cd("CON", "against")
judge_agent = Agent(
    name="JUDGE", 
    model=groq_model, 
    instructions=["Evaluate logic and bias fairly. Output scorecard and winner. Keep it brief."]
)

def rd():
    topic = input("Enter Debate Topic: ")
    print(f"\n--- DEBATE: {topic} ---\n")

    # Round 1
    results = {}
    for agent in [pro_agent, con_agent]:
        print(f" {agent.name} is preparing...")
        results[agent.name] = agent.run(topic).content
        print(f"[{agent.name} OPENING]:\n{results[agent.name]}\n")

    # Round 2
    print(" STARTING REBUTTAL ROUND ")
    pro_reb = pro_agent.run(f"REBUT THIS: {results['CON']}").content
    con_reb = con_agent.run(f"REBUT THIS: {results['PRO']}").content

    print(f"[PRO REBUTTAL]: {pro_reb}\n\n[CON REBUTTAL]: {con_reb}\n")

    # Evaluation
    print("JUDGE is evaluating the scores: ")
    his = f"Topic: {topic}\nPRO Open: {results['PRO']}\nCON Open: {results['CON']}\nPRO Rebut: {pro_reb}\nCON Rebut: {con_reb}"
    print(f"\n{judge_agent.run(his).content}")

if __name__ == "__main__":
    rd()