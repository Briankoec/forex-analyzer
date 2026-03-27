import numpy as np
import pandas as pd
from decimal import Decimal


class TechnicalAnalyzer:
    """Calculate technical indicators for forex analysis"""

    @staticmethod
    def calculate_rsi(prices, period=14):
        """
        Calculate Relative Strength Index (RSI)
        RSI = 100 - (100 / (1 + RS))
        where RS = Average Gain / Average Loss
        """
        if len(prices) < period + 1:
            return None

        prices = np.array([float(p) for p in prices])
        deltas = np.diff(prices)
        
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])

        if avg_loss == 0:
            return 100 if avg_gain > 0 else 50

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)

    @staticmethod
    def calculate_macd(prices, fast=12, slow=26, signal=9):
        """
        Calculate MACD (Moving Average Convergence Divergence)
        Returns: (MACD, Signal Line, Histogram)
        """
        if len(prices) < slow:
            return None, None, None

        prices = np.array([float(p) for p in prices])
        
        # Calculate exponential moving averages
        ema_fast = TechnicalAnalyzer._ema(prices, fast)
        ema_slow = TechnicalAnalyzer._ema(prices, slow)
        
        if ema_fast is None or ema_slow is None:
            return None, None, None

        macd = ema_fast - ema_slow
        
        # Signal line is EMA of MACD
        macd_array = np.full(len(prices), np.nan)
        macd_array[-1] = macd
        signal_line = TechnicalAnalyzer._ema(macd_array[~np.isnan(macd_array)], signal)
        
        histogram = macd - signal_line if signal_line is not None else None
        
        return round(macd, 5), round(signal_line, 5) if signal_line else None, round(histogram, 5) if histogram else None

    @staticmethod
    def calculate_sma(prices, period=20):
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return None
        
        prices = np.array([float(p) for p in prices])
        return round(float(np.mean(prices[-period:])), 5)

    @staticmethod
    def _ema(prices, period):
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return None
        
        prices = np.array([float(p) for p in prices])
        multiplier = 2 / (period + 1)
        
        # Start with SMA
        ema = np.mean(prices[:period])
        
        # Calculate EMA for remaining prices
        for i in range(period, len(prices)):
            ema = (prices[i] - ema) * multiplier + ema
        
        return ema

    @staticmethod
    def get_rsi_signal(rsi):
        """Determine RSI signal: overbought (>70), oversold (<30), or normal"""
        if rsi is None:
            return 'normal'
        
        if rsi > 70:
            return 'overbought'
        elif rsi < 30:
            return 'oversold'
        else:
            return 'normal'

    @staticmethod
    def get_greed_level(rsi):
        """
        Map RSI to greed level
        RSI > 80: Extreme Greed
        RSI 60-80: Greed
        RSI 40-60: Neutral
        RSI 20-40: Fear
        RSI < 20: Extreme Fear
        """
        if rsi is None:
            return 'neutral'
        
        if rsi > 80:
            return 'extreme_greed'
        elif rsi > 60:
            return 'greed'
        elif rsi < 20:
            return 'extreme_fear'
        elif rsi < 40:
            return 'fear'
        else:
            return 'neutral'


class TradingSignalGenerator:
    """Generate buy/sell signals based on technical indicators"""

    @staticmethod
    def generate_signal(rsi, macd_value, macd_signal, sma_20, sma_50, current_price):
        """
        Generate trading signal based on RSI and MACD
        
        Buy Signals:
        - RSI < 30 (oversold) + MACD crosses above signal line
        - SMA 20 > SMA 50 (uptrend) + RSI < 50
        
        Sell Signals:
        - RSI > 70 (overbought) + MACD crosses below signal line
        - SMA 20 < SMA 50 (downtrend) + RSI > 50
        """
        reasons = []
        confidence = 0
        signal_type = 'HOLD'

        # RSI Analysis
        if rsi is not None:
            if rsi < 30:
                reasons.append("RSI oversold (< 30)")
                confidence += 35
            elif rsi > 70:
                reasons.append("RSI overbought (> 70)")
                confidence += 35

        # MACD Analysis
        if macd_value is not None and macd_signal is not None:
            macd_diff = macd_value - macd_signal
            if macd_diff > 0:
                reasons.append("MACD above signal line (bullish)")
                confidence += 25
            elif macd_diff < 0:
                reasons.append("MACD below signal line (bearish)")
                confidence -= 25

        # SMA Analysis
        if sma_20 is not None and sma_50 is not None:
            if sma_20 > sma_50:
                reasons.append("SMA 20 > SMA 50 (uptrend)")
                confidence += 20
            elif sma_20 < sma_50:
                reasons.append("SMA 20 < SMA 50 (downtrend)")
                confidence -= 20

        # Determine signal type
        if confidence > 40 and rsi is not None and rsi < 50:
            signal_type = 'BUY'
        elif confidence < -40 and rsi is not None and rsi > 50:
            signal_type = 'SELL'
        else:
            signal_type = 'HOLD'

        confidence = max(0, min(100, confidence + 50))  # Normalize to 0-100

        return {
            'signal_type': signal_type,
            'confidence': confidence,
            'reason': ' | '.join(reasons) if reasons else 'Insufficient data for strong signal',
        }
