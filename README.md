cat > README.md <<'EOF'
# HiveGrid — Prototype 1: PheroMQ (Stigmergy) Demo

**What it is**  
A tiny, self-contained simulation that demonstrates **HiveGrid’s pheromone-driven (stigmergic) control**.  
A Demand Response (DR) pheromone is emitted at the center of a small honeycomb network. It **evaporates** and **diffuses** to neighbors.  
Each node runs an “Edge Agent” that perceives local intensity and **offers kW** within **Hard Unbreakable Laws (HULs)**, so the **aggregate response** ramps up until the DR target is met.

**Why it matters**  
- Shows HiveGrid’s **swarm behavior** in action (unique differentiator).  
- Demonstrates **safety-first** logic (offers respect HUL bounds).  
- Runs **offline** as a single Python file, easy to fork and extend.

---

## Quickstart

```bash
# 1) (If needed) install matplotlib to enable PNG plot
pip3 install matplotlib
# or on Debian: sudo apt install -y python3-matplotlib

# 2) Run the simulation
python3 prototype1_pheromq_sim.py --steps 20 --target 20

# 3) Optional: save a PNG chart of aggregate response
python3 prototype1_pheromq_sim.py --steps 20 --target 20 --plot
# creates aggregate_offer.png

# 4) Optional: capture console output for your records
python3 prototype1_pheromq_sim.py --steps 20 --target 20 | tee demo_output.txt
