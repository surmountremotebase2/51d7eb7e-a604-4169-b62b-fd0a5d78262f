from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "MANGO"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # Setting the interval to '1day' for daily RSI calculation.
        return "1day"

    def run(self, data):
        # Thresholds for RSI to trigger buy or sell.
        overbought_threshold = 70
        oversold_threshold = 30
        
        current_rsi = RSI(self.ticker, data["ohlcv"], 14)  # 14-day RSI
        
        if not current_rsi:
            log("RSI calculation failed or data insufficient.")
            return TargetAllocation({})
        
        latest_rsi = current_rsi[-1]  # Get the most recent RSI value
        
        allocation = 0
        
        if latest_rsi < oversold_threshold:
            # If RSI indicates oversold, allocate 100% to buying MANGO.
            log(f"MANGO is oversold with an RSI of {latest_rsi}. Buying.")
            allocation = 1
        elif latest_rsi > overbought_threshold:
            # If RSI indicates overbought, do not buy MANGO.
            log(f"MANGO is overbought with an RSI of {latest_rsi}. Avoiding.")
            allocation = 0
        else:
            # For RSI values in between, maintain or adjust to a neutral stance.
            log(f"MANGO RSI at {latest_rsi}, no action suggested.")
            allocation = 0
        
        return TargetAllocation({self.ticker: allocation})