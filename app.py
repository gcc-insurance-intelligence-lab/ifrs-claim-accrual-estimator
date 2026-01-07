"""
IFRS Claim Accrual Estimator
Rule-based accrual bracket estimation for insurance claims under IFRS 17 principles.
"""

import gradio as gr

# Accrual bracket logic (rule-based, symbolic output only)
def calculate_accrual_bracket(claim_stage, severity_bracket, investigation_duration, ibnr_flag):
    """
    Calculate accrual bracket based on claim characteristics.
    Returns symbolic bracket text only - NO actual monetary amounts.
    
    Args:
        claim_stage: Current stage of claim processing
        severity_bracket: Severity level of the claim
        investigation_duration: Duration of investigation in months
        ibnr_flag: Whether claim is Incurred But Not Reported
        
    Returns:
        Tuple of (accrual_bracket, warnings, uncertainty, explanation)
    """
    
    # Initialize base accrual level
    accrual_level = 0
    warnings = []
    uncertainty_score = 0.0
    
    # Stage-based accrual adjustment
    stage_weights = {
        "Reported": 1,
        "Under Investigation": 2,
        "Evaluated": 3,
        "Settlement Negotiation": 4,
        "Closed": 5
    }
    
    accrual_level += stage_weights.get(claim_stage, 1)
    
    # Severity-based adjustment
    severity_weights = {
        "Minor": 1,
        "Moderate": 2,
        "Severe": 3,
        "Catastrophic": 4
    }
    
    accrual_level += severity_weights.get(severity_bracket, 1)
    
    # Investigation duration adjustment
    if investigation_duration > 12:
        accrual_level += 2
        warnings.append("⚠️ Extended investigation period (>12 months) increases uncertainty")
        uncertainty_score += 0.25
    elif investigation_duration > 6:
        accrual_level += 1
        warnings.append("⚠️ Moderate investigation period (6-12 months)")
        uncertainty_score += 0.15
    
    # IBNR flag adjustment
    if ibnr_flag == "Yes":
        accrual_level += 2
        warnings.append("⚠️ IBNR claim - higher uncertainty in estimation")
        uncertainty_score += 0.30
    
    # Additional uncertainty factors
    if claim_stage == "Reported":
        uncertainty_score += 0.20
    elif claim_stage == "Under Investigation":
        uncertainty_score += 0.15
    
    if severity_bracket == "Catastrophic":
        uncertainty_score += 0.20
        warnings.append("⚠️ Catastrophic severity - consult senior actuarial team")
    
    # Cap uncertainty at 1.0
    uncertainty_score = min(uncertainty_score, 1.0)
    
    # Determine accrual bracket (symbolic only)
    if accrual_level <= 3:
        bracket = "Band A (Low Reserve)"
    elif accrual_level <= 5:
        bracket = "Band B (Moderate Reserve)"
    elif accrual_level <= 7:
        bracket = "Band C (Elevated Reserve)"
    elif accrual_level <= 9:
        bracket = "Band D (High Reserve)"
    else:
        bracket = "Band E (Maximum Reserve)"
    
    # Generate explanation
    explanation = generate_explanation(
        claim_stage, severity_bracket, investigation_duration, 
        ibnr_flag, bracket, accrual_level, warnings, uncertainty_score
    )
    
    return bracket, explanation, uncertainty_score


