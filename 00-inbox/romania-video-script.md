---
title: Romania Pathfinding — Video Script
tags: [ai, project, video, script]
status: draft
created: 2026-09-15
updated: 2026-09-15
---

# Romania Pathfinding — Video Script

*Production bible → see artifact (AI Romania Video Production Bible)*
*Project note → [[rome-pathfinding]]*

---

## HOOK (0:00–0:45)

How did you get to KMITL the first time? More than half of you probably came by car — but did you already know the way? No. You opened Google Maps, or Apple Maps, or whatever app you use. It found the best route, the shortest path, avoided the accidents and roadworks.

But have you ever wondered — how does it actually know? How does it work?

---

## THE PROBLEM (0:45–2:00)

Let's use an example straight out of an AI textbook: the Romania map problem.

An agent is on holiday in Romania, currently in the city of Arad. There's a flight from Bucharest tomorrow — it can't be changed. The agent needs to find the shortest path to Bucharest.

Where do you go from Arad? Sibiu, Timisoara, or Zerind? What's the right sequence of moves? This is a search problem: we're looking for a sequence of actions — a route — that reaches the goal.

Here's the catch. This path goes through Fagaras and uses three roads: 140 plus 99 plus 211 — 450 kilometres. This other path goes through Rimnicu Vilcea and Pitesti. Four roads, but only 418 kilometres. Fewer roads doesn't mean shorter. We need to minimise total distance, and do it systematically.

---

## WHY BRUTE FORCE DIES (2:00–3:15)

If we calculated every possible path, computed every cost, and hardcoded it into the system — it wouldn't scale. Say one day the king wants to build a new city. The clerk who made the original map would have to recalculate everything from scratch to find the new optimal paths.

And the numbers get brutal fast. With 20 cities you already have more possible paths than there are seconds since the Big Bang. Brute force is dead before it starts. We need a search strategy.

---

## UNIFORM COST SEARCH (3:15–4:45)

Here's the first smart idea: always expand the cheapest discovered route so far.

Start at Arad — cost zero. Explore its neighbours, record the costs. Now expand the cheapest node. Then its neighbours. Update costs if you find a cheaper way to reach a city. Repeat.

One important detail: we don't stop when we first reach Bucharest. We stop when Bucharest is the cheapest thing left to expand — because only then can we be sure no cheaper alternative is hiding on the frontier. Roads have non-negative costs, so anything cheaper would have been expanded already.

This is Uniform Cost Search. Its priority is just g(n): the cost already paid.

---

## THE HEURISTIC IDEA (4:45–6:15)

UCS works. It always finds the cheapest path. But watch what happens — it expands Timisoara, Zerind, cities heading west, away from Bucharest. It doesn't know that. It only asks: what's the cheapest thing I've found?

What if we gave it a compass?

At any city we know two things: how much we've paid to get here — g — and we can estimate how much is left — call that h. Add them: f. That's our best guess at the total trip cost.

But the estimate has to follow one rule: it can never be higher than the true remaining cost. If it overestimates, we might dismiss a path that's actually best. We call this admissibility — h must never exceed the real distance d.

---

## A* — THE UPGRADE (6:15–7:45)

Instead of ranking by g alone, we rank by f = g + h. We still respect what we've paid. But we lean toward the goal.

With a straight-line distance as h, UCS would expand in all directions like a flood. A* leans toward Bucharest from the start — still carefully tracking costs, still finding the same 418-kilometre answer, but expanding far fewer cities.

Same answer. Less work. That's what a good heuristic buys you.

And because h never overestimates, A* inherits UCS's guarantee: it will always find the shortest path.

---

## OUR HEURISTIC: LP + ALT (7:45–10:30)

Now, there's a hard constraint in our project: straight-line distance is banned. We can only use data from the assignment map — road distances and pixel coordinates. So we built our own heuristic. Two of them, combined.

### LP — Linear Program Heuristic

The first one: what if you didn't have to follow roads as they are? What if you could buy fractions of any road, in any direction, as long as the vectors added up to the total displacement you need to cover?

That's a more flexible problem — a linear program. And because you have more options, the cheapest solution can only be cheaper than any real route — never more expensive. So it's always a valid lower bound.

We solve this offline using scipy with the HiGHS solver. For every pair of cities, we precompute the answer and store it in a table. At search time, it's just a lookup.

For Arad to Bucharest: LP gives 388 kilometres. The real shortest path is 418. Our estimate is lower — never over. Admissible.

### ALT — Landmarks and the Triangle Inequality

The second heuristic uses a trick from geometry. Pick a reference city — a landmark. Precompute the shortest road distance from that landmark to every other city.

Now: if you know the distance from landmark L to node n, and from L to the goal, then the distance from n to the goal must be at least the difference of those two numbers. That's the triangle inequality — no shortcut through a third point can beat a direct route.

We use up to 8 landmarks — cities at geographic extremes, corners of the map. For each city we compute all 8 bounds and take the maximum. More landmarks, tighter bounds.

There's a beautiful edge case. Giurgiu connects to only one city: Bucharest. Because it's a dead-end, the triangle inequality closes perfectly — the landmark bound becomes the exact true distance for any query going to Bucharest. Not an estimate. Exact.

ALT alone, with 8 landmarks, reaches a mean heuristic value of 98.5% of the true road cost. Extremely tight.

### Combining: max, not sum

LP gives 388 for Arad→Bucharest. The Giurgiu landmark gives exactly 418. We take the maximum: 418.

Why not add them? They're both estimating the same remaining journey. Adding would double-count — and break admissibility immediately.

We also keep LP even though ALT alone is nearly as tight: they're completely independent. LP uses pixel coordinates and vector decomposition. ALT uses road distances and geometry. If our landmark selection was somehow flawed, LP still holds. Admissibility doesn't rest on a single assumption.

---

## BIDIRECTIONAL A* (11:15–12:45)

One more technique: run two searches simultaneously. One forward from Arad, one backward from Bucharest. Each uses the same combined heuristic, pointed at the opposite endpoint.

When the two frontiers share a city, we have a complete route. But the first meeting point might not be the cheapest — a different meeting city could form a cheaper path. So we track μ: the best complete route found so far.

We stop when the minimum f-value on either frontier reaches μ. At that point, any cheaper path would need to pass through a frontier city with f below μ — but no such city exists. Done.

On 20 cities, bidirectional is actually slower — the overhead of managing two frontiers outweighs the savings. The real payoff is at millions of nodes, where halving the search depth changes everything.

---

## RESULTS & OUTRO (12:45–14:00)

Let's run it. Same query — Arad to Bucharest. Same answer every time: 418 kilometres, through Sibiu, Rimnicu Vilcea, and Pitesti.

What changes is how much work each algorithm does to get there.

Three ideas built on each other.

First: always expand the cheapest discovered route — UCS. Guarantees you never miss the optimal path.

Second: add an admissible estimate of what's left — A*. Points the search in the right direction without breaking the guarantee.

Third: make that estimate as tight as possible — LP from vector decomposition, ALT from landmark distances and the triangle inequality, combined with max.

The result: a search that's both correct and fast.

And that's what your maps app is doing. Not checking every route. Not guessing. Making an informed, provably safe estimate of where the answer lies — and following it there.

---

*Script status: full draft. Needs: on-camera delivery pass, Manim scene sync, timing check against 10–15 min target.*
