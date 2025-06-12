import streamlit as st

st.title("Livestream Cost Calculator")

# Input: Total cost (always required)
total_cost = st.number_input("Total Cost ($)", min_value=0.0, step=1.0, format="%.2f")

# Dropdown to select variable to calculate (default is Cost Per Viewer)
to_calculate = st.selectbox(
    "Which variable would you like to calculate?",
    [
        "Cost Per Viewer",
        "Client Pays",
        "Number of Viewers"
    ],
    index=0
)

# Helper for input fields
def input_field(label, key, disabled, default_value=0.0, is_int=False):
    if is_int:
        return st.number_input(label, key=key, value=int(default_value), step=1, disabled=disabled)
    else:
        return st.number_input(label, key=key, value=float(default_value), step=1.0, format="%.2f", disabled=disabled)

# Determine which fields to disable
disable_client_pays = (to_calculate == "Client Pays")
disable_viewers = (to_calculate == "Number of Viewers")
disable_cost_per_viewer = (to_calculate == "Cost Per Viewer")

# Inputs (with defaults)
client_pays_input = input_field("Client Pays ($)", "client_pays", disabled=disable_client_pays)
# Display Short Fall right below Client Pays input
if to_calculate == "Client Pays" and client_pays_input is not None:
    if to_calculate == "Client Pays":
        # Calculate short fall for display if calculating client pays
        short_fall_val = total_cost - (cost_per_viewer_input * viewers_input) if 'cost_per_viewer_input' in locals() and 'viewers_input' in locals() else 0
    else:
        short_fall_val = total_cost - client_pays_input
    st.markdown(f"<h5 style='margin-top: 0;'>Short Fall: ${short_fall_val:,.2f}</h5>", unsafe_allow_html=True)
else:
    # Also display short fall for all other cases below client pays input
    short_fall_val = total_cost - client_pays_input
    st.markdown(f"<h5 style='margin-top: 0;'>Short Fall: ${short_fall_val:,.2f}</h5>", unsafe_allow_html=True)

cost_per_viewer_input = input_field("Cost per Viewer ($)", "cost_per_viewer", disabled=disable_cost_per_viewer)
viewers_input = input_field("Number of Viewers", "viewers", disabled=disable_viewers, default_value=100, is_int=True)

# Calculate result
result = None
error = None

try:
    if to_calculate == "Cost Per Viewer":
        if viewers_input == 0:
            error = "Number of viewers cannot be zero."
        else:
            company_covers = total_cost - client_pays_input
            result = company_covers / viewers_input

    elif to_calculate == "Number of Viewers":
        if cost_per_viewer_input == 0:
            error = "Cost per viewer cannot be zero."
        else:
            company_covers = total_cost - client_pays_input
            result = company_covers / cost_per_viewer_input

    elif to_calculate == "Client Pays":
        # Client pays = Total cost - (Cost per viewer * Number of viewers)
        result = total_cost - (cost_per_viewer_input * viewers_input)
        if result < 0:
            error = "Client pays calculated as negative — please check inputs."

except Exception as e:
    error = f"Error: {str(e)}"

# Show result
st.markdown("---")
if error:
    st.error(error)
elif result is not None:
    if to_calculate == "Number of Viewers":
        st.success(f"**{to_calculate}:** {int(result):,}")
    else:
        st.success(f"**{to_calculate}:** ${result:,.2f}")
