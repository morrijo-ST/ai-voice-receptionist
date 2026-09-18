
import html
import pandas as pd
import streamlit as st

def shell(name, title, subtitle, style):
    global PALETTE, INK, PANEL, BG, ACCENT
    themes = {
      'terminal': ('#091411','#10221d','#e7f5ee','#3fe0a0','#7e9c8d',4),
      'purple': ('#171625','#222137','#f5f1ff','#ba9bff','#9ca1c0',12),
      'indigo': ('#f4f5fb','#ffffff','#242746','#5149b9','#64708b',18),
      'coral': ('#faf7f2','#ffffff','#302a27','#c7543e','#796d65',20),
      'blue': ('#f2f6fa','#ffffff','#183348','#126bb5','#5d7486',8),
      'cyan': ('#07141d','#102330','#def5ff','#53d2ed','#8caab9',4),
      'ops': ('#0b1720','#132733','#e7f5f4','#4edbc4','#99b5bd',10),
      'editorial': ('#f8f7f3','#ffffff','#253b38','#317764','#6b7d77',6),
      'amber': ('#17212c','#223140','#f8f4e9','#efbc67','#a6b2bf',6),
    }
    BG,PANEL,INK,ACCENT,MUTED,RADIUS=themes[style]
    PALETTE=[ACCENT,'#4c9fd6','#d99455','#ae83c6','#6cae8b']
    st.markdown(f"""<style>
    .stApp {{background:{BG};color:{INK}}}
    [data-testid="stHeader"] {{background:{BG};}}
    .block-container {{max-width:1480px;padding:2rem 2.5rem 4rem;}}
    [data-testid="stSidebar"] {{background:{PANEL};border-right:1px solid {MUTED}35;}}
    h1,h2,h3,p,label,[data-testid="stMarkdownContainer"], [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{color:{INK};}}
    h1 {{font-size:2.55rem!important;letter-spacing:-.055em;line-height:1.12!important;font-weight:650!important;}}
    h2,h3 {{letter-spacing:-.025em;}}
    [data-testid="stCaptionContainer"] {{opacity:1!important;}}
    [data-testid="stCaptionContainer"] p {{color:{MUTED}!important;}}
    [data-tag] {{background:{ACCENT}25!important;color:{INK}!important;border:1px solid {ACCENT}50;}}
    [data-tag] span,[data-tag] button {{color:{INK}!important;}}
    [data-testid="stMetric"] {{background:{PANEL};border:1px solid {MUTED}30;border-top:2px solid {ACCENT};border-radius:{RADIUS}px;padding:18px 20px;}}
    [data-testid="stMetricValue"] {{font-variant-numeric:tabular-nums;font-size:1.8rem;}}
    [data-testid="stPlotlyChart"] {{background:{PANEL};border:1px solid {MUTED}30;border-radius:{RADIUS}px;overflow:hidden;}}
    [data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"], textarea {{background:{PANEL}!important;color:{INK}!important;}}
    input,textarea {{color:{INK}!important;-webkit-text-fill-color:{INK}!important;}}
    [data-baseweb="tag"] {{background:{ACCENT}25!important;color:{INK}!important;}}
    [data-baseweb="tag"] span {{color:{INK}!important;}}
    button[kind="secondary"], [data-testid="stDownloadButton"] button {{background:{PANEL};color:{INK};border-color:{MUTED}65;}}
    [data-baseweb="tab"] {{color:{INK}!important;}}
    [data-testid="stAlert"] {{background:{PANEL};color:{INK};}}
    .eyebrow {{font:600 11px ui-monospace,monospace;letter-spacing:.15em;color:{ACCENT};margin-bottom:16px;}}
    .hero {{border-bottom:1px solid {MUTED}40;padding:12px 0 25px;margin-bottom:24px;}}
    .hero p {{max-width:850px;color:{MUTED};font-size:1rem;}}
    .brief {{border-left:3px solid {ACCENT};background:{PANEL};padding:16px 20px;margin:18px 0;color:{INK};}}
    @media(max-width:700px){{.block-container{{padding:1rem;}}h1{{font-size:1.8rem!important;}}}}
    </style>""",unsafe_allow_html=True)
    st.markdown(f'<div class="hero"><div class="eyebrow">MORRIS / {html.escape(name.upper())} · SYNTHETIC DEMO</div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',unsafe_allow_html=True)
    st.sidebar.caption('MORRIS · PORTFOLIO LAB')
    st.sidebar.caption('Fictional data. Explore the workflow; no external systems are connected.')

