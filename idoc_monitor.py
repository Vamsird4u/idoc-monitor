import streamlit as st
from pyrfc import Connection
from datetime import datetime

# SAP Connection Settings (you can also use st.secrets for security)
conn_params = {
    'user': 'SAP_USER',
    'passwd': 'SAP_PASSWORD',
    'ashost': 'SAP_HOST',
    'sysnr': '00',
    'client': '100',
    'lang': 'EN'
}

st.set_page_config(page_title="SAP IDoc Monitor", layout="centered")
st.title("📦 SAP IDoc Failure Monitor")
st.caption("Real-time alerting and visibility into failed IDocs")

# Threshold
THRESHOLD = 5

# Connect to SAP
try:
    conn = Connection(**conn_params)
    result = conn.call('Z_GET_FAILED_IDOCS')
    failed_count = result['E_COUNT']
    failed_idocs = result.get('E_DETAILS', [])

    st.metric(label="🚨 Failed IDocs", value=failed_count)

    if failed_count > THRESHOLD:
        st.error(f"⚠️ Alert: {failed_count} failed IDocs! Check ASAP.")
    else:
        st.success("✅ All good. Failed IDocs below threshold.")

    with st.expander("Show Failed IDoc Details"):
        for idoc in failed_idocs[:10]:  # Limit to 10 for now
            st.write(f"IDoc Number: {idoc['DOCNUM']} | Status: {idoc['STATUS']} | Created: {idoc['CREDAT']}")

    st.caption(f"Last Checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
except Exception as e:
    st.error("Could not connect to SAP system.")
    st.exception(e)
