"""
IFRS 17 Claim Accrual Estimation Utilities
Provides actuarial calculation functions for claim reserve estimation.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime, timedelta


class ChainLadder:
    """Chain ladder method for ultimate loss estimation."""
    
    def __init__(self, development_patterns: Dict[str, List[float]]):
        """
        Initialize with development patterns.
        
        Args:
            development_patterns: Dictionary mapping claim types to LDF lists
        """
        self.patterns = development_patterns
    
    def get_cumulative_factor(self, claim_type: str, development_period: int) -> float:
        """
        Get cumulative development factor for a claim.
        
        Args:
            claim_type: Type of claim
            development_period: Years since occurrence
            
        Returns:
            Cumulative development factor
        """
        ldfs = self.patterns.get(claim_type, self.patterns.get("Auto", [1.0]))
        
        # Ensure development period is within bounds
        period = min(development_period, len(ldfs) - 1)
        
        # Calculate cumulative factor from current period to ultimate
        if period >= len(ldfs) - 1:
            return 1.0  # Fully developed
        
        cdf = np.prod(ldfs[period:])
        return cdf
    
    def estimate_ultimate(self, incurred: float, claim_type: str, 
                         development_period: int) -> Dict[str, float]:
        """
        Estimate ultimate loss for a claim.
        
        Args:
            incurred: Current incurred loss
            claim_type: Type of claim
            development_period: Years since occurrence
            
        Returns:
            Dictionary with ultimate estimate and development info
        """
        cdf = self.get_cumulative_factor(claim_type, development_period)
        ultimate = incurred * cdf
        
        return {
            'incurred': incurred,
            'development_period': development_period,
            'cumulative_factor': cdf,
            'ultimate_loss': ultimate,
            'ibnr': ultimate - incurred
        }
    
    def batch_estimate(self, claims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Estimate ultimate losses for multiple claims.
        
        Args:
            claims_df: DataFrame with columns: incurred, claim_type, development_period
            
        Returns:
            DataFrame with added ultimate loss estimates
        """
        results = []
        
        for _, row in claims_df.iterrows():
            result = self.estimate_ultimate(
                incurred=row['incurred'],
                claim_type=row['claim_type'],
                development_period=row['development_period']
            )
            results.append(result)
        
        # Add results to dataframe
        claims_df['cumulative_factor'] = [r['cumulative_factor'] for r in results]
        claims_df['ultimate_loss'] = [r['ultimate_loss'] for r in results]
        claims_df['ibnr'] = [r['ibnr'] for r in results]
        
        return claims_df


class RiskAdjustment:
    """Risk adjustment calculations for IFRS 17."""
    
    def __init__(self, risk_factors: Dict[str, float]):
        """
        Initialize with risk adjustment factors.
        
        Args:
            risk_factors: Dictionary mapping risk levels to factors
        """
        self.factors = risk_factors
    
    def calculate(self, ultimate_loss: float, risk_level: str) -> Dict[str, float]:
        """
        Calculate risk adjustment.
        
        Args:
            ultimate_loss: Ultimate loss estimate
            risk_level: Risk/uncertainty level (Low/Medium/High)
            
        Returns:
            Dictionary with risk adjustment details
        """
        factor = self.factors.get(risk_level, 0.10)
        adjustment = ultimate_loss * factor
        
        return {
            'ultimate_loss': ultimate_loss,
            'risk_level': risk_level,
            'risk_factor': factor,
            'risk_adjustment': adjustment
        }
    
    def batch_calculate(self, claims_df: pd.DataFrame, 
                       risk_level_col: str = 'risk_level') -> pd.DataFrame:
        """
        Calculate risk adjustments for multiple claims.
        
        Args:
            claims_df: DataFrame with ultimate_loss and risk_level columns
            risk_level_col: Name of risk level column
            
        Returns:
            DataFrame with added risk adjustment
        """
        results = []
        
        for _, row in claims_df.iterrows():
            result = self.calculate(
                ultimate_loss=row['ultimate_loss'],
                risk_level=row[risk_level_col]
            )
            results.append(result)
        
        claims_df['risk_factor'] = [r['risk_factor'] for r in results]
        claims_df['risk_adjustment'] = [r['risk_adjustment'] for r in results]
        
        return claims_df


class Discounting:
    """Present value discounting for IFRS 17."""
    
    def __init__(self, discount_rate: float):
        """
        Initialize with discount rate.
        
        Args:
            discount_rate: Annual discount rate (e.g., 0.035 for 3.5%)
        """
        self.rate = discount_rate
    
    def calculate_pv(self, future_value: float, years: float) -> Dict[str, float]:
        """
        Calculate present value.
        
        Args:
            future_value: Future cash flow amount
            years: Years until payment
            
        Returns:
            Dictionary with PV calculation details
        """
        if years <= 0:
            discount_factor = 1.0
            present_value = future_value
        else:
            discount_factor = (1 + self.rate) ** (-years)
            present_value = future_value * discount_factor
        
        discount_amount = future_value - present_value
        
        return {
            'future_value': future_value,
            'years': years,
            'discount_rate': self.rate,
            'discount_factor': discount_factor,
            'present_value': present_value,
            'discount_amount': discount_amount
        }
    
    def batch_calculate(self, claims_df: pd.DataFrame, 
                       fv_col: str = 'ultimate_loss',
                       years_col: str = 'years_to_settlement') -> pd.DataFrame:
        """
        Calculate present values for multiple claims.
        
        Args:
            claims_df: DataFrame with future values and timing
            fv_col: Column name for future values
            years_col: Column name for years to settlement
            
        Returns:
            DataFrame with added PV calculations
        """
        results = []
        
        for _, row in claims_df.iterrows():
            result = self.calculate_pv(
                future_value=row[fv_col],
                years=row[years_col]
            )
            results.append(result)
        
        claims_df['discount_factor'] = [r['discount_factor'] for r in results]
        claims_df['present_value'] = [r['present_value'] for r in results]
        claims_df['discount_amount'] = [r['discount_amount'] for r in results]
        
        return claims_df


