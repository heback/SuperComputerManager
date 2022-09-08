import re
import sqlite3
from datetime import datetime

import numpy as np
import streamlit as st

# DB 연결 ################################
con = sqlite3.Connection('db.db')
cur = con.cursor()
#########################################


# DB 함수 ################################
def get_node_names():
    cur.execute(f"SELECT name FROM nodes WHERE state = 1")
    res = cur.fetchall()
    return np.asarray(res)[:, 0]


def get_node_no(name):
    cur.execute(f"SELECT no FROM nodes WHERE name='{name}'")
    res = cur.fetchone()
    return res[0]


def get_node_state(no):
    cur.execute(f"SELECT state FROM nodes WHERE no={no}")
    res = cur.fetchone()
    return res[0]
#########################################

st.header('슈퍼컴퓨터 사용 신청')
st.info('원격 데스크톱/SSH: (IP)210.110.244.120 (PORT)45002/6024')

tab1, tab2, tab3 = st.tabs(['사용 신청', '사용 이력', '통계'])
with tab1:
    st.subheader('사용 신청')
    node_names = get_node_names();
    with st.form('request_node'):
        node_name = st.selectbox('사용 가능한 노드 선택', options=node_names)
        name = st.text_input('학번+성명')
        message = st.text_area('신청 사유')
        start_time = st.date_input('시작 일')
        end_time = st.date_input('종료 일')
        submit = st.form_submit_button('제출')

        if submit:
            no = get_node_no(node_name)
            state = get_node_state(no)
            # print(state)
            # 신청 가능 여부(신청 중에 다른 학생이 신청한 경우)
            if state == 0:
                st.warning('이미 신청 중인 노드입니다.')
                st.stop()
            # 학번+성명 확인
            if len(name) > 5:
                pattern = re.compile('[0-9]{4}[가-힣]{2,4}')
                if not pattern.match(name):
                    st.warning('학번+성명을 정확하게 입력하세요. ')
                    st.stop()
            else:
                st.warning('학번+성명(예: 1001홍길동)을 정확하게 입력하세요. ')
                st.stop()
            # 신청 사유 확인
            if len(message) < 5:
                st.warning('신청 사유는 적어도 5글자 이상 입력하세요. ')
                st.stop()
            # 사용 기간 계산
            # print(start_time)
            date_diff = end_time - start_time
            if date_diff.days > 7:
                st.warning('사용 기간은 7일까지 가능합니다. ')
                st.stop()

            cur.execute(f"INSERT INTO uses VALUES ("
                        f"{no}, '{name}', '{message}'"                        
                        f")")

with tab2:
    st.subheader('사용 이력')


with tab3:
    st.subheader('통계')