def generate_explanation(claim_stage, severity_bracket, investigation_duration, 
                        ibnr_flag, bracket, accrual_level, warnings, uncertainty_score):
    """Generate detailed explanation of accrual estimation."""
    
    explanation = f"""### IFRS 17 Accrual Bracket Estimation

**Claim Stage:** {claim_stage}
**Severity Bracket:** {severity_bracket}
**Investigation Duration:** {investigation_duration} months
**IBNR Flag:** {ibnr_flag}

---

**Estimated Accrual Bracket:** {bracket}
**Accrual Level Score:** {accrual_level}/10+
**Uncertainty Score:** {uncertainty_score:.2f}

---

#### Factors Considered:

"""
    
    # Add stage factor
    explanation += f"- **Claim Stage ({claim_stage})**: "
    if claim_stage == "Closed":
        explanation += "Claim is closed, accrual should reflect final settlement\n"
    elif claim_stage == "Settlement Negotiation":
        explanation += "Active settlement discussions, accrual near final amount\n"
    elif claim_stage == "Evaluated":
        explanation += "Claim evaluated, accrual based on assessment\n"
    elif claim_stage == "Under Investigation":
        explanation += "Investigation ongoing, accrual includes development potential\n"
    else:
        explanation += "Early stage, accrual includes significant development uncertainty\n"
    
    # Add severity factor
    explanation += f"- **Severity ({severity_bracket})**: "
    if severity_bracket == "Catastrophic":
        explanation += "Catastrophic severity requires maximum reserve consideration\n"
    elif severity_bracket == "Severe":
        explanation += "Severe claims require elevated reserve levels\n"
    elif severity_bracket == "Moderate":
        explanation += "Moderate severity with standard reserve approach\n"
    else:
        explanation += "Minor severity with lower reserve requirements\n"
    
    # Add investigation duration factor
    explanation += f"- **Investigation Duration ({investigation_duration} months)**: "
    if investigation_duration > 12:
        explanation += "Extended investigation suggests complexity and higher uncertainty\n"
    elif investigation_duration > 6:
        explanation += "Moderate investigation period indicates some complexity\n"
    else:
        explanation += "Standard investigation timeframe\n"
    
    # Add IBNR factor
    explanation += f"- **IBNR Status ({ibnr_flag})**: "
    if ibnr_flag == "Yes":
        explanation += "Incurred But Not Reported - requires additional reserve margin\n"
    else:
        explanation += "Reported claim with known details\n"
    
    # Add warnings section
    if warnings:
        explanation += "\n---\n\n#### ⚠️ Warnings & Considerations:\n\n"
        for warning in warnings:
            explanation += f"- {warning}\n"
    
    # Add mandatory disclaimers
    explanation += """

---

### 🔴 MANDATORY HUMAN REVIEW

**CRITICAL:** This is a symbolic accrual bracket estimation tool only. 

**Required Actions:**
- ✅ **Consult Finance Team**: All accrual decisions must be reviewed by qualified finance/actuarial staff
- ✅ **Verify Assumptions**: Validate all input parameters and assumptions
- ✅ **Apply Company Policy**: Use company-specific reserving policies and guidelines
- ✅ **Consider All Factors**: This tool uses simplified rules - real accruals require comprehensive analysis
- ✅ **Document Decisions**: Maintain proper documentation for all reserve decisions

**This tool does NOT:**
- ❌ Calculate actual monetary reserve amounts
- ❌ Apply company-specific reserving formulas
- ❌ Consider reinsurance or other risk transfers
- ❌ Account for regulatory or accounting policy specifics
- ❌ Replace professional actuarial judgment

---

### ⚠️ Compliance Notice

This project models generic insurance concepts. All outputs are synthetic and made-up for demonstration purposes. 
No proprietary pricing, underwriting rules, policy wording, or confidential logic was used. 

**Outputs are illustrative only and require human review.** 

Not to be used for any pricing, reserving, claim approval, or policy issuance.

**Human-in-the-loop is mandatory for all financial decisions.**
"""
    
    return explanation


