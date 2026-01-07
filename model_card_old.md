# Model Card: IFRS 17 Claim Accrual Estimator

## Model Details

### Model Description

This is a **calculation-based estimation tool** for insurance claim reserves under IFRS 17 accounting standards. It applies actuarial methods (chain ladder) and IFRS 17 measurement principles to estimate claim liabilities.

- **Developed by:** Qoder for Vercept
- **Model type:** Deterministic calculation engine (not ML)
- **Language:** Python
- **License:** MIT

### Model Sources

- **Repository:** Hugging Face Spaces
- **Demo:** Interactive Gradio interface

## Uses

### Direct Use

This tool is designed for:

- **Educational purposes**: Learning IFRS 17 measurement principles
- **Demonstration**: Showcasing actuarial reserve calculations
- **Training**: Teaching insurance accounting concepts
- **Prototyping**: Testing reserve estimation workflows
- **Concept validation**: Understanding component interactions

### Downstream Use

Not applicable - this is a standalone demonstration tool.

### Out-of-Scope Use

⚠️ **This tool should NOT be used for:**

- Actual financial reporting or statutory filings
- Regulatory compliance (Solvency II, local GAAP, etc.)
- Audit support or external reporting
- Investment decisions or portfolio management
- Pricing, underwriting, or risk management
- Any decision affecting real financial statements
- Production actuarial reserving

## Bias, Risks, and Limitations

### Known Limitations

1. **Simplified Development Patterns**: Uses generic LDFs, not company-specific experience
2. **No Historical Data**: Does not analyze actual loss triangles
3. **Single Point Estimates**: No confidence intervals or stochastic modeling
4. **No Tail Factors**: Development stops at year 10
5. **No Trend Adjustments**: Does not account for inflation or claim cost trends
6. **Simplified Risk Adjustment**: Uses percentage factors instead of stochastic analysis
7. **No Reinsurance**: Does not consider reinsurance recoveries
8. **No Expenses**: Does not include claim adjustment expenses
9. **Single Discount Curve**: Real IFRS 17 uses complex yield curves
10. **No Validation**: Development factors are illustrative, not validated

### Potential Issues

- **Oversimplification**: Real actuarial analysis is far more complex
- **Pattern Mismatch**: Generic patterns may not reflect actual claim behavior
- **Risk Adjustment**: Percentage-based approach is not IFRS 17 compliant (should use confidence level method)
- **Discount Rate**: Single rate assumption vs. term structure of interest rates
- **No Uncertainty Quantification**: Provides point estimates without ranges

### Recommendations

Users should:

- Understand this is a **simplified demonstration only**
- Never use for actual financial reporting
- Consult qualified actuaries for real reserve estimates
- Recognize the difference between this tool and production actuarial systems
- Review IFRS 17 standards and actuarial standards of practice
- Seek professional guidance for implementation

## How to Get Started with the Model

```python
import gradio as gr
from app import demo

# Launch the interface
demo.launch()
```

Or visit the Hugging Face Space to use the interactive demo.

## Training Details

Not applicable - this is a calculation-based system using predefined formulas and development patterns.

## Evaluation

### Testing Data, Factors & Metrics

No formal evaluation has been conducted. The tool applies deterministic calculations without statistical validation against real claim data.

### Results

Not applicable.

## Environmental Impact

Minimal - this is a lightweight calculation tool with no training requirements.

## Technical Specifications

### Calculation Architecture

**Components:**

1. **Ultimate Loss Estimation**
   - Method: Chain Ladder
   - Input: Incurred loss, claim type, development period
   - Output: Projected ultimate loss
   - Formula: Ultimate = Incurred × Cumulative Development Factor

2. **Outstanding Claims**
   - Formula: Outstanding = Ultimate Loss - Paid Loss
   - Includes case reserves and IBNR

3. **Risk Adjustment**
   - Method: Percentage of ultimate loss
   - Factors: 5% (Low), 10% (Medium), 20% (High)
   - Note: Simplified vs. IFRS 17 confidence level approach

4. **Discounting**
   - Method: Standard present value formula
   - Formula: PV = FV / (1 + r)^t
   - Input: Discount rate, time to settlement

