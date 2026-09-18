from pathlib import Path
import numpy as np
from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1]/'app.py'
def app():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    assert not at.exception
    return at

def test_blank_input_does_not_classify_and_urgent_routes_to_person():
    at=app()
    at.text_area[0].set_value('').run()
    assert not at.exception
    assert len(at.metric)==0
    at.text_area[0].set_value('Our system is down, urgent help please').run()
    assert at.metric[0].value=='Urgent Support'
    assert any('does not notify' in e.value for e in at.error)
