from django.contrib import admin
from .models import ForexPair, ForexData, TechnicalIndicators, TradingSignal


@admin.register(ForexPair)
class ForexPairAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('symbol', 'name')


@admin.register(ForexData)
class ForexDataAdmin(admin.ModelAdmin):
    list_display = ('pair', 'timestamp', 'close_price', 'volume')
    list_filter = ('pair', 'timestamp')
    search_fields = ('pair__symbol',)
    ordering = ('-timestamp',)


@admin.register(TechnicalIndicators)
class TechnicalIndicatorsAdmin(admin.ModelAdmin):
    list_display = ('forex_data', 'rsi', 'rsi_signal', 'macd')
    list_filter = ('rsi_signal', 'forex_data__pair')
    search_fields = ('forex_data__pair__symbol',)
    ordering = ('-forex_data__timestamp',)


@admin.register(TradingSignal)
class TradingSignalAdmin(admin.ModelAdmin):
    list_display = ('pair', 'signal_type', 'confidence', 'greed_level', 'timestamp')
    list_filter = ('signal_type', 'greed_level', 'timestamp', 'pair')
    search_fields = ('pair__symbol', 'reason')
    ordering = ('-timestamp',)
