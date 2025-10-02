# Age of Empires II - Multiplayer Network Module

A Python-based real-time strategy game inspired by Age of Empires II with full multiplayer networking support using a hybrid Python-C communication architecture.

## 🎮 Overview

This project implements a complete multiplayer networking solution for an Age of Empires-style RTS game, featuring:

- **Real-time multiplayer gameplay** supporting up to 100 players
- **Hybrid Python-C communication** for high-performance UDP networking
- **Cross-platform compatibility** (Linux, Windows)
- **Advanced game mechanics** including units, buildings, resources, and AI
- **Multiple game modes** and map generation systems
- **Web-based game overview** with HTML reporting

## 🏗️ Architecture

### Core Components

```
main/
├── Game/                     # Core game logic and state management
├── Entity/                   # Game entities (units, buildings, resources)
├── GameField/                # Map generation and game field management
├── ImageProcessingDisplay/   # UI, menus, and rendering
├── AITools/                  # AI systems and pathfinding
├── network/                  # Networking infrastructure
│   ├── packettransport/      # Low-level UDP communication
│   │   ├── python/           # Python networking components
│   │   └── C/                # High-performance C communicators
│   └── QueryProcessing/      # Network message parsing and formatting
├── Projectile/               # Projectile system
└── Sounds/                   # Audio assets
```

### Network Architecture

The networking system uses a **dual-layer architecture**:

1. **Python Layer** (`CythonCommunicator`): High-level game logic and player interaction
2. **C Layer** (`communicator.c`): Low-level UDP packet handling for maximum performance

```
┌─────────────────┐    UDP     ┌─────────────────┐    UDP     ┌─────────────────┐
│   Game Client   │ ◄─────────► │  C Communicator │ ◄─────────► │ Remote Players  │
│   (Python)      │   50000     │      (C)        │   50001+    │                 │
└─────────────────┘             └─────────────────┘             └─────────────────┘
```

## � Getting Started

### Prerequisites

- **Python 3.8+** with pip
- **GCC compiler** for building C components
- **SDL2** development libraries
- **Linux** (recommended) or Windows with WSL

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Network
   ```

2. **Install Python dependencies**
   ```bash
   cd main
   pip install -r requirements.txt
   ```

3. **Build C networking components**
   ```bash
   cd network/packettransport/C
   make clean && make
   ```

4. **Configure system for optimal networking** (Linux only)
   ```bash
   cd ../../../requirments
   sudo ./networkSetup.sh
   ```

### Quick Start

1. **Start the game**
   ```bash
   cd main
   python main.py
   ```

2. **Create a multiplayer game**
   - Select "Create Game" from the main menu
   - Configure map size, mode, and player count
   - Click "Start Game"

3. **Join an existing game**
   - Select "Join Game" from the main menu
   - Choose from available games in the discovery list
   - Click "Join"

## 🎯 Game Features

### Game Modes

- **Lean Mode**: Fast-paced gameplay with reduced resource requirements
- **Mean Mode**: Balanced gameplay with standard resource management
- **Marines Mode**: Military-focused gameplay with enhanced combat

### Map Types

- **Normal Map**: Standard random generation with balanced resources
- **Centered Map**: Resources concentrated in the center for competitive play

### Units & Buildings

#### Units
- **Villagers**: Resource gathering and construction
- **Archers**: Ranged combat units
- **Swordsmen**: Melee infantry
- **Horsemen**: Fast cavalry units

#### Buildings
- **Town Center**: Main base building for villager production
- **Barracks**: Infantry unit production
- **Archery Range**: Archer production
- **Stable**: Cavalry production
- **House**: Population capacity increase
- **Farm**: Food production

#### Resources
- **Gold**: Currency for advanced units and upgrades
- **Wood**: Basic construction material
- **Food**: Unit production and sustenance

## 🌐 Networking Protocol

### Communication Layers

#### Python-C Interface
```python
# Python initiates communication
communicator = CythonCommunicator(python_port=50000, c_port=50001)
communicator.send_packet("A/ae+unit_id:target_id")  # Attack command
```

#### C Network Handler
```c
// C processes and broadcasts
int send_to_all(PlayersTable* players, Communicator* comm, const char* buffer);
```

### Message Format

The game uses a structured query format for all network communications:

```
Header/Function+Arguments
```

**Examples:**
- `A/ae+123:456` - Unit 123 attacks unit 456
- `A/ce+789:101` - Villager 789 collects resource 101
- `A/tu+player:unit_type` - Train unit of type for player

### Network Discovery

The system implements automatic game discovery using UDP broadcasts:

1. **Discovery Request**: `D` - Broadcast to find available games
2. **Discovery Response**: `R/dvrp+seed:cellX:cellY:mode:carte:players` - Game configuration
3. **Join Request**: `Jport` - Request to join game on specific port
4. **Create Request**: `C` - Create new game session

## 🔧 Configuration

### Network Settings

Default ports (configurable in `GLOBAL_VAR.py`):
- **Python Communication**: 50000
- **C Communicator**: 50001-50002
- **Discovery Service**: 10000
- **Game Sessions**: 50003+

### Performance Tuning

The system includes automated network optimization:

```bash
# Increase UDP buffer sizes
net.core.rmem_max = 10485760
net.core.wmem_max = 10485760

