---
title: IFRS Claim Accrual Estimator
emoji: 📊
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# IFRS 17 Claim Accrual Estimator

## Overview

An interactive demonstration tool for estimating symbolic accrual brackets for insurance claims under IFRS 17 principles. This application uses rule-based logic to assign reserve brackets based on claim characteristics. **Note: This tool provides symbolic brackets only, NOT actual monetary amounts.**

---

## Disclaimer

This project models generic insurance concepts common in GCC markets. All datasets are synthetic and made-up for demonstration and research purposes. No proprietary pricing, underwriting rules, policy wording, or confidential logic was used. Outputs are illustrative only and require human review. Not to be used for any pricing, reserving, claim approval, or policy issuance.

## Human-In-The-Loop

No AI component here issues approvals, denials, or financial outcomes. All outputs require human verification and decision-making.

---

## Features

- **Accrual Bracket Assignment**: Rule-based symbolic bracket estimation (Band A through E)
- **Claim Stage Analysis**: Considers current stage of claim processing
- **Severity Assessment**: Evaluates claim severity impact on reserves
- **Investigation Duration**: Accounts for complexity indicated by investigation length
- **IBNR Handling**: Special consideration for Incurred But Not Reported claims
- **Uncertainty Scoring**: Confidence assessment based on available information
- **Human Review Warnings**: Mandatory human-in-the-loop enforcement
- **Interactive Interface**: Real-time bracket assignment with detailed explanations

## Accrual Brackets

This tool assigns symbolic reserve brackets based on claim characteristics:

### Band A (Low Reserve)
- Early stage claims with minor severity
- Short investigation periods
- Reported claims with good information

### Band B (Moderate Reserve)
- Standard claims with moderate characteristics
- Normal investigation timeframes
- Typical severity levels

### Band C (Elevated Reserve)
- Claims with elevated risk factors
- Moderate investigation duration or severity
- Some uncertainty in estimation

### Band D (High Reserve)
- Severe claims or extended investigations
- Higher uncertainty factors
- Complex claim scenarios

### Band E (Maximum Reserve)
- Catastrophic severity claims
- IBNR with high uncertainty
- Maximum reserve consideration required

## Input Parameters

Compensation for uncertainty about amount and timing:
- **Low Risk**: 5% of ultimate loss
- **Medium Risk**: 10% of ultimate loss
- **High Risk**: 20% of ultimate loss

### 4. Discounting

Present value calculation using:
- Configurable discount rate (0-10%)
- Time to expected settlement
- Standard discounting formula: PV = FV / (1 + r)^t

### 5. Total Accrual

Final reserve requirement:
```
Total Accrual = PV(Outstanding Claims) + Risk Adjustment
```

## Usage

### Input Parameters

**Claim Information:**
- Claim ID
- Claim Type (Auto, Property, Liability, Health, Workers Comp)
- Incurred Loss (current estimate)
- Paid Loss (amount already paid)

**Timing & Risk:**
- Occurrence Date (when claim happened)
- Expected Settlement Date (when claim will be closed)
- Risk/Uncertainty Level (Low/Medium/High)
- Discount Rate (annual percentage)

### Output

The tool provides:

1. **Summary Report**: Key estimates and calculations
2. **Detailed Breakdown**: Component-by-component analysis
3. **Calculation Notes**: Methodology explanations

## Methodology

### Chain Ladder Method

The chain ladder technique is an industry-standard actuarial method that:

1. Analyzes historical claim development patterns
2. Applies development factors to immature claims
3. Projects ultimate losses

**Example Development Pattern (Auto):**
- Year 1: 3.5x (claims develop to 3.5x initial report)
- Year 2: 2.2x
- Year 3: 1.5x
- ...
- Year 10: 1.0x (fully developed)

### Risk Adjustment Calculation

Risk adjustment reflects the compensation an entity requires for bearing uncertainty:

```python
Risk Adjustment = Ultimate Loss × Risk Factor
```

Where risk factor depends on uncertainty level.

### Discounting

Present value calculation:

```python
PV = Ultimate Loss / (1 + discount_rate)^years_to_settlement
```

## Example Calculation

**Inputs:**
- Claim Type: Auto
- Incurred Loss: $50,000
- Paid Loss: $15,000
- Months Since Occurrence: 18
- Months to Settlement: 30
- Risk Level: Medium
- Discount Rate: 3.5%

**Outputs:**
- Ultimate Loss: ~$75,000 (using 1.5x development factor)
- Outstanding Claims: $60,000
- Risk Adjustment: $7,500 (10% of ultimate)
- Discount: ~$5,000
- Total Accrual: ~$62,500

## Compliance & Safety

⚠️ **IMPORTANT DISCLAIMERS**:

- This is a **demonstration tool only** using simplified assumptions
- **Not suitable for actual financial reporting** or regulatory compliance
- All development factors and patterns are **synthetic/illustrative**
- Does not replace professional actuarial analysis
- No real insurer data, policies, or proprietary formulas used
- All outputs are **advisory only**
- Not intended for pricing, quoting, or underwriting

## Technical Details

- **Framework**: Gradio 4.44.0
- **Language**: Python 3.9+
- **Dependencies**: pandas, numpy
- **Methods**: Chain ladder, discounted cash flow

## About IFRS 17

IFRS 17 is the International Financial Reporting Standard for insurance contracts, effective January 1, 2023. It requires insurers to measure insurance liabilities using:

1. **Fulfillment Cash Flows** (FCF)
   - Estimates of future cash flows
   - Adjustment for time value of money (discounting)
   - Risk adjustment for non-financial risk

2. **Contractual Service Margin** (CSM)
   - Unearned profit recognized over coverage period

This tool focuses on the **Liability for Incurred Claims (LIC)** component of FCF.

## Limitations

- Simplified development patterns (real actuarial analysis uses triangles with years of data)
- Single development factor per year (real analysis may use quarterly or monthly)
- No consideration of claim-specific characteristics
- No tail factor or trend adjustments
- Simplified risk adjustment (real calculations use stochastic modeling)
- No consideration of reinsurance
- No expense provisions

## License

MIT License

---

**Built by Qoder for Vercept**

---

**For educational and demonstration purposes only**
