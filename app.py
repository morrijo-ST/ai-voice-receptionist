import re
import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Voice Receptionist",layout="wide")
st.title("AI Voice Receptionist")
st.caption("Synthetic inbound-call workflow with intent routing, summaries, appointment handling, and escalation.")

SAMPLES={
"Schedule appointment":"Hi, I need to schedule a consultation for next Tuesday afternoon.",
"Billing question":"I have a question about an invoice that looks higher than I expected.",
"Urgent support":"Our system is down and we need someone to call us back immediately.",
"General inquiry":"Can you tell me what services your company offers?",
}
choice=st.sidebar.selectbox("Sample call",list(SAMPLES))
transcript=st.text_area("Caller transcript",SAMPLES[choice],height=120)

def classify(text):
    t=text.lower()
    if any(x in t for x in ["down","urgent","immediately","emergency"]): return "Urgent Support","Human escalation",95
    if any(x in t for x in ["schedule","appointment","consultation","meeting"]): return "Scheduling","Calendar workflow",92
    if any(x in t for x in ["invoice","billing","charge","payment"]): return "Billing","Finance queue",90
    return "General Inquiry","Knowledge response",78

intent,route,confidence=classify(transcript)
summary=re.sub(r"\s+"," ",transcript.strip())[:180]

c1,c2,c3=st.columns(3)
c1.metric("Detected intent",intent)
c2.metric("Confidence",f"{confidence}%")
c3.metric("Route",route)

st.subheader("Structured call output")
record={"intent":intent,"route":route,"confidence":confidence,"summary":summary,"requires_human":route in ["Human escalation","Finance queue"]}
st.json(record)

if intent=="Scheduling":
    st.subheader("Appointment workflow")
    date=st.date_input("Requested date")
    time=st.selectbox("Available slot",["9:00 AM","11:30 AM","2:00 PM","4:00 PM"])
    if st.button("Simulate booking"):
        st.success(f"Appointment reserved for {date} at {time}; CRM activity and confirmation would be created.")
elif intent=="Urgent Support":
    st.error("Escalation triggered: transfer/callback workflow and on-call notification required.")
elif intent=="Billing":
    st.warning("Billing questions route to a finance-reviewed queue; the agent does not invent account-specific answers.")
else:
    st.info("General inquiries may be answered from an approved knowledge base before human escalation.")

st.subheader("Example call log")
log=pd.DataFrame([
    ["CALL-1001","Scheduling","Booked",92],["CALL-1002","Billing","Finance Review",90],["CALL-1003","Urgent Support","Escalated",95],["CALL-1004","General Inquiry","Resolved",78]
],columns=["call_id","intent","disposition","confidence"])
st.dataframe(log,use_container_width=True,hide_index=True)
