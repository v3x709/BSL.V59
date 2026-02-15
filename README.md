# BSL.v59 Modern Python Server
A complex and modern rebuild of the BSL.v59 private server in Python for Termux.

## Features
- Full accurately ported protocol (Lobby + Login)
- Real-time UDP Battle Server skeleton with simulation loop
- SQLite Database for full persistence
- Complex Ranked System: Random 200-900+ points per win
- Modded Rewards: High trophy gains (80-350) and Shop Welcome Reward (99k gems)
- Termux Optimized: Uses `pysodium` to avoid build errors.

## Installation
1. `pkg update && pkg install python libsodium`
2. `pip install pysodium`
3. `chmod +x start.sh`
4. `./start.sh`

## Credits
LkPrtctrd for the original C# server.
Jules for the Modern Python rebuild.
