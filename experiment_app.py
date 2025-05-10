import streamlit as st

# ----- 预设的11轮资产收益率 -----
predefined_returns = [
    [0.002761, -0.0012, 0.0036],
    [-0.00566, 0.0177, -0.0028],
    [-0.0008616, -0.0050, 0.0284],
    [-0.00392, -0.0017, 0.0329],
    [-0.0002, 0.0033, -0.0057],
    [0.005067, -0.0017, -0.185],
    [0.001168, -0.0099, -0.0001],
    [-0.001746, 0.0226, -0.0076],
    [0.008637, -0.0019, -0.0058],
    [-0.00579, 0.0052, 0.0212],
    [0.003378, -0.0032, 0.0077]
]

def get_diff_level(diff):
    if diff > 0.5:
        return 1
    elif 0 < diff <= 0.5:
        return 2
    elif -0.5 <= diff <= 0:
        return 3
    else:
        return 4

st.set_page_config(page_title="过度自信实验", layout="centered")
st.title("📊 过度自信实验")

# 状态持久化
if "round" not in st.session_state:
    st.session_state.round = 0
    st.session_state.results = []

if st.session_state.round < 11:
    st.subheader(f"第 {st.session_state.round + 1} 轮")

    with st.form(key="investment_form"):
        col1, col2, col3 = st.columns(3)
        a = col1.number_input("资产 A", min_value=0, max_value=10, step=1, key="a_input")
        b = col2.number_input("资产 B", min_value=0, max_value=10, step=1, key="b_input")
        c = col3.number_input("资产 C", min_value=0, max_value=10, step=1, key="c_input")

        prediction = st.radio(
            "你预测的收益率差额属于哪个档位？",
            ["1: 高于50%", "2: 高于0-50%", "3: 低于0-50%", "4: 低于50%以上"],
            index=None
        )

        submitted = st.form_submit_button("提交本轮")

        if submitted:
            if a + b + c != 10:
                st.error("总投资单位数必须为 10。")
            elif prediction is None:
                st.error("请选择一个预测档位。")
            else:
                actual_returns = predefined_returns[st.session_state.round]
                weighted_return = (a * actual_returns[0] + b * actual_returns[1] + c * actual_returns[2]) / 10
                avg_return = sum(actual_returns) / 3
                diff = weighted_return - avg_return
                actual_level = get_diff_level(diff)
                predicted_level = int(prediction[0])
                deviation = abs(predicted_level - actual_level)

                st.session_state.results.append(deviation)
                st.success(f"✅ 第 {st.session_state.round + 1} 轮偏离档数：{deviation}")
                st.session_state.round += 1

else:
    st.success("🎉 实验结束！以下是你每轮的偏离档数：")
    for i, dev in enumerate(st.session_state.results, 1):
        st.write(f"第 {i} 轮：偏离档数 = {dev}")
    st.write("感谢参与实验！")

