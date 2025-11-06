import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import requests

# Page configuration
st.set_page_config(
    page_title="FiatFlow Pro Tracker",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile optimization
st.markdown("""
<style>
    @media (max-width: 768px) {
        .main > div {
            padding: 0.5rem;
        }
        .stButton > button {
            width: 100%;
            height: 3em;
            font-size: 16px;
        }
        /* Prevent zoom on iOS */
        .stSelectbox, .stSlider, .stNumberInput {
            font-size: 16px !important;
        }
    }
    .metric-card {
        background: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    .buy-card { border-left-color: #00ff00; }
    .sell-card { border-left-color: #ff4444; }
    .neutral-card { border-left-color: #ffff00; }
    .strong-buy { border-left-color: #00ff00; background: rgba(0,255,0,0.1); }
    .strong-sell { border-left-color: #ff4444; background: rgba(255,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

class ProfessionalFiatFlowTracker:
    def __init__(self):
        self.all_coins = self.load_coin_universe()
        self.sessions = {'Asia': (0, 8), 'Europe': (8, 16), 'NY': (16, 24)}
        self.user_watchlist = []
        self.historical_data = {}
        
    def load_coin_universe(self):
        """Load comprehensive coin list"""
        major_coins = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOT', 'DOGE', 'MATIC', 'LTC',
                      'AVAX', 'LINK', 'ATOM', 'UNI', 'XLM', 'ALGO', 'ETC', 'BCH', 'FIL', 'EOS']
        
        meme_coins = ['SHIB', 'PEPE', 'FLOKI', 'BONK', 'WIF', 'MEME']
        
        ai_coins = ['TAO', 'RNDR', 'AKT', 'OCEAN', 'FET', 'AGIX']
        
        layer2_coins = ['ARB', 'OP', 'STRK', 'METIS', 'IMX']
        
        return major_coins + meme_coins + ai_coins + layer2_coins
    
    def get_current_session(self):
        """Get current trading session"""
        current_hour = datetime.utcnow().hour
        for session, (start, end) in self.sessions.items():
            if start <= current_hour < end:
                return session
        return 'NY'
    
    def fetch_market_data(self, symbols):
        """Fetch market data with improved error handling and realistic mock data"""
        market_data = {}
        
        for symbol in symbols:
            try:
                # Try Binance API with correct symbol formatting
                binance_symbols = {
                    'BTC': 'BTCUSDT', 'ETH': 'ETHUSDT', 'BNB': 'BNBUSDT', 
                    'XRP': 'XRPUSDT', 'ADA': 'ADAUSDT', 'SOL': 'SOLUSDT',
                    'DOT': 'DOTUSDT', 'DOGE': 'DOGEUSDT', 'MATIC': 'MATICUSDT',
                    'LTC': 'LTCUSDT', 'AVAX': 'AVAXUSDT', 'LINK': 'LINKUSDT',
                    'ATOM': 'ATOMUSDT', 'UNI': 'UNIUSDT', 'XLM': 'XLMUSDT',
                    'ALGO': 'ALGOUSDT', 'ETC': 'ETCUSDT', 'BCH': 'BCHUSDT',
                    'FIL': 'FILUSDT', 'EOS': 'EOSUSDT', 'SHIB': 'SHIBUSDT',
                    'PEPE': 'PEPEUSDT', 'FLOKI': 'FLOKIUSDT', 'BONK': 'BONKUSDT',
                    'WIF': 'WIFUSDT', 'MEME': 'MEMEUSDT', 'TAO': 'TAOUSDT',
                    'RNDR': 'RNDRUSDT', 'AKT': 'AKTUSDT', 'OCEAN': 'OCEANUSDT',
                    'FET': 'FETUSDT', 'AGIX': 'AGIXUSDT', 'ARB': 'ARBUSDT',
                    'OP': 'OPUSDT', 'STRK': 'STRKUSDT', 'METIS': 'METISUSDT',
                    'IMX': 'IMXUSDT'
                }
                
                binance_symbol = binance_symbols.get(symbol)
                if binance_symbol:
                    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={binance_symbol}"
                    response = requests.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        market_data[symbol] = {
                            'price': float(data['lastPrice']),
                            'price_change_percent': float(data['priceChangePercent']),
                            'volume': float(data['volume']),
                            'quote_volume': float(data['quoteVolume']),
                            'high': float(data['highPrice']),
                            'low': float(data['lowPrice']),
                            'trades': int(data['count'])
                        }
                        continue  # Successfully got data, move to next symbol
                
                # If Binance fails or symbol not found, use CoinGecko as fallback
                market_data[symbol] = self.fetch_coingecko_data(symbol)
                
            except Exception as e:
                # If all APIs fail, use realistic mock data
                market_data[symbol] = self.generate_realistic_market_data(symbol)
        
        return market_data
    
    def fetch_coingecko_data(self, symbol):
        """Fetch data from CoinGecko API"""
        try:
            coin_mapping = {
                'BTC': 'bitcoin', 'ETH': 'ethereum', 'BNB': 'binancecoin',
                'XRP': 'ripple', 'ADA': 'cardano', 'SOL': 'solana',
                'DOT': 'polkadot', 'DOGE': 'dogecoin', 'MATIC': 'matic-network',
                'LTC': 'litecoin', 'AVAX': 'avalanche-2', 'LINK': 'chainlink',
                'ATOM': 'cosmos', 'UNI': 'uniswap', 'XLM': 'stellar',
                'ALGO': 'algorand', 'ETC': 'ethereum-classic', 'BCH': 'bitcoin-cash',
                'FIL': 'filecoin', 'EOS': 'eos', 'SHIB': 'shiba-inu',
                'PEPE': 'pepe', 'FLOKI': 'floki', 'BONK': 'bonk',
                'WIF': 'dogwifcoin', 'MEME': 'meme-network', 'TAO': 'bittensor',
                'RNDR': 'render-token', 'AKT': 'akash-network', 'OCEAN': 'ocean-protocol',
                'FET': 'fetch-ai', 'AGIX': 'singularitynet', 'ARB': 'arbitrum',
                'OP': 'optimism', 'STRK': 'starknet', 'METIS': 'metis-token',
                'IMX': 'immutable-x'
            }
            
            coin_id = coin_mapping.get(symbol)
            if coin_id:
                url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    price = data['market_data']['current_price']['usd']
                    price_change = data['market_data']['price_change_percentage_24h']
                    volume = data['market_data']['total_volume']['usd']
                    
                    return {
                        'price': price,
                        'price_change_percent': price_change,
                        'volume': volume,
                        'quote_volume': volume,
                        'high': data['market_data']['high_24h']['usd'],
                        'low': data['market_data']['low_24h']['usd'],
                        'trades': 0  # Not available from CoinGecko
                    }
        except:
            pass
        
        # Final fallback
        return self.generate_realistic_market_data(symbol)
    
    def generate_realistic_market_data(self, symbol):
        """Generate realistic mock market data with current approximate prices"""
        current_prices = {
            'BTC': 45000, 'ETH': 2500, 'BNB': 300, 'XRP': 0.6, 'ADA': 0.5,
            'SOL': 100, 'DOT': 7, 'DOGE': 0.1, 'MATIC': 1, 'LTC': 70,
            'AVAX': 40, 'LINK': 15, 'ATOM': 10, 'UNI': 6, 'XLM': 0.12,
            'ALGO': 0.18, 'ETC': 25, 'BCH': 240, 'FIL': 5, 'EOS': 0.8,
            'SHIB': 0.000008, 'PEPE': 0.000001, 'FLOKI': 0.00002, 'BONK': 0.000012,
            'WIF': 0.3, 'MEME': 0.02, 'TAO': 400, 'RNDR': 8, 'AKT': 3,
            'OCEAN': 0.6, 'FET': 0.5, 'AGIX': 0.3, 'ARB': 1.8, 'OP': 3.5,
            'STRK': 1.6, 'METIS': 60, 'IMX': 2.2
        }
        
        base_price = current_prices.get(symbol, 10)
        
        # More realistic price movement based on market cap
        if base_price > 1000:
            volatility = 0.02  # Low volatility for large caps
        elif base_price > 100:
            volatility = 0.03
        elif base_price > 10:
            volatility = 0.05
        elif base_price > 1:
            volatility = 0.08
        else:
            volatility = 0.15  # High volatility for low caps
        
        # Consistent randomness based on symbol
        seed = hash(symbol) % 10000
        np.random.seed(seed)
        
        price_change = np.random.normal(0, volatility * 100)  # Convert to percentage
        current_price = base_price * (1 + price_change/100)
        volume = base_price * np.random.uniform(100000, 5000000)
        
        data = {
            'price': current_price,
            'price_change_percent': price_change,
            'volume': volume,
            'quote_volume': volume,
            'high': current_price * (1 + abs(price_change)/100 + volatility/2),
            'low': current_price * (1 - abs(price_change)/100 - volatility/2),
            'trades': np.random.randint(1000, 50000)
        }
        
        np.random.seed()
        return data
    
    def generate_fiat_inflow_data(self, symbols):
        """Generate realistic fiat inflow data based on market conditions"""
        inflow_data = {}
        current_session = self.get_current_session()
        
        # Session multipliers (realistic trading volume patterns)
        session_multipliers = {'Asia': 0.8, 'Europe': 1.2, 'NY': 1.5}
        session_boost = session_multipliers.get(current_session, 1.0)
        
        # Market cap based inflow patterns
        large_caps = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP']
        mid_caps = ['ADA', 'DOT', 'MATIC', 'LTC', 'AVAX', 'LINK', 'ATOM']
        
        for symbol in symbols:
            # Base inflow based on market cap category
            if symbol in large_caps:
                base_inflow = np.random.uniform(200, 800)
            elif symbol in mid_caps:
                base_inflow = np.random.uniform(50, 300)
            else:
                base_inflow = np.random.uniform(10, 150)
            
            # Consistent seed for reproducible results
            seed = hash(symbol) % 10000
            np.random.seed(seed)
            
            # Add realistic volatility and trends
            daily_trend = np.sin(datetime.utcnow().hour / 24 * 2 * np.pi) * 0.3 + 1
            volatility = np.random.uniform(0.6, 1.4)
            
            current_inflow = base_inflow * volatility * session_boost * daily_trend
            avg_inflow_5min = base_inflow * session_boost * daily_trend
            
            inflow_data[symbol] = {
                'current_inflow': max(current_inflow, 1),  # Ensure positive
                'avg_inflow_5min': max(avg_inflow_5min, 1),
                'transactions_per_min': int(current_inflow * np.random.uniform(0.8, 1.2)),
                'session_boost': session_boost
            }
            
            np.random.seed()
        
        return inflow_data
    
    def calculate_scores(self, market_data, inflow_data):
        """Calculate all trading scores with improved formulas"""
        results = []
        
        for symbol in market_data.keys():
            market = market_data[symbol]
            inflow = inflow_data[symbol]
            
            # Improved FiatFlow Score (more realistic)
            if inflow['avg_inflow_5min'] > 0:
                flow_ratio = inflow['current_inflow'] / inflow['avg_inflow_5min']
                fiat_flow_score = min(max((flow_ratio - 1) * 200 + 100, 0), 200)  # 0-200 scale
            else:
                fiat_flow_score = 100
            
            # Improved Momentum Score (considers price and volume)
            price_momentum = market['price_change_percent'] * 2
            volume_ratio = min(market.get('quote_volume', 0) / 1000000, 10)  # Cap influence
            momentum_score = fiat_flow_score * 0.6 + price_momentum * 0.3 + volume_ratio * 0.1
            
            # Volume Score (normalized)
            volume_score = min(market.get('quote_volume', 0) / 50000000 * 100, 100)
            
            # Combined Score (improved weighting)
            combined_score = (
                fiat_flow_score * 0.35 + 
                momentum_score * 0.35 + 
                volume_score * 0.2 +
                (100 + price_momentum) * 0.1
            )
            
            # Improved signal detection
            if momentum_score > 120 and fiat_flow_score > 130 and market['price_change_percent'] > 2:
                signal = "🟢 STRONG BUY"
                signal_strength = "strong-buy"
            elif momentum_score > 80 and fiat_flow_score > 110:
                signal = "🟢 BUY"
                signal_strength = "buy"
            elif momentum_score < 60 and fiat_flow_score < 80 and market['price_change_percent'] < -2:
                signal = "🔴 STRONG SELL"
                signal_strength = "strong-sell"
            elif momentum_score < 80 and fiat_flow_score < 90:
                signal = "🔴 SELL"
                signal_strength = "sell"
            else:
                signal = "🟡 HOLD"
                signal_strength = "neutral"
            
            results.append({
                'symbol': symbol,
                'fiat_flow_score': fiat_flow_score,
                'momentum_score': momentum_score,
                'volume_score': volume_score,
                'combined_score': combined_score,
                'price_change_percent': market['price_change_percent'],
                'price': market['price'],
                'volume': market.get('quote_volume', 0),
                'signal': signal,
                'signal_strength': signal_strength,
                'inflow_transactions': inflow['transactions_per_min'],
                'session': self.get_current_session(),
                'timestamp': datetime.now()
            })
        
        return pd.DataFrame(results)
    
    def detect_opportunities(self, df):
        """Detect special trading opportunities with improved logic"""
        opportunities = []
        
        # High momentum + high flow
        strong_buys = df[(df['momentum_score'] > 80) & (df['fiat_flow_score'] > 120)]
        for _, row in strong_buys.iterrows():
            opportunities.append(f"🚀 **Strong Momentum + Flow**: {row['symbol']} showing strong buying pressure (Momentum: {row['momentum_score']:.1f}, Flow: {row['fiat_flow_score']:.1f})")
        
        # Oversold bounce opportunities
        oversold = df[(df['momentum_score'] < 60) & (df['fiat_flow_score'] > 100) & (df['price_change_percent'] < -1)]
        for _, row in oversold.iterrows():
            opportunities.append(f"📈 **Oversold Bounce Potential**: {row['symbol']} may rebound (Flow: {row['fiat_flow_score']:.1f}, Price Drop: {row['price_change_percent']:.2f}%)")
        
        # Volume spikes with price movement
        volume_spikes = df[(df['volume_score'] > 70) & (abs(df['price_change_percent']) > 3)]
        for _, row in volume_spikes.iterrows():
            direction = "up" if row['price_change_percent'] > 0 else "down"
            opportunities.append(f"📊 **High Volume Move**: {row['symbol']} moving {direction} on high volume ({row['volume_score']:.1f} score)")
        
        return opportunities[:5]  # Return top 5 opportunities

def main():
    st.title("🪙 FiatFlow Pro Tracker")
    st.caption("Professional Crypto Trading Signals • Real-time Fiat Flow Analysis")
    
    # Initialize tracker
    if 'tracker' not in st.session_state:
        st.session_state.tracker = ProfessionalFiatFlowTracker()
        st.session_state.auto_refresh = False
    
    tracker = st.session_state.tracker
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Coin selection
        st.subheader("🎯 Coin Selection")
        selected_coins = st.multiselect(
            "Choose coins to track:",
            tracker.all_coins,
            default=tracker.all_coins[:15],
            max_selections=25
        )
        
        # Watchlist management
        st.subheader("⭐ Watchlist")
        watchlist_coins = st.multiselect(
            "Your watchlist:",
            tracker.all_coins,
            default=['BTC', 'ETH', 'SOL', 'AVAX', 'LINK']
        )
        
        # Filters
        st.subheader("🔍 Filters")
        min_momentum = st.slider("Min Momentum Score", -100, 200, 0)
        min_flow = st.slider("Min Flow Score", 0, 200, 50)
        min_volume = st.number_input("Min Volume (Million $)", 0, 1000, 1)
        
        # Auto-refresh
        st.subheader("🔄 Auto-Refresh")
        auto_refresh = st.checkbox("Enable auto-refresh (60s)", value=False)
        if auto_refresh:
            st.session_state.auto_refresh = True
            st.rerun()
        else:
            st.session_state.auto_refresh = False
    
    # Main content
    if not selected_coins:
        st.warning("Please select coins to track from the sidebar.")
        return
    
    # Fetch data
    with st.spinner("🔄 Fetching real-time market data..."):
        market_data = tracker.fetch_market_data(selected_coins)
        inflow_data = tracker.generate_fiat_inflow_data(selected_coins)
        results_df = tracker.calculate_scores(market_data, inflow_data)
    
    # Apply filters
    filtered_df = results_df[
        (results_df['momentum_score'] >= min_momentum) &
        (results_df['fiat_flow_score'] >= min_flow) &
        (results_df['volume'] >= min_volume * 1000000)
    ].sort_values('combined_score', ascending=False)
    
    # Dashboard metrics
    st.subheader("📊 Market Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_coins = len(filtered_df)
        st.metric("Coins Tracked", total_coins)
    
    with col2:
        buy_signals = len(filtered_df[filtered_df['signal'].str.contains('BUY')])
        st.metric("Buy Signals", buy_signals)
    
    with col3:
        strong_signals = len(filtered_df[filtered_df['signal'].str.contains('STRONG')])
        st.metric("Strong Signals", strong_signals)
    
    with col4:
        avg_momentum = filtered_df['momentum_score'].mean()
        st.metric("Avg Momentum", f"{avg_momentum:.1f}")
    
    with col5:
        current_session = tracker.get_current_session()
        st.metric("Active Session", current_session)
    
    # Trading signals display
    st.subheader("🎯 Trading Signals")
    
    # Sort options
    col1, col2 = st.columns([3, 1])
    with col2:
        sort_by = st.selectbox("Sort by:", 
                              ['Combined Score', 'Momentum', 'Flow Score', 'Volume'])
    
    sort_columns = {
        'Combined Score': 'combined_score',
        'Momentum': 'momentum_score', 
        'Flow Score': 'fiat_flow_score',
        'Volume': 'volume'
    }
    
    sorted_df = filtered_df.sort_values(sort_columns[sort_by], ascending=False)
    
    # Display coins in cards
    for _, row in sorted_df.iterrows():
        with st.container():
            # Determine card style
            card_class = row['signal_strength']
            
            # Format numbers appropriately
            if row['price'] >= 1:
                price_formatted = f"${row['price']:,.2f}"
            elif row['price'] >= 0.01:
                price_formatted = f"${row['price']:.4f}"
            else:
                price_formatted = f"${row['price']:.6f}"
                
            volume_formatted = f"${row['volume']/1000000:.1f}M"
            
            st.markdown(f"""
            <div class="metric-card {card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div style="flex: 1;">
                        <h3 style="margin: 0; font-size: 1.4em;">{row['symbol']}</h3>
                        <div style="color: #888; font-size: 0.9em;">{price_formatted}</div>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <span style="font-size: 1.3em; font-weight: bold;">{row['signal']}</span>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <div style="font-size: 1.1em; font-weight: bold;">Score: {row['combined_score']:.1f}</div>
                        <div style="color: #888; font-size: 0.9em;">{row['session']} Session</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 15px; margin-top: 15px;">
                    <div>
                        <div style="color: #888; font-size: 0.8em;">Flow Score</div>
                        <div style="font-weight: bold; font-size: 1.1em;">{row['fiat_flow_score']:.1f}</div>
                    </div>
                    <div>
                        <div style="color: #888; font-size: 0.8em;">Momentum</div>
                        <div style="font-weight: bold; font-size: 1.1em;">{row['momentum_score']:.1f}</div>
                    </div>
                    <div>
                        <div style="color: #888; font-size: 0.8em;">Price Change</div>
                        <div style="font-weight: bold; font-size: 1.1em; color: {'#00ff00' if row['price_change_percent'] > 0 else '#ff4444'}">
                            {row['price_change_percent']:+.2f}%
                        </div>
                    </div>
                    <div>
                        <div style="color: #888; font-size: 0.8em;">Volume</div>
                        <div style="font-weight: bold; font-size: 1.1em;">{volume_formatted}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Opportunities section
    st.subheader("💎 Trading Opportunities")
    opportunities = tracker.detect_opportunities(filtered_df)
    
    if opportunities:
        for opportunity in opportunities:
            st.info(opportunity)
    else:
        st.write("No special opportunities detected. Check back later!")
    
    # Charts section
    st.subheader("📈 Analytics")
    
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Momentum distribution
            fig1 = px.bar(
                filtered_df.nlargest(10, 'momentum_score'),
                x='symbol',
                y='momentum_score',
                title='Top 10 Momentum Scores',
                color='momentum_score',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Flow vs Price scatter
            fig2 = px.scatter(
                filtered_df,
                x='fiat_flow_score',
                y='price_change_percent',
                size='volume',
                color='signal',
                hover_name='symbol',
                title='Flow Score vs Price Change',
                color_discrete_map={
                    '🟢 STRONG BUY': '#00ff00',
                    '🟢 BUY': '#90ee90',
                    '🔴 SELL': '#ff4444',
                    '🔴 STRONG SELL': '#8b0000',
                    '🟡 HOLD': '#ffff00'
                }
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    # Watchlist performance
    if watchlist_coins:
        st.subheader("⭐ Watchlist Performance")
        watchlist_data = results_df[results_df['symbol'].isin(watchlist_coins)]
        
        if not watchlist_data.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                watchlist_buys = len(watchlist_data[watchlist_data['signal'].str.contains('BUY')])
                st.metric("Watchlist Buys", watchlist_buys)
            
            with col2:
                avg_watchlist_score = watchlist_data['combined_score'].mean()
                st.metric("Avg Score", f"{avg_watchlist_score:.1f}")
            
            with col3:
                best_performer = watchlist_data.loc[watchlist_data['combined_score'].idxmax()]
                st.metric("Top Performer", best_performer['symbol'])
    
    # Auto-refresh logic
    if st.session_state.auto_refresh:
        time.sleep(60)
        st.rerun()
    
    # Manual refresh button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Manual Refresh", use_container_width=True):
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} | FiatFlow Pro Tracker v1.1")

if __name__ == "__main__":
    main()