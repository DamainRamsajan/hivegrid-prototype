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

## HiveMind Architecture Diagrams

Below are the generic HiveMind diagrams (auto-generated, labeled sequentially):

HiveMind Architecture Diagrams
Below are the generic HiveMind diagrams (auto-generated, labeled sequentially):

Diagram 1
https://./diagrams/deepseek_mermaid_20250915_f04452.png

Diagram 2
https://./diagrams/deepseek_mermaid_20250915_cda544.png

Diagram 3
https://./diagrams/deepseek_mermaid_20250915_bf3425.png

Diagram 4
https://./diagrams/deepseek_mermaid_20250915_b0415f.png

Diagram 5
https://./diagrams/deepseek_mermaid_20250915_b2f547.png

Diagram 6
https://./diagrams/deepseek_mermaid_20250915_0e5bab.png

Diagram 7
https://./diagrams/deepseek_mermaid_20250915_1ecf8d.png

Diagram 8
https://./diagrams/deepseek_mermaid_20250915_2eb1d3.png

Diagram 9
https://./diagrams/deepseek_mermaid_20250915_9a1dc2.png

Diagram 10
https://./diagrams/deepseek_mermaid_20250915_9ff779.png

Diagram 11
https://./diagrams/deepseek_mermaid_20250915_10ad19.png

Diagram 12
https://./diagrams/deepseek_mermaid_20250915_47c76b.png

Diagram 13
https://./diagrams/deepseek_mermaid_20250915_52ffbb.png