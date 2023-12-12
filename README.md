## Trading Bot Documentation

### Overview

This Python script is a basic trading bot that interacts with the Binance API to perform buy and sell actions for a given trading pair (in this case, "LUNAUSDT"). The bot uses moving average strategies to determine buy and sell signals based on historical price data retrieved from Binance.

### Dependencies

- `numpy` library: Used for numerical computations.
- `binance` library: Allows interaction with the Binance API.
- `config`: Contains API key and secret for Binance authentication.
- `time`, `datetime`: For time-related functionalities.
- `os`: For interacting with the operating system.

### Initialization

- **Parameters**:
    - `n`: Defines the period for moving average calculations (default: 60).
    - `folder`: Specifies the directory where historical data files are stored.
    - `pair`: Defines the trading pair to be used (default: "LUNAUSDT").
    - `data`: Holds information about available funds for trading (initially set as `[0, 100]`).
    - `nb` and `ns`: Parameters for the moving average strategy indicating buy and sell signals respectively.
    - `client`: Binance client object initialized with API key and secret.

### Functions

#### 1. `get_online_data(s, t)`

- **Description**: Generates online price data for the given symbol at specified intervals.
- **Parameters**:
    - `s`: Symbol for which the price data is fetched.
    - `t`: Time interval in seconds for data fetching.
- **Returns**: Yields live price data.

#### 2. `get_data(folder)`

- **Description**: Generates historical data from the specified folder.
- **Parameters**:
    - `folder`: Directory where historical data files are stored.
- **Returns**: Yields historical data.

#### 3. `buy(data, p, c)` and `sel(data, p, c)`

- **Description**: Simulates buying and selling actions with given parameters.
- **Parameters**:
    - `data`: Holds available funds and stock amounts.
    - `p`: Price at which the action is performed.
    - `c`: Quantity or count of the asset to be bought/sold.
- **Returns**: Updated `data` after buying/selling.

#### 4. `avg(n, prices)` and `mavg_strategy(data, g, nb, ns, history)`

- **Description**: Implements a moving average strategy for trading.
- **Parameters**:
    - `n`: Period for moving average calculations.
    - `prices`: Price history used for calculation.
    - `data`: Holds available funds and stock amounts.
    - `g`: Online data generator.
    - `nb` and `ns`: Parameters for buy and sell signals.
    - `history`: Historical price data.
- **Returns**: None.

### Execution

The script starts by initializing necessary parameters and fetching historical price data. It then executes the moving average strategy (`mavg_strategy`) using online price data (`g`) to simulate buying and selling actions based on calculated signals.

Note: Some sections of the code (marked within triple quotes) provide alternative functions for buying and selling actions using Binance API. They are commented out but can be used by uncommenting these blocks and commenting the previous versions of `buy()` and `sel()` functions.