# Optimize file descriptors
fs.file-max = 2097152
```

### System Requirements

**Minimum:**
- 4GB RAM
- 1GB available storage
- Network interface with UDP support

**Recommended:**
- 8GB+ RAM for large multiplayer sessions
- SSD storage for faster map loading
- Gigabit Ethernet for optimal performance

## 🎮 Gameplay Features

### Real-Time Strategy Elements

- **Resource Management**: Collect wood, gold, and food
- **Base Building**: Construct and upgrade buildings
- **Unit Production**: Train and command military units
- **Combat System**: Tactical combat with projectiles and formations
- **AI Players**: Sophisticated AI with multiple strategies

### Multiplayer Features

- **Simultaneous Gameplay**: Up to 100 concurrent players
- **Real-time Synchronization**: Sub-second latency for actions
- **Spectator Mode**: Watch ongoing games
- **Game State Persistence**: Save and resume multiplayer sessions

### Advanced Systems

- **Formation System**: Coordinate unit movements
- **Pathfinding**: A* algorithm for optimal unit navigation
- **Fog of War**: Limited visibility system
- **Minimap**: Real-time strategic overview

## 🛠️ Development

### Architecture Patterns

- **Entity-Component System**: Modular game object design
- **Command Pattern**: Network action serialization
- **Observer Pattern**: Game state synchronization
- **Factory Pattern**: Dynamic entity creation

### Code Structure

```python
# Game entities inherit from base Entity class
class Villager(Unit):
    def collect_entity(self, resource_id):
        # Generate network command
        query = NetworkQueryFormatter.format_collect_entity(self.id, resource_id)
        game_state.user.add_query(query, "s")

# Network commands are processed via QueryExecutor
class QueryExecutor:
    def execute_collect_entity(self, actor_id, resource_id):
        # Execute game logic and broadcast to clients
```

### Testing

```bash
# Run stress test with 700 units and 400 buildings
python stress_test.py

# Test network performance
cd network/packettransport/C
./communicator
```

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts**
   ```bash
   # Check port availability
   ss -lun | grep ":50000"
   ```

2. **UDP packet loss**
   ```bash
   # Monitor network statistics
   netstat -su
   ```

3. **Firewall blocking**
   ```bash
   # Allow UDP ports
   sudo ufw allow 50000:50010/udp
   ```

### Performance Optimization

1. **Increase process priority**
   ```bash
   sudo nice -n -10 python main.py
   ```

2. **CPU affinity for C processes**
   ```bash
   taskset -c 0,1 ./communicator
   ```

3. **Monitor system resources**
   ```bash
   htop
   iotop
   ```

## 📊 Game Analytics

The system generates HTML reports for game analysis:

```python
# Auto-generated overview.html includes:
# - Player resources and statistics
# - Real-time team performance
# - Interactive team visibility controls
```

Access the web interface by opening `overview.html` in your browser during gameplay.

## 🤝 Contributing

### �👥 Contributors

| **GitHub Username** | **Name**        |
|----------------------|----------------------|
| `@XpertLambda`         | SAAD Ahmad          |
| `@0xTristo`         | TERRO Ali              |
| `@amer-03`         | EL JIBBAWE Amer        |
| `@Jonasftn`         | FONTAINE-DEMAY Jonas |
| `@ameliesvnt`         | SAUVAN-MAGNET Amélie |
| `@AlexisDan17`         | DANET Alexis |

### Development Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Guidelines:**
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add docstrings for all public functions
- Test multiplayer features with multiple clients

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by Age of Empires II gameplay mechanics
- Uses Pygame for graphics and input handling
- Network architecture inspired by modern game engines
- AI pathfinding based on A* algorithm implementation

---

**Built with ❤️ for the RTS gaming community**

For questions, bug reports, or feature requests, please open an issue on GitHub.
