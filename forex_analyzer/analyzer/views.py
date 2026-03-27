from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch
from datetime import datetime, timedelta
import json

from .models import ForexPair, ForexData, TechnicalIndicators, TradingSignal
from .indicators import TechnicalAnalyzer, TradingSignalGenerator
from .api_client import AlphaVantageClient


def index(request):
    """Dashboard view"""
    active_pairs = ForexPair.objects.filter(is_active=True)
    
    context = {
        'pairs': active_pairs,
        'total_pairs': active_pairs.count(),
    }
    
    return render(request, 'index.html', context)


def pair_detail(request, pair_id):
    """Detailed analysis for a specific forex pair"""
    pair = get_object_or_404(ForexPair, id=pair_id)
    
    # Get last 100 data points
    forex_data = ForexData.objects.filter(pair=pair).order_by('-timestamp').all()[:100]
    forex_data = list(forex_data)
    forex_data.reverse()
    
    # Get recent signals
    signals = TradingSignal.objects.filter(pair=pair, is_active=True).order_by('-timestamp')[:20]
    
    context = {
        'pair': pair,
        'data_points': forex_data,
        'signals': signals,
        'latest_data': forex_data[-1] if forex_data else None,
    }
    
    return render(request, 'pair_detail.html', context)


@require_http_methods(["POST"])
def refresh_pair(request, pair_id):
    """Manually refresh data for a pair"""
    pair = get_object_or_404(ForexPair, id=pair_id)
    
    try:
        # Extract base and quote currency from symbol (e.g., EUR/USD -> EUR, USD)
        parts = pair.symbol.split('/')
        if len(parts) != 2:
            return JsonResponse({'success': False, 'error': 'Invalid pair format'}, status=400)
        
        base_currency, quote_currency = parts
        
        # Fetch data from API
        client = AlphaVantageClient()
        time_series = client.get_forex_daily(base_currency, quote_currency)
        
        if not time_series:
            return JsonResponse({'success': False, 'error': 'No data returned from API'}, status=400)
        
        # Parse and save data
        parsed_data = AlphaVantageClient.parse_forex_data(time_series)
        
        saved_count = 0
        for data_point in parsed_data:
            forex_data, created = ForexData.objects.update_or_create(
                pair=pair,
                timestamp=data_point['timestamp'],
                defaults={
                    'open_price': data_point['open'],
                    'high_price': data_point['high'],
                    'low_price': data_point['low'],
                    'close_price': data_point['close'],
                }
            )
            if created:
                saved_count += 1
        
        # Generate indicators for latest data
        latest_data = ForexData.objects.filter(pair=pair).order_by('-timestamp').first()
        if latest_data:
            generate_indicators_for_pair(pair)
            generate_signals_for_pair(pair)
        
        return JsonResponse({
            'success': True,
            'message': f'Updated {saved_count} data points for {pair.symbol}'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def api_pair_data(request, pair_id):
    """API endpoint for chart data"""
    pair = get_object_or_404(ForexPair, id=pair_id)
    
    # Get last 60 data points
    forex_data = list(ForexData.objects.filter(pair=pair).order_by('-timestamp')[:60])
    forex_data.reverse()
    
    data = {
        'pair': pair.symbol,
        'data_points': [
            {
                'timestamp': data.timestamp.isoformat(),
                'close': float(data.close_price),
                'close_price': float(data.close_price),
                'open': float(data.open_price),
                'open_price': float(data.open_price),
                'high': float(data.high_price),
                'high_price': float(data.high_price),
                'low': float(data.low_price),
                'low_price': float(data.low_price),
                'volume': data.volume if data.volume else 0,
                'indicators': {
                    'rsi': float(data.indicators.rsi) if (hasattr(data, 'indicators') and data.indicators and data.indicators.rsi) else None,
                    'macd': float(data.indicators.macd) if (hasattr(data, 'indicators') and data.indicators and data.indicators.macd) else None,
                    'macd_signal': float(data.indicators.macd_signal) if (hasattr(data, 'indicators') and data.indicators and data.indicators.macd_signal) else None,
                    'sma_20': float(data.indicators.sma_20) if (hasattr(data, 'indicators') and data.indicators and data.indicators.sma_20) else None,
                    'sma_50': float(data.indicators.sma_50) if (hasattr(data, 'indicators') and data.indicators and data.indicators.sma_50) else None,
                } if (hasattr(data, 'indicators') and data.indicators) else {
                    'rsi': None,
                    'macd': None,
                    'macd_signal': None,
                    'sma_20': None,
                    'sma_50': None,
                }
            }
            for data in forex_data
        ]
    }
    
    return JsonResponse(data)


def api_signals(request, pair_id):
    """API endpoint for trading signals"""
    pair = get_object_or_404(ForexPair, id=pair_id)
    
    signals = TradingSignal.objects.filter(pair=pair).order_by('-timestamp')[:50]
    
    data = {
        'pair': pair.symbol,
        'signals': [
            {
                'timestamp': signal.timestamp.isoformat(),
                'type': signal.signal_type,
                'confidence': signal.confidence,
                'price': float(signal.price_at_signal),
                'rsi': signal.rsi_value,
                'greed_level': signal.greed_level,
                'reason': signal.reason,
            }
            for signal in signals
        ]
    }
    
    return JsonResponse(data)


def generate_indicators_for_pair(pair):
    """Generate technical indicators for all data points of a pair"""
    forex_data = ForexData.objects.filter(pair=pair).order_by('timestamp')
    
    if not forex_data.exists():
        return
    
    # Get all prices for calculation
    all_prices = [float(d.close_price) for d in forex_data]
    
    for i, data in enumerate(forex_data):
        # Only calculate indicators if we have enough historical data
        if i < 25:  # Need at least 26 data points for MACD (slow=26)
            continue
        
        # Get prices up to current point
        prices_up_to_now = all_prices[:i+1]
        
        # Calculate indicators
        rsi = TechnicalAnalyzer.calculate_rsi(prices_up_to_now, period=14)
        macd, macd_signal, macd_histogram = TechnicalAnalyzer.calculate_macd(prices_up_to_now)
        sma_20 = TechnicalAnalyzer.calculate_sma(prices_up_to_now, period=20)
        sma_50 = TechnicalAnalyzer.calculate_sma(prices_up_to_now, period=50)
        
        # Save indicators
        indicators, _ = TechnicalIndicators.objects.get_or_create(forex_data=data)
        indicators.rsi = rsi
        indicators.rsi_signal = TechnicalAnalyzer.get_rsi_signal(rsi)
        indicators.macd = macd
        indicators.macd_signal = macd_signal
        indicators.macd_histogram = macd_histogram
        indicators.sma_20 = sma_20
        indicators.sma_50 = sma_50
        indicators.save()


def generate_signals_for_pair(pair):
    """Generate trading signals for a pair"""
    # Get latest data with indicators
    latest_data = ForexData.objects.filter(
        pair=pair,
        indicators__isnull=False
    ).order_by('-timestamp').first()
    
    if not latest_data or not latest_data.indicators:
        return
    
    indicators = latest_data.indicators
    
    # Generate signal
    signal_data = TradingSignalGenerator.generate_signal(
        rsi=indicators.rsi,
        macd_value=indicators.macd,
        macd_signal=indicators.macd_signal,
        sma_20=indicators.sma_20,
        sma_50=indicators.sma_50,
        current_price=latest_data.close_price
    )
    
    # Create trading signal
    greed_level = TechnicalAnalyzer.get_greed_level(indicators.rsi)
    
    TradingSignal.objects.create(
        pair=pair,
        signal_type=signal_data['signal_type'],
        confidence=signal_data['confidence'],
        reason=signal_data['reason'],
        price_at_signal=latest_data.close_price,
        rsi_value=indicators.rsi,
        macd_value=indicators.macd,
        greed_level=greed_level,
    )


@require_http_methods(["GET"])
def create_pair(request):
    """Create a new forex pair to monitor"""
    from_symbol = request.GET.get('from', '').upper()
    to_symbol = request.GET.get('to', '').upper()
    
    if not from_symbol or not to_symbol:
        return JsonResponse({'success': False, 'error': 'Missing currency symbols'}, status=400)
    
    symbol = f"{from_symbol}/{to_symbol}"
    
    try:
        pair, created = ForexPair.objects.get_or_create(
            symbol=symbol,
            defaults={'name': f'{from_symbol} to {to_symbol}'}
        )
        
        if created:
            # Fetch initial data
            client = AlphaVantageClient()
            time_series = client.get_forex_daily(from_symbol, to_symbol)
            
            if time_series:
                parsed_data = AlphaVantageClient.parse_forex_data(time_series)
                
                for data_point in parsed_data:
                    ForexData.objects.create(
                        pair=pair,
                        timestamp=data_point['timestamp'],
                        open_price=data_point['open'],
                        high_price=data_point['high'],
                        low_price=data_point['low'],
                        close_price=data_point['close'],
                    )
                
                generate_indicators_for_pair(pair)
                generate_signals_for_pair(pair)
        
        return JsonResponse({'success': True, 'pair_id': pair.id, 'symbol': pair.symbol})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
