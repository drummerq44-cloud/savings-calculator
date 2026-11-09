import streamlit as st
import pandas as pd

st.title("Retirement Savings Projector")
st.write("See how monthly contributions and compound growth build wealth over time.")

start = st.number_input("Starting balance ($)", 0.0, value=1000.0, step=500.0)
monthly = st.number_input("Monthly contribution ($)", 0.0, value=300.0, step=50.0)
rate = st.slider("Expected annual return (%)", 0.0, 15.0, 7.0, 0.5)
years = st.slider("Years invested", 1, 50, 30)
inflation = st.slider("Expected inflation (%)", 0.0, 6.0, 2.5, 0.1)

r = rate / 100 / 12
bal, contrib, rows = start, start, []
for m in range(1, years * 12 + 1):
    bal = bal * (1 + r) + monthly
    contrib += monthly
    if m % 12 == 0:
        real = bal / ((1 + inflation / 100) ** (m / 12))
        rows.append({"Year": m // 12, "Balance": round(bal, 2),
                     "Total Contributed": round(contrib, 2),
                     "Inflation-Adjusted": round(real, 2)})

df = pd.DataFrame(rows)
final = df.iloc[-1]
c1, c2, c3 = st.columns(3)
c1.metric("Ending Balance", f"${final['Balance']:,.0f}")
c2.metric("You Contributed", f"${final['Total Contributed']:,.0f}")
c3.metric("Growth Earned", f"${final['Balance'] - final['Total Contributed']:,.0f}")

st.line_chart(df.set_index("Year")[["Balance", "Total Contributed", "Inflation-Adjusted"]])
st.dataframe(df, use_container_width=True)
