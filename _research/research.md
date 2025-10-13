---
title: "Research"
permalink: /research/
layout: single
author_profile: true
---

> I work on fast-transient PMICs, high-density hybrid converters, and robust current balancing across concurrent multi-inductor paths.

## 1) Fast-Transient Dual-Loop Hybrids (single-chip & multi-chip)
We address transient droop/overshoot by combining a **fast VOUT loop** with a **slow VAUX loop** that specifies the current allocation among **non-uniform (large/small) inductors**.

**Highlights**
- Dual-loop control: fast regulation for immediate load steps; slow VAUX loop sets inductor current ratios.
- Non-uniform multi-inductor paths to boost both rising and falling current slew rates.
- **Single-chip** LLSC prototype and **multi-chip** “bucklet” arrays with decentralized coordination.
- Modeling & stability guidance for coupled loops; measured large-signal transients.

---

## 2) Inductor-First Hybrids for High Power Density
To push density, we develop **inductor-first / inductor-on-ground hybrid switched-capacitor** converters that shrink magnetics and favor on-package/on-board integration.

**Highlights**
- Inductor-first energy routing to reduce switch stress and improve efficiency at high VCR.
- Multi-path operation with ripple-reduction techniques for compact passives.
- Packaging co-design (on-package IVRs, short PDN) and thermal/EMI considerations.
- High-frequency operation and WBG-friendly gate driving for better FoM.

---

## 3) Concurrent Multi-Inductor Supply with Current Balancing
We propose lightweight **current-sharing** methods when multiple inductor paths deliver current simultaneously.

**Highlights**
- Low-overhead / one-pin current-balancing strategies (no high-bandwidth inter-module links).
- Robust to parameter mismatch and **heterogeneous frequencies/bandwidths** across modules.
- Beat-frequency/ripple interaction analysis and EMI mitigation.
- Startup/protection coordination for large arrays; silicon/PCB validation.