class IFRS17Accrual:
    """Complete IFRS 17 claim accrual calculator."""
    
    def __init__(self, chain_ladder: ChainLadder, 
                 risk_adjustment: RiskAdjustment,
                 discounting: Discounting):
        """
        Initialize with calculation components.
        
        Args:
            chain_ladder: ChainLadder instance
            risk_adjustment: RiskAdjustment instance
            discounting: Discounting instance
        """
        self.chain_ladder = chain_ladder
        self.risk_adjustment = risk_adjustment
        self.discounting = discounting
    
    def calculate_accrual(self, 
                         incurred: float,
                         paid: float,
                         claim_type: str,
                         development_period: int,
                         years_to_settlement: float,
                         risk_level: str) -> Dict[str, float]:
        """
        Calculate complete IFRS 17 accrual for a claim.
        
        Args:
            incurred: Current incurred loss
            paid: Amount already paid
            claim_type: Type of claim
            development_period: Years since occurrence
            years_to_settlement: Years until expected settlement
            risk_level: Risk/uncertainty level
            
        Returns:
            Dictionary with complete accrual breakdown
        """
        # Step 1: Estimate ultimate loss
        ultimate_est = self.chain_ladder.estimate_ultimate(
            incurred, claim_type, development_period
        )
        ultimate = ultimate_est['ultimate_loss']
        
        # Step 2: Calculate outstanding claims
        outstanding = ultimate - paid
        
        # Step 3: Calculate risk adjustment
        risk_adj = self.risk_adjustment.calculate(ultimate, risk_level)
        
        # Step 4: Discount ultimate and outstanding
        pv_ultimate = self.discounting.calculate_pv(ultimate, years_to_settlement)
        pv_outstanding = self.discounting.calculate_pv(outstanding, years_to_settlement)
        
        # Step 5: Total accrual
        total_accrual = pv_outstanding['present_value'] + risk_adj['risk_adjustment']
        
        return {
            'incurred': incurred,
            'paid': paid,
            'ultimate_loss': ultimate,
            'outstanding_claims': outstanding,
            'risk_adjustment': risk_adj['risk_adjustment'],
            'pv_ultimate': pv_ultimate['present_value'],
            'pv_outstanding': pv_outstanding['present_value'],
            'discount_amount': pv_ultimate['discount_amount'],
            'total_accrual': total_accrual,
            'development_period': development_period,
            'years_to_settlement': years_to_settlement,
            'risk_level': risk_level
        }
    
    def batch_calculate(self, claims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate accruals for multiple claims.
        
        Args:
            claims_df: DataFrame with required columns
            
        Returns:
            DataFrame with complete accrual calculations
        """
        results = []
        
        for _, row in claims_df.iterrows():
            result = self.calculate_accrual(
                incurred=row['incurred'],
                paid=row['paid'],
                claim_type=row['claim_type'],
                development_period=row['development_period'],
                years_to_settlement=row['years_to_settlement'],
                risk_level=row['risk_level']
            )
            results.append(result)
        
        # Create results dataframe
        results_df = pd.DataFrame(results)
        
        # Merge with original data
        output_df = pd.concat([claims_df.reset_index(drop=True), 
                              results_df.reset_index(drop=True)], axis=1)
        
        return output_df
    
    def get_summary_statistics(self, claims_df: pd.DataFrame) -> Dict[str, float]:
        """
        Get summary statistics for a portfolio of claims.
        
        Args:
            claims_df: DataFrame with calculated accruals
            
        Returns:
            Dictionary with summary statistics
        """
        if 'total_accrual' not in claims_df.columns:
            claims_df = self.batch_calculate(claims_df)
        
        return {
            'total_claims': len(claims_df),
            'total_incurred': claims_df['incurred'].sum(),
            'total_paid': claims_df['paid'].sum(),
            'total_ultimate': claims_df['ultimate_loss'].sum(),
            'total_outstanding': claims_df['outstanding_claims'].sum(),
            'total_risk_adjustment': claims_df['risk_adjustment'].sum(),
            'total_discount': claims_df['discount_amount'].sum(),
            'total_accrual': claims_df['total_accrual'].sum(),
            'avg_development_period': claims_df['development_period'].mean(),
            'avg_years_to_settlement': claims_df['years_to_settlement'].mean()
        }
