#!/usr/bin/env python3
"""
HiveGrid Prototype #1: PheroMQ (stigmergy) simulation
- In-memory pheromone "bus" with evaporation + diffusion on a tiny honeycomb graph
- Agents perceive local DR pheromone and offer kW within HUL bounds
- Console ASCII snapshot; optional matplotlib plot if available

Run:
  python prototype1_pheromq_sim.py --steps 20 --target 20

Optional:
  python prototype1_pheromq_sim.py --plot
"""
from __future__ import annotations
import math, random, argparse, time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# ---------- Graph ----------
def honeycomb7():
    # center 0; ring 1..6 with cyclic adjacency and each connected to center
    adj = {i: [] for i in range(7)}
    for i in range(1,7):
        adj[0].append(i); adj[i].append(0)
    ring = [1,2,3,4,5,6]
    for idx,i in enumerate(ring):
        j = ring[(idx+1)%6]
        adj[i].append(j); adj[j].append(i)
    return adj

# ---------- Domain ----------
@dataclass
class Agent:
    node: int
    name: str
    max_shed_kw: float
    base_load_kw: float
    offered_kw: float = 0.0

    def perceive_and_offer(self, dr_intensity: float) -> float:
        # intensity -> fraction via tanh (smooth saturation)
        fraction = math.tanh(1.5 * dr_intensity)  # ~0..1
        desired = fraction * self.max_shed_kw
        # HUL: 0 <= offer <= max_shed_kw
        self.offered_kw = max(0.0, min(self.max_shed_kw, desired))
        return self.offered_kw

@dataclass
class World:
    N: int
    adj: Dict[int, List[int]]
    evap: float = 0.82
    diff: float = 0.35
    field: Dict[Tuple[int, str], float] = field(default_factory=dict)

    def step(self):
        # Evaporation
        for key in list(self.field.keys()):
            self.field[key] *= self.evap
            if self.field[key] < 1e-4:
                del self.field[key]
        # Diffusion
        increments: Dict[Tuple[int,str], float] = {}
        for (i, typ), inten in self.field.items():
            neigh = self.adj.get(i, [])
            if not neigh: continue
            share = (self.diff * inten) / len(neigh)
            for j in neigh:
                increments[(j, typ)] = increments.get((j, typ), 0.0) + share
        for key, val in increments.items():
            self.field[key] = self.field.get(key, 0.0) + val

# ---------- Viz helpers ----------
def ascii_snapshot(field: Dict[Tuple[int,str], float], offers: List[float]) -> str:
    lines=[]
    for i in range(7):
        inten = field.get((i,'DR'),0.0)
        bar = "#"*int(max(0,min(10, inten*10)))
        lines.append(f"Node {i:1d} I={inten:0.2f} |{bar:<10}| offer={offers[i]:0.2f} kW")
    return "\n".join(lines)

def maybe_plot(history, show=False, save_path=None):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return False
    steps = [t for t, total, offers, field in history]
    totals = [total for t,total,_,_ in history]
    plt.figure()
    plt.plot(steps, totals, marker="o")
    plt.xlabel("step"); plt.ylabel("total offered kW"); plt.title("Aggregate DR response vs time")
    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    if show:
        plt.show()
    plt.close()
    return True

# ---------- Simulation ----------
def run_sim(agents: List[Agent], world: World, steps:int, target_kw:float):
    history=[]
    for t in range(steps):
        offers=[]
        for ag in agents:
            inten = world.field.get((ag.node,'DR'), 0.0)
            offers.append(ag.perceive_and_offer(inten))
        total = sum(offers)
        history.append((t,total,offers[:],dict(world.field)))
        print(f"\n--- step {t} total_offer={total:0.2f} kW ---")
        print(ascii_snapshot(world.field, offers))
        if total >= target_kw:
            print(f"Target {target_kw} kW met at step {t} ✅")
            break
        world.step()
    return history

def main():
    ap = argparse.ArgumentParser(description="HiveGrid Prototype #1: PheroMQ simulation")
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--target", type=float, default=20.0)
    ap.add_argument("--evap", type=float, default=0.82)
    ap.add_argument("--diff", type=float, default=0.35)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--plot", action="store_true", help="save plot PNG")
    args = ap.parse_args()

    random.seed(args.seed)

    adj = honeycomb7()
    world = World(7, adj, evap=args.evap, diff=args.diff)
    world.field[(0,'DR')] = 1.0  # seed a DR pheromone at center

    # agents with reproducible capacities
    agents=[]
    rng=random.Random(args.seed)
    for i in range(7):
        base = rng.uniform(8,15)
        maxshed = rng.uniform(3,8)
        agents.append(Agent(i, f"A{i}", max_shed_kw=maxshed, base_load_kw=base))


    print("Starting PheroMQ DR diffusion demo (honeycomb-7)...")
    print(f"evap={args.evap} diff={args.diff} target={args.target} kW")

    hist = run_sim(agents, world, args.steps, args.target)

    if args.plot:
        ok = maybe_plot(hist, show=False, save_path="aggregate_offer.png")
        if ok:
            print("Saved plot: aggregate_offer.png")
        else:
            print("matplotlib not available; skipping plot")

    print("\nDone.")

if __name__ == "__main__":
    main()