# Create Gradio interface
with gr.Blocks(title="IFRS Claim Accrual Estimator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📊 IFRS Claim Accrual Estimator
    
    **Rule-Based Accrual Bracket Estimation for Insurance Claims**
    
    This tool provides symbolic accrual bracket estimates for insurance claims under IFRS 17 principles.
    
    ## ⚠️ MANDATORY DISCLAIMER
    
    **This is a demonstration tool for educational purposes only.**
    
    - ✅ Outputs are **symbolic brackets only** - NO actual monetary amounts
    - ✅ All outputs are **advisory only** and require professional actuarial review
    - ✅ No AI component issues financial approvals or reserve amounts
    - ✅ This tool uses **rule-based logic only** - not actuarial models
    - ✅ No real insurance company data or proprietary formulas are used
    - ✅ Not for use in actual reserving, pricing, or financial reporting
    
    **Consult qualified finance/actuarial professionals for all reserve decisions.**
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Claim Information")
            
            claim_stage = gr.Dropdown(
                choices=["Reported", "Under Investigation", "Evaluated", "Settlement Negotiation", "Closed"],
                label="Claim Stage",
                value="Under Investigation",
                info="Current stage of claim processing"
            )
            
            severity_bracket = gr.Dropdown(
                choices=["Minor", "Moderate", "Severe", "Catastrophic"],
                label="Severity Bracket",
                value="Moderate",
                info="Assessed severity level of the claim"
            )
            
            investigation_duration = gr.Slider(
                minimum=0,
                maximum=36,
                step=1,
                label="Investigation Duration (months)",
                value=3,
                info="How long the claim has been under investigation"
            )
            
            ibnr_flag = gr.Radio(
                choices=["No", "Yes"],
                label="IBNR (Incurred But Not Reported)",
                value="No",
                info="Is this an IBNR claim?"
            )
            
            estimate_btn = gr.Button("📊 Estimate Accrual Bracket", variant="primary", size="lg")
        
        with gr.Column():
            gr.Markdown("### Estimation Results")
            
            bracket_output = gr.Textbox(
                label="Accrual Bracket",
                lines=2,
                interactive=False
            )
            
            uncertainty_output = gr.Number(
                label="Uncertainty Score (0-1)",
                interactive=False
            )
    
    with gr.Row():
        explanation_output = gr.Markdown(label="Detailed Analysis")
    
    estimate_btn.click(
        fn=calculate_accrual_bracket,
        inputs=[claim_stage, severity_bracket, investigation_duration, ibnr_flag],
        outputs=[bracket_output, explanation_output, uncertainty_output]
    )
    
    with gr.Accordion("ℹ️ About This Tool", open=False):
        gr.Markdown("""
        ## How It Works
        
        This accrual estimator uses **configurable business rules** to assign symbolic reserve brackets. 
        It does NOT calculate actual monetary amounts or use actuarial models.
        
        ### Accrual Brackets:
        
        - **Band A (Low Reserve)**: Early stage, minor severity claims
        - **Band B (Moderate Reserve)**: Standard claims with moderate characteristics
        - **Band C (Elevated Reserve)**: Claims with elevated risk factors
        - **Band D (High Reserve)**: Severe claims or extended investigations
        - **Band E (Maximum Reserve)**: Catastrophic or highly uncertain claims
        
        ### Factors Evaluated:
        
        1. **Claim Stage**: Earlier stages have higher uncertainty
        2. **Severity Bracket**: Higher severity requires higher reserves
        3. **Investigation Duration**: Longer investigations suggest complexity
        4. **IBNR Flag**: Unreported claims have additional uncertainty
        
        ### Uncertainty Score:
        
        Indicates confidence in the bracket assignment based on available information. 
        Higher uncertainty suggests more caution and expert review needed.
        
        ### Educational Purposes:
        
        - **Prototyping**: Test IFRS 17 accrual workflows
        - **Training**: Teach claims reserving concepts
        - **Demonstration**: Showcase rule-based estimation systems
        - **Testing**: Validate accrual logic
        
        ### Compliance & Safety:
        
        - ✅ No real insurer names or proprietary information
        - ✅ No actuarial formulas or pricing models
        - ✅ No actual monetary calculations
        - ✅ All outputs marked as advisory only
        - ✅ Human-in-the-loop enforced
        
        ### Limitations:
        
        - Simplified rule-based logic (real reserving uses actuarial models)
        - No integration with actual claims systems
        - No consideration of reinsurance or risk transfers
        - Educational demonstration only
        - Symbolic brackets only - not actual reserve amounts
        
        **Built by Qoder for Vercept**
        """)

if __name__ == "__main__":
    demo.launch()