def brief(text):
    st.markdown('<div class="brief">'+html.escape(text)+'</div>',unsafe_allow_html=True)

def money(value):
    sign='−' if value<0 else ''
    return f'{sign}${abs(value)/1e6:,.2f}M' if abs(value)>=1e6 else f'{sign}${abs(value):,.0f}'

def metrics(items):
    for col,(label,value) in zip(st.columns(len(items)),items):col.metric(label,value)

def table(df, name='detail', height=360):
    config={}
    for col in df.columns:
        label=str(col).replace('_',' ').title()
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            if any(x in str(col) for x in ['pct','margin','confidence','attainment','probability','achievement']):
                config[col]=st.column_config.NumberColumn(label,format='%.3f')
            elif any(x in str(col) for x in ['amount','revenue','arr','acv','cost','expense','cash','earned','capitalized','amortization','balance','asset','budget','forecast','variance','value','backlog','receipts','payroll','subcontractor','materials','labor']):
                config[col]=st.column_config.NumberColumn(label,format='$%.2f')
            else:config[col]=st.column_config.NumberColumn(label)
        else:config[col]=st.column_config.Column(label)
    st.dataframe(df,use_container_width=True,hide_index=True,height=height,column_config=config)
    st.download_button('Download '+name.replace('_',' ')+' CSV',df.to_csv(index=False),name+'.csv','text/csv',key='export_'+name)

def nonempty(df):
    if df.empty:
        st.info('No records in this selection. Choose at least one filter value to continue.')
        st.stop()

import re,json
st.set_page_config(page_title='Call Routing / Morris',layout='wide')
shell('CALL CONCIERGE','A clear handoff for every caller.','Explore intent routing, review the conversation, and prepare the next action.','indigo')
SAMPLES={
"Schedule appointment":"Hi, I need to schedule a consultation for next Tuesday afternoon.",
"Billing question":"I have a question about an invoice that looks higher than I expected.",
"Urgent support":"Our system is down and we need someone to call us back immediately.",
"General inquiry":"Can you tell me what services your company offers?",
}
def classify(text):
    t=text.lower()
    if any(x in t for x in ["down","urgent","immediately","emergency"]): return "Urgent Support","Human escalation",95
    if any(x in t for x in ["schedule","appointment","consultation","meeting"]): return "Scheduling","Calendar workflow",92
    if any(x in t for x in ["invoice","billing","charge","payment"]): return "Billing","Finance queue",90
    return "General Inquiry","Knowledge response",78


choice=st.sidebar.selectbox('Sample call',list(SAMPLES))
a,b=st.columns([1.2,1])
with a:
    st.subheader('Caller transcript')
    transcript=st.text_area('Edit the transcript',SAMPLES[choice],height=180,key='transcript_'+choice)
    if not transcript.strip():
        st.info('Enter a transcript to classify the request.')
        st.stop()
    intent,route,score=classify(transcript)
    summary=re.sub(r'\s+',' ',transcript.strip())[:180]
    st.caption('Text simulation. No microphone, speech recognition, or telephony connection is active.')
    st.subheader('Call notes')
    st.write(summary)
with b:
    st.subheader('Routing decision')
    st.metric('Intent',intent)
    st.info(route)
    st.caption('Keyword routing rules; numeric confidence estimates have been removed because they were not calibrated.')
    if intent=='Scheduling':
        date=st.date_input('Requested date')
        time=st.selectbox('Illustrative slot',['9:00 AM','11:30 AM','2:00 PM','4:00 PM'])
        if st.button('Record demo appointment'):
            st.session_state['appointment']=f'{date} at {time}'
        if st.session_state.get('appointment'):st.success('Demo request saved: '+st.session_state.appointment+'. No calendar booking or confirmation was sent.')
    elif intent=='Urgent Support':st.error('Suggested action: human escalation. This demo does not notify an on-call team.')
    elif intent=='Billing':st.warning('Suggested action: finance review. Verify the account before discussing invoice details.')
    else:st.write('Suggested action: consult an approved knowledge source or transfer to a person.')
record={'intent':intent,'suggested_route':route,'transcript_excerpt':summary,'requires_human':intent in ['Urgent Support','Billing'],'simulation':True}
with st.expander('Structured handoff'):
    st.json(record)
    st.download_button('Download handoff JSON',json.dumps(record,indent=2),'demo_call_handoff.json','application/json')
brief('Try changing the sample from scheduling to billing or urgent support. The routing decision updates from the transcript; all actions remain local demonstrations.')
