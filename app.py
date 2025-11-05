import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Mobile-optimized config
st.set_page_config(
    page_title="FiatFlow Mobile",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Mobile CSS
st.markdown("""
<style>
    /* Mobile optimization */
    @media (max-width: 768px) {
        .main > div {
            padding: 0.5rem;
        }
        .stButton > button {
            width: 100%;
            height: 3em;
        }
        /* Larger touch targets */
        .stSelectbox div[data-baseweb="select"] {
            min-height: 3em;
        }
    }
    .coin-card {
        background: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    .buy-card { border-left-color: #00ff00; }
    .sell-card { border-left-color: #ff4444; }
    .neutral-card { border-left-color: #ffff00; }
</style>
""", unsafe_allow_html=True)

class MobileTracker:
    def __init__(self):
        self.coins = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOGE', 'MATIC', 'DOT', 'LTC']
    
    def generate_data(self):
        data = []
        for coin in self.coins:
            price_change = np.random.uniform(-8, 8)
            flow_score = np.random.uniform(50, 200)
            momentum = flow_score + (price_change * 10)
            
            if momentum > 50:
                signal = "🟢 BUY"
                card_class = "buy-card"
            elif momentum < -30:
                signal = "🔴 SELL" 
                card_class = "sell-card"
            else:
                signal = "🟡 HOLD"
                card_class = "neutral-card"
                
            data.append({
                'coin': coin,
                'price_change': price_change,
                'flow_score': flow_score,
                'momentum': momentum,
                'signal': signal,
                'card_class': card_class,
                'volume': np.random.uniform(1000000, 50000000)
            })
        return data

def main():
    st.title("🪙 FiatFlow Tracker")
    st.caption("Mobile-Optimized Crypto Signals")
    
    tracker = MobileTracker()
    
    # Simple controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("📊 Show Charts", use_container_width=True):
            st.session_state.show_charts = True
    
    # Generate and display data
    data = tracker.generate_data()
    
    for coin_data in data:
        with st.container():
            st.markdown(f"""
            <div class="coin-card {coin_data['card_class']}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0;">{coin_data['coin']}</h3>
                    <span style="font-size: 1.2em; font-weight: bold;">{coin_data['signal']}</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                    <div>Flow: <b>{coin_data['flow_score']:.0f}%</b></div>
                    <div>Momentum: <b>{coin_data['momentum']:.1f}</b></div>
                    <div>Price: <b>{coin_data['price_change']:+.2f}%</b></div>
                    <div>Volume: <b>${coin_data['volume']/1000000:.1f}M</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Simple alerts
    st.subheader("🚨 Alerts")
    strong_buys = [d for d in data if d['momentum'] > 70]
    strong_sells = [d for d in data if d['momentum'] < -40]
    
    for coin in strong_buys[:3]:
        st.success(f"🔥 {coin['coin']}: Strong Buy (Momentum: {coin['momentum']:.1f})")
    
    for coin in strong_sells[:3]:
        st.error(f"⚠️ {coin['coin']}: Strong Sell (Momentum: {coin['momentum']:.1f})")
    
    # Session info
    st.markdown("---")
    st.caption(f"Last update: {datetime.now().strftime('%H:%M:%S')} | Mobile Optimized")

if __name__ == "__main__":
    main()
