# google vs QQQ index strategy

def initialize(context):
    set_benchmark(symbol('QQQ'))
    context.google = sid(26578)

    schedule_function(simple_ma_strat, 
                      date_rules.every_day(),
                      time_rules.market_open(hours=1))

def simple_ma_strat(context, data):
    hist = data.history(
        context.google, 
        fields= 'price', 
        bar_count=50, 
        frequency='1d'
    )
   
    log.info(hist.head())
    sma_50 = hist.mean()
    sma_20 = hist[-20:].mean()
 
    open_orders = get_open_orders()
 
    if sma_20 > sma_50:
        if context.google not in open_orders:
            order_target_percent(context.google, 1.0)
   
    elif sma_50 > sma_20: 
        if context.google not in open_orders:
            order_target_percent(context.google, -1.0)
  
    record(leverage = context.account.leverage)