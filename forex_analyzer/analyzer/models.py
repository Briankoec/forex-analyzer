from django.db import models
from django.utils import timezone

class ForexPair(models.Model):
    symbol = models.CharField(max_length=10, unique=True)  # e.g., EUR/USD
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['symbol']

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class ForexData(models.Model):
    pair = models.ForeignKey(ForexPair, on_delete=models.CASCADE, related_name='data')
    timestamp = models.DateTimeField()
    open_price = models.DecimalField(max_digits=10, decimal_places=5)
    high_price = models.DecimalField(max_digits=10, decimal_places=5)
    low_price = models.DecimalField(max_digits=10, decimal_places=5)
    close_price = models.DecimalField(max_digits=10, decimal_places=5)
    volume = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('pair', 'timestamp')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['pair', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.pair.symbol} - {self.timestamp}"


class TechnicalIndicators(models.Model):
    forex_data = models.OneToOneField(ForexData, on_delete=models.CASCADE, related_name='indicators')
    rsi = models.FloatField(null=True, blank=True)  # Relative Strength Index (0-100) - GREED SCALE
    rsi_signal = models.CharField(
        max_length=10,
        choices=[('overbought', 'Overbought'), ('normal', 'Normal'), ('oversold', 'Oversold')],
        default='normal'
    )
    macd = models.FloatField(null=True, blank=True)  # MACD line
    macd_signal = models.FloatField(null=True, blank=True)  # Signal line
    macd_histogram = models.FloatField(null=True, blank=True)  # MACD histogram
    sma_20 = models.FloatField(null=True, blank=True)  # 20-period Simple Moving Average
    sma_50 = models.FloatField(null=True, blank=True)  # 50-period Simple Moving Average
    
    class Meta:
        ordering = ['-forex_data__timestamp']

    def __str__(self):
        return f"Indicators for {self.forex_data.pair.symbol} at {self.forex_data.timestamp}"


class TradingSignal(models.Model):
    pair = models.ForeignKey(ForexPair, on_delete=models.CASCADE, related_name='signals')
    timestamp = models.DateTimeField(auto_now_add=True)
    signal_type = models.CharField(
        max_length=10,
        choices=[('BUY', 'Buy'), ('SELL', 'Sell'), ('HOLD', 'Hold')]
    )
    confidence = models.FloatField()  # 0-100
    reason = models.TextField()
    price_at_signal = models.DecimalField(max_digits=10, decimal_places=5)
    rsi_value = models.FloatField(null=True, blank=True)
    macd_value = models.FloatField(null=True, blank=True)
    greed_level = models.CharField(
        max_length=20,
        choices=[
            ('extreme_greed', 'Extreme Greed'),
            ('greed', 'Greed'),
            ('neutral', 'Neutral'),
            ('fear', 'Fear'),
            ('extreme_fear', 'Extreme Fear')
        ]
    )
    is_active = models.BooleanField(default=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.signal_type} signal for {self.pair.symbol} at {self.timestamp}"
