import streamlit as st

st.header('슈퍼 컴퓨터 사용 신청')
st.info('원격 데스크톱/SSH: (IP)210.110.244.120 (PORT)45002/6024')

tab1, tab2, tab3 = st.tabs(['사용신청', '사용이력', '통계'])
with tab1:
    st.subheader('사용신청')

with tab2:
    st.subheader('사용이력')

with tab3:
    st.subheader('통계')