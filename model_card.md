# Model Card: IFRS Claim Accrual Estimator

## Disclaimer

⚠️ **CRITICAL NOTICE:**

This tool is for **educational and demonstration purposes ONLY**. It does NOT provide financial advice, accounting guidance, or regulatory compliance support.

- **NOT for production use** in financial reporting or statutory filings
- **NOT a substitute** for qualified actuaries or finance professionals
- **All outputs are advisory only** and require human validation
- **Consult finance and actuarial teams** before any business decisions

## Model Details

### Model Description

This is a **rule-based accrual estimation system** for insurance claims. It does not use machine learning models but instead applies configurable business rules to assign symbolic accrual brackets based on claim characteristics.

- **Developed by:** Qoder for Vercept
- **Model type:** Rule-based decision system
- **Language:** Python
- **License:** MIT

### Model Sources

- **Repository:** Hugging Face Spaces
- **Demo:** Interactive Gradio interface

## Uses

### Direct Use

This tool is designed for:

- **Educational purposes**: Understanding claim accrual concepts
- **Demonstration**: Showcasing rule-based accrual bracket assignment
- **Training**: Teaching insurance finance workflows
- **Prototyping**: Testing accrual estimation logic
- **Concept validation**: Understanding how claim characteristics affect reserves

### Downstream Use

Not applicable - this is a standalone demonstration tool.

### Out-of-Scope Use

⚠️ **This tool should NOT be used for:**

- Actual financial reporting or statutory filings
- Regulatory compliance (IFRS 17, Solvency II, local GAAP)
- Audit support or external reporting
- Investment decisions or portfolio management
- Setting actual reserve amounts or pricing
- Any decision affecting real financial statements
- Production actuarial reserving or accounting
- Replacing qualified finance professionals

## Bias, Risks, and Limitations

### Known Limitations

1. **Symbolic Brackets Only**: Provides Band A-E labels, not actual monetary amounts
2. **Rule-Based Logic**: Uses simple if-then rules, not statistical models
3. **No Historical Data**: Does not analyze company-specific claim patterns
4. **Generic Factors**: Accrual factors are illustrative, not validated
5. **No Uncertainty Quantification**: Provides point estimates without confidence intervals
6. **Simplified IBNR**: Basic toggle, not sophisticated IBNR modeling
7. **No Reinsurance**: Does not consider reinsurance recoveries
8. **No Expenses**: Does not include claim adjustment expenses
9. **No Discounting**: Does not apply time value of money adjustments
10. **No Validation**: Rules are for demonstration only, not actuarially validated

### Potential Issues

- **Oversimplification**: Real accrual estimation requires complex actuarial analysis
- **Generic Rules**: Rules may not reflect actual company-specific patterns
- **No Monetary Amounts**: Symbolic brackets require finance team interpretation
- **No Regulatory Compliance**: Does not follow IFRS 17 or other accounting standards
- **Human Validation Required**: All outputs must be reviewed by qualified professionals

### Recommendations

Users should:

- Understand this is a **simplified demonstration only**
- Never use for actual financial reporting or accounting
- **Always consult finance and actuarial teams** before any decisions
- Recognize the difference between this tool and production systems
- Review IFRS 17 and other relevant accounting standards
- Seek professional guidance for implementation
- Validate all outputs with qualified professionals

## How to Get Started with the Model

```python
import gradio as gr
from app import demo

# Launch the interface
demo.launch()
```

Or visit the Hugging Face Space to use the interactive demo.

## Training Details

Not applicable - this is a rule-based system using predefined business logic, not a machine learning model.

## Evaluation

### Testing Data, Factors & Metrics

The tool has been tested with various claim scenarios to ensure:

- Correct bracket assignment based on input combinations
- Appropriate uncertainty scoring
- Proper warning generation for edge cases
- Consistent human-in-the-loop enforcement

### Results

The rule logic correctly assigns accrual brackets based on:

- **Claim Stage**: Early vs. late stage claims
- **Severity Bracket**: Low, Medium, High, Catastrophic
- **Investigation Duration**: Short, Medium, Long
- **IBNR Flag**: Whether claim is incurred but not reported

**Accrual Brackets:**

- **Band A**: Minimal accrual (early stage, low severity)
- **Band B**: Low accrual (early-mid stage, low-medium severity)
- **Band C**: Moderate accrual (mid stage, medium severity)
- **Band D**: Substantial accrual (late stage, high severity)
- **Band E**: Maximum accrual (catastrophic or complex cases)

## Technical Specifications

### Model Architecture and Objective

**Architecture**: Rule-based decision tree

**Logic Flow**:
1. Parse input parameters (claim_stage, severity_bracket, investigation_duration, IBNR)
2. Apply scoring rules to calculate base accrual factor
3. Apply multipliers for IBNR and investigation duration
4. Assign symbolic bracket (Band A-E) based on final score
5. Calculate uncertainty score based on input characteristics
6. Generate warnings and recommendations
7. Enforce mandatory "consult finance" disclaimer

### Compute Infrastructure

Runs on standard CPU infrastructure. No GPU required.

## Environmental Impact

Minimal - simple rule-based calculations with negligible computational requirements.

## Citation

**BibTeX:**

```bibtex
@software{ifrs_claim_accrual_estimator,
  author = {Qoder for Vercept},
  title = {IFRS Claim Accrual Estimator},
  year = {2026},
  publisher = {Hugging Face},
  howpublished = {\url{https://huggingface.co/spaces/}}
}
```

## Glossary

- **Accrual**: Reserve amount set aside for expected claim payments
- **IBNR**: Incurred But Not Reported - claims that have occurred but not yet been reported
- **IFRS 17**: International Financial Reporting Standard for insurance contracts
- **Claim Stage**: Phase of claim lifecycle (Reported, Investigation, Settlement, Closed)
- **Severity Bracket**: Expected magnitude of claim loss
- **Investigation Duration**: Time spent investigating claim validity and amount

## More Information

For questions or feedback, please visit the Hugging Face Space discussion board.

## Model Card Authors

Qoder for Vercept

## Model Card Contact

Via Hugging Face Space discussions