5. **Total Accrual**
   - Formula: PV(Outstanding) + Risk Adjustment

### Development Patterns

**Loss Development Factors (LDFs) by Claim Type:**

- **Auto**: [3.5, 2.2, 1.5, 1.2, 1.1, 1.05, 1.02, 1.01, 1.005, 1.0]
- **Property**: [2.8, 1.9, 1.4, 1.15, 1.08, 1.04, 1.02, 1.01, 1.005, 1.0]
- **Liability**: [5.0, 3.5, 2.5, 1.8, 1.4, 1.2, 1.1, 1.05, 1.02, 1.01]
- **Health**: [2.0, 1.5, 1.2, 1.1, 1.05, 1.02, 1.01, 1.005, 1.0, 1.0]
- **Workers Comp**: [4.5, 3.0, 2.2, 1.6, 1.3, 1.15, 1.08, 1.04, 1.02, 1.01]

These patterns are **synthetic and illustrative only**.

### Compute Infrastructure

**Requirements**: Minimal - runs on CPU

**Dependencies**:
- Python 3.9+
- Gradio 4.44.0
- Pandas 2.1.4
- NumPy 1.26.2

## Model Card Contact

For questions or feedback, contact Vercept.

## Glossary

- **IFRS 17**: International Financial Reporting Standard for insurance contracts
- **LIC**: Liability for Incurred Claims
- **Chain Ladder**: Actuarial method for projecting ultimate losses
- **LDF**: Loss Development Factor - ratio of losses at successive evaluation points
- **IBNR**: Incurred But Not Reported - claims that have occurred but not yet reported
- **Risk Adjustment**: Compensation for uncertainty about amount and timing of cash flows
- **Discounting**: Adjustment for time value of money
- **Ultimate Loss**: Final projected cost of a claim when fully settled
- **Fulfillment Cash Flows**: IFRS 17 term for present value of future cash flows
- **CSM**: Contractual Service Margin - unearned profit in IFRS 17

## IFRS 17 Context

### Standard Overview

IFRS 17 requires insurance liabilities to be measured as:

```
Insurance Liability = Fulfillment Cash Flows + Contractual Service Margin
```

Where Fulfillment Cash Flows (FCF) consist of:

1. Estimates of future cash flows
2. Discount adjustment (time value of money)
3. Risk adjustment for non-financial risk

### This Tool's Scope

This tool focuses on the **Liability for Incurred Claims (LIC)** component, which is part of FCF. It does not address:

- Liability for Remaining Coverage (LRC)
- Contractual Service Margin (CSM)
- Loss component
- Coverage units
- Onerous contract testing

### Differences from Full IFRS 17

| Component | This Tool | Full IFRS 17 |
|-----------|-----------|--------------|
| Risk Adjustment | Percentage of ultimate | Confidence level method (e.g., 75th percentile) |
| Discount Rate | Single rate | Term structure of risk-free rates |
| Cash Flows | Ultimate loss estimate | Detailed payment patterns |
| Uncertainty | None | Stochastic modeling often used |
| Reinsurance | Not included | Separate measurement required |
| Expenses | Not included | Must include claim adjustment expenses |

## Model Card Authors

Qoder (Vercept)

## Disclaimer

⚠️ **CRITICAL NOTICE**:

This project models generic insurance concepts common in GCC markets. All datasets are synthetic and made-up for demonstration and research purposes. No proprietary pricing, underwriting rules, policy wording, or confidential logic was used. Outputs are illustrative only and require human review. Not to be used for any pricing, reserving, claim approval, or policy issuance.

## Human-In-The-Loop

No AI component here issues approvals, denials, or financial outcomes. All outputs require human verification and decision-making.

---

This is a **simplified educational tool** using synthetic data and illustrative assumptions. It is **not suitable for**:

- Financial reporting under IFRS 17 or any other standard
- Regulatory filings or compliance
- Audit support
- Investment decisions
- Actuarial opinions
- Any real-world financial decision-making

All development factors, risk adjustments, and calculations are **demonstrative only** and do not reflect actual insurance experience or comply with full IFRS 17 requirements.

**For actual IFRS 17 implementation, consult qualified actuaries and accounting professionals.**
