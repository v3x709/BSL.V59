# BSL.v59 Python Server
A rebuild of the BSL.v59 server in Python, optimized for Termux.

## Features
- Full Python rebuild from C#
- SQLite database for persistence
- Custom Trophy (80-350) and Ranked Point (200-900+) rewards
- Shelly starter brawler
- Shop welcome reward
- Simulated battle system
- Termux compatible (non-root)

## Installation in Termux

We use `pysodium` to avoid compilation issues in Termux. It requires the system `libsodium` package.

1. **Update and install build essentials:**
   ```bash
   pkg update
   pkg install python libsodium
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

## Customization
- **Database**: The server uses `server.db`. You can inspect it using any SQLite viewer.
- **Rewards**: Trophy and Ranked point gains can be adjusted in `logic/player.py`.

## Credits
Original C# server by LkPrtctrd.
Python rebuild by Jules.
