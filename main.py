from agno.agent import Agent
from agno.models.ollama import Ollama

local_brain = Ollama(id="llama3.2")

# PRO: The "For" Advocate
pro_agent = Agent(
    name="PRO",
    model=local_brain,
    instructions=[
        "CRITICAL: You MUST start your response with: 'Today, I stand for the motion.'",
        "Keep your argument logical and UNDER 150 words.",
        "Do not repeat yourself."
    ],
)

# CON: The "Against" Advocate
con_agent = Agent(
    name="CON",
    model=local_brain,
    instructions=[
        "CRITICAL: You MUST start your response with: 'Today, I stand against the motion.'",
        "Keep your argument strong with clear rebuttal and UNDER 150 words.",
        "Do not repeat yourself."
    ],
)
# JUDGE: The Evaluation System
judge_agent = Agent(
    name="JUDGE",
    model=local_brain,
    instructions=[
        "Be an unbiased referee. Evaluate logic and persuasiveness.",
        "To prevent looping: Keep each section to 1-2 sentences maximum.",
        "Format your output exactly like this and STOP after the reasoning:",
        "",
        "-- PRO SCORECARD ---",
        "Logic: [X/10] | Evidence: [X/10] | Persuasiveness: [X/10]",
        "",
        "-- CON SCORECARD ---",
        "Logic: [X/10] | Evidence: [X/10] | Persuasiveness: [X/10]",
        "",
        " --- BIAS CHECK ---",
        "[1 sentence on if you were biased]",
        "",
        " --- FINAL VERDICT ---",
        "Winner: [PRO or CON]",
        "Reasoning: [1 sentence explaining why]"
    ],
)

def start_debate():
    topic = input(" Enter Debate Topic: ")
    print(f"\n---  DEBATE START: {topic} ---\n")

    # PRO Round
    print(" PRO is generating...")
    pro_res = pro_agent.run(topic)
    print(f"[PRO ARGUMENT]\n{pro_res.content}\n")

    # CON Round
    print(" CON is ready for rebuttal...")
    con_res = con_agent.run(topic)
    print(f"[CON ARGUMENT]\n{con_res.content}\n")

    # JUDGE Round
    print("JUDGE is evaluating ...")
    verdict = judge_agent.run(f"PRO said: {pro_res.content}\n\nCON said: {con_res.content}")
    print(f"\n{verdict.content}")

if __name__ == "__main__":
    start_debate()
