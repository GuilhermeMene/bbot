## Binance Bot

### A Python Bot for Spot Trading on the Binance exchange

The concept was fundamentally designed based on conventional signals and, later, using a machine learning model.

The main signals used in the bot machine learning models are:
1. Simple Moving Average (5, 10, 20, and 50 periods);
2. Relative Strength Index;
3. Bollinger Bands;
4. Moving Average Convergence Divergence;
5. Sthocastic Oscillator;
6. Fibonacci Retracement;
7. Average Directional Index;
8. Awesome Oscillator;
9. Average True Range;
10. On-balance Volume (OBV).

The indicators used directly in the bot are:
1. Simple Moving Average 5 cross SMA 10;
2. Simple Moving Average 5 cross SMA 20;
3. Bollinger Bands;
4. Stochastic Oscillator;
5. Relative Strength Index;
6. Awesome Oscillator.

The machine learning models were created using Decision Forests algorithms:
1. Gradient Boosting and;
2. Histogram-Based Gradient Boosting.

Desision Forests were created using Scikit-learn.
