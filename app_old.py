"""
IFRS Claim Accrual Estimator
Interactive demo for estimating insurance claim reserves under IFRS 17 principles.
"""

import gradio as gr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Synthetic loss development factors (LDFs)
LDF_PATTERNS = {
    "Auto": [3.5, 2.2, 1.5, 1.2, 1.1, 1.05, 1.02, 1.01, 1.005, 1.0],
    "Property": [2.8, 1.9, 1.4, 1.15, 1.08, 1.04, 1.02, 1.01, 1.005, 1.0],
    "Liability": [5.0, 3.5, 2.5, 1.8, 1.4, 1.2, 1.1, 1.05, 1.02, 1.01],
    "Health": [2.0, 1.5, 1.2, 1.1, 1.05, 1.02, 1.01, 1.005, 1.0, 1.0],
    "Workers Comp": [4.5, 3.0, 2.2, 1.6, 1.3, 1.15, 1.08, 1.04, 1.02, 1.01]
}

# Risk adjustment factors
RISK_ADJUSTMENT_FACTORS = {
    "Low": 0.05,
    "Medium": 0.10,
    "High": 0.20
}


def calculate_ultimate_loss(incurred_loss, claim_type, months_since_occurrence):
    """
    Calculate ultimate loss using chain ladder method.
    
    Args:
        incurred_loss: Current incurred loss amount
        claim_type: Type of insurance claim
        months_since_occurrence: Months since claim occurred
        
    Returns:
        Estimated ultimate loss
    """
    # Get development pattern
    ldfs = LDF_PATTERNS.get(claim_type, LDF_PATTERNS["Auto"])
    
    # Determine development period (in years)
    years_developed = min(months_since_occurrence // 12, len(ldfs) - 1)
    
    # Calculate cumulative development factor
    if years_developed >= len(ldfs) - 1:
        cdf = 1.0  # Fully developed
    else:
        cdf = np.prod(ldfs[years_developed:])
    
    # Calculate ultimate loss
    ultimate_loss = incurred_loss * cdf
    
    return ultimate_loss


def calculate_risk_adjustment(ultimate_loss, risk_level):
    """Calculate risk adjustment based on uncertainty level."""
    factor = RISK_ADJUSTMENT_FACTORS.get(risk_level, 0.10)
    return ultimate_loss * factor


def calculate_discount(ultimate_loss, months_to_settlement, discount_rate):
    """Calculate present value discount."""
    years_to_settlement = months_to_settlement / 12
    discount_factor = (1 + discount_rate) ** (-years_to_settlement)
    present_value = ultimate_loss * discount_factor
    discount_amount = ultimate_loss - present_value
    return present_value, discount_amount


def estimate_claim_accrual(
    claim_id,
    claim_type,
    incurred_loss,
    paid_loss,
    occurrence_date,
    expected_settlement_date,
    risk_level,
    discount_rate
):
    """
    Estimate IFRS 17 claim accrual components.
    
    Returns:
        Tuple of (summary_text, details_dataframe)
    """
    # Calculate months since occurrence
    occurrence = datetime.strptime(occurrence_date, "%Y-%m-%d")
    settlement = datetime.strptime(expected_settlement_date, "%Y-%m-%d")
    today = datetime.now()
    
    months_since_occurrence = max(0, (today.year - occurrence.year) * 12 + (today.month - occurrence.month))
    months_to_settlement = max(0, (settlement.year - today.year) * 12 + (settlement.month - today.month))
    
    # Step 1: Calculate ultimate loss
    ultimate_loss = calculate_ultimate_loss(incurred_loss, claim_type, months_since_occurrence)
    
    # Step 2: Calculate outstanding claims (IBNR + case reserves)
    outstanding_claims = ultimate_loss - paid_loss
    
    # Step 3: Calculate risk adjustment
    risk_adjustment = calculate_risk_adjustment(ultimate_loss, risk_level)
    
    # Step 4: Calculate present value and discount
    pv_ultimate, discount_amount = calculate_discount(ultimate_loss, months_to_settlement, discount_rate)
    pv_outstanding, _ = calculate_discount(outstanding_claims, months_to_settlement, discount_rate)
    
    # Step 5: Calculate total accrual
    total_accrual = pv_outstanding + risk_adjustment
    
    # Build summary
    summary = f"""
## IFRS 17 Claim Accrual Estimate

**Claim ID:** {claim_id}  
**Claim Type:** {claim_type}  
**Development Period:** {months_since_occurrence} months  
**Time to Settlement:** {months_to_settlement} months  

---

### Key Estimates

| Component | Amount |
|-----------|--------|
| **Incurred Loss (Reported)** | ${incurred_loss:,.2f} |
| **Paid Loss** | ${paid_loss:,.2f} |
| **Ultimate Loss Estimate** | ${ultimate_loss:,.2f} |
| **Outstanding Claims** | ${outstanding_claims:,.2f} |
| **Risk Adjustment ({risk_level})** | ${risk_adjustment:,.2f} |
| **Discount (@ {discount_rate*100:.1f}%)** | $({discount_amount:,.2f}) |
| **Present Value - Ultimate** | ${pv_ultimate:,.2f} |
| **Present Value - Outstanding** | ${pv_outstanding:,.2f} |
| **Total Accrual Required** | **${total_accrual:,.2f}** |

---

### Calculation Notes

1. **Ultimate Loss**: Estimated using chain ladder method with {claim_type} development pattern
2. **Outstanding Claims**: Ultimate loss minus paid losses
3. **Risk Adjustment**: {RISK_ADJUSTMENT_FACTORS[risk_level]*100:.0f}% of ultimate loss for {risk_level.lower()} uncertainty
4. **Discounting**: Applied at {discount_rate*100:.1f}% annual rate over {months_to_settlement} months
5. **Total Accrual**: PV of outstanding claims plus risk adjustment

---

⚠️ **DISCLAIMER**: This is a simplified demonstration using synthetic data and illustrative assumptions. 
Not suitable for actual financial reporting or regulatory compliance.
"""
    
    # Build details dataframe
    details_data = {
        "Component": [
            "Incurred Loss",
            "Paid Loss",
            "Ultimate Loss Estimate",
            "Outstanding Claims",
            f"Risk Adjustment ({risk_level})",
            f"Discount @ {discount_rate*100:.1f}%",
            "PV - Ultimate Loss",
            "PV - Outstanding Claims",
            "TOTAL ACCRUAL"
        ],
        "Amount": [
            f"${incurred_loss:,.2f}",
            f"${paid_loss:,.2f}",
            f"${ultimate_loss:,.2f}",
            f"${outstanding_claims:,.2f}",
            f"${risk_adjustment:,.2f}",
            f"$({discount_amount:,.2f})",
            f"${pv_ultimate:,.2f}",
            f"${pv_outstanding:,.2f}",
            f"${total_accrual:,.2f}"
        ]
    }
    
    details_df = pd.DataFrame(details_data)
    
    return summary, details_df


# Create Gradio interface
with gr.Blocks(title="IFRS Claim Accrual Estimator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📊 IFRS 17 Claim Accrual Estimator
    
    Interactive tool for estimating insurance claim reserves under IFRS 17 principles.
    
    **Features:**
    - Ultimate loss estimation using chain ladder method
    - Risk adjustment calculation
    - Present value discounting
    - Complete accrual breakdown
    
    ⚠️ **For demonstration purposes only** - uses synthetic data and simplified assumptions.
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Claim Information")
            claim_id = gr.Textbox(label="Claim ID", value="CLM-2026-001")
            claim_type = gr.Dropdown(
                label="Claim Type",
                choices=list(LDF_PATTERNS.keys()),
                value="Auto"
            )
            incurred_loss = gr.Number(label="Incurred Loss ($)", value=50000)
            paid_loss = gr.Number(label="Paid Loss ($)", value=15000)
            
        with gr.Column():
            gr.Markdown("### Timing & Risk")
            occurrence_date = gr.Textbox(label="Occurrence Date (YYYY-MM-DD)", value="2025-06-15")
            settlement_date = gr.Textbox(label="Expected Settlement Date (YYYY-MM-DD)", value="2027-12-31")
            risk_level = gr.Dropdown(
                label="Risk/Uncertainty Level",
                choices=["Low", "Medium", "High"],
                value="Medium"
            )
            discount_rate = gr.Slider(
                label="Discount Rate (%)",
                minimum=0,
                maximum=10,
                value=3.5,
                step=0.1
            )
    
    calculate_btn = gr.Button("Calculate Accrual", variant="primary")
    
    gr.Markdown("---")
    
    with gr.Row():
        summary_output = gr.Markdown(label="Accrual Summary")
    
    with gr.Row():
        details_output = gr.Dataframe(label="Detailed Breakdown", interactive=False)
    
    # Connect button to function
    calculate_btn.click(
        fn=lambda cid, ct, il, pl, od, sd, rl, dr: estimate_claim_accrual(
            cid, ct, il, pl, od, sd, rl, dr/100
        ),
        inputs=[
            claim_id, claim_type, incurred_loss, paid_loss,
            occurrence_date, settlement_date, risk_level, discount_rate
        ],
        outputs=[summary_output, details_output]
    )
    
    gr.Markdown("""
    ---
    
    ### About IFRS 17
    
    IFRS 17 is the international accounting standard for insurance contracts. Key components include:
    
    - **Fulfillment Cash Flows**: Present value of future cash flows
    - **Risk Adjustment**: Compensation for uncertainty about amount and timing
    - **Contractual Service Margin**: Unearned profit
    
    This tool focuses on the liability for incurred claims (LIC) component.
    
    ### Methodology
    
    - **Chain Ladder**: Industry-standard actuarial method for loss development
    - **Risk Adjustment**: Percentage of ultimate loss based on uncertainty
    - **Discounting**: Time value of money adjustment
    
    ---
    
    **Built by Qoder for Vercept** | All data synthetic | Advisory only
    """)

if __name__ == "__main__":
    demo.launch()
