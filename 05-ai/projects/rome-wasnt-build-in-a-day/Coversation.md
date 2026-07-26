# AI Project Analysis: Romania Pathfinding & Heuristics

## 💬 Conversation Summary: Bento & "Cream Bun"
The recent discussion focused on navigating the technical constraints and optimization strategies for the Romania-Map assignment.
- **Strict Constraints:** The Professor has explicitly prohibited the use of **Straight-Line Distance (SLD)** as a heuristic. Students must develop a **custom heuristic** using only the data provided in the PDF.
- **Data Extraction:** Bento extracted pixel-based coordinates for the cities (e.g., Arad at 773, 874) to use as a baseline, while others like "Cream Bun" attempted to organize this data into JSON format.
- **The "Corridor" Algorithm:** Bento developed a sophisticated heuristic called **"CORRIDOR,"** which incorporates Bézier curves, Hop-Filters, and Windowed Dynamic Programming.
- **Optimization vs. Utility:** Bento's custom method is **1.18x faster per query** than standard methods but is nearly **8,000x slower to precompute**. Bento admitted that this level of "bit trickery" and extreme optimization might be drifting away from the actual **grading criteria**.

## 📊 Current Project Situation
- **Technical Progress:**
    - Map coordinates (X, Y axes) have been successfully extracted from the assignment image.
    - Performance benchmarks have been established comparing **Dijkstra** (Blind Search) against the custom **Corridor** heuristic.
- **Key Metrics:**
    - **Efficiency:** The Corridor heuristic visits fewer nodes (avg 5.7) and is faster per query (2399 ns) than Dijkstra (11.3 nodes, 3513 ns).
    - **Admissibility:** The custom heuristic is confirmed as **admissible** for all 190 tested city pairs, ensuring it never overestimates the actual path cost.
- **Risks:** The high precompute time (~345ms) means the system only "breaks even" in efficiency after more than 310,000 queries.

## 🧒 ELI5: What's Happening?
Imagine you have to find the best way to drive across a map of Romania.
1. **The Rule:** The teacher said you **cannot use a ruler** to measure the straight distance between cities to help you "guess" the right way.
2. **The "Super Brain":** Bento spent a lot of time building a very complicated math machine to help the computer make really good guesses.
3. **The Problem:** This machine is like a giant robot that takes **3 hours to assemble** just so it can help you find a wrench **1 second faster** than doing it by hand.
4. **The Goal:** It works perfectly, but we need to make sure the website is easy to use and looks good, rather than just being obsessed with super-fast math!.