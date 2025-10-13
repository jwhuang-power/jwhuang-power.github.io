---
title: "Research"
permalink: /research/
layout: single
author_profile: true
---

> I work on fast-transient PMICs, high-density hybrid converters, and scalable control for parallel/heterogeneous modules.

## 1) Fast-Transient Hybrid Converters with Specified Current Allocation
We develop dual-loop, non-uniform multi-inductor hybrid DC–DC converters that reallocate inductor currents during load transients to minimize droop/overshoot and recovery time.

**Key ideas**
- Dual-loop regulation: a fast VOUT loop + a slow VAUX loop that sets the current ratio among multiple inductors.  
- Non-uniform multi-inductor paths to boost both rising and falling current slew rates.  
- Small-signal modeling and stability guidelines for the coupled loops.  
- Silicon/PCB validation under large step loads.

**Resources**: [Paper](/files/LLSC_paper.pdf) · [Slides](/files/LLSC_slides.pdf)

---

## 2) Inductor-First / Inductor-on-Ground Hybrid Switched-Capacitor Converters
To push power density, we design multi-path inductor-first (IOG) hybrid SC converters that shrink magnetics and enable in-package/on-board integration for CPU/GPU rails.

**Key ideas**
- Inductor-first energy routing to reduce switch stress and improve conversion efficiency.  
- Multi-path current flow with ripple-reduction techniques for compact passives.  
- Packaging co-design (on-package IVRs, short PDN) and thermal hot-spot management.  
- Wide-bandgap-friendly gate driving and loss breakdown at high frequency.

**Resources**: [Paper](/files/InductorFirst_paper.pdf) · [Poster](/files/InductorFirst_poster.pdf)

---

## 3) Scalable Multi-Chip Power Delivery with Heterogeneous Frequencies
We study decentralized control for many parallel modules operating at different switching frequencies, ensuring current balance and system stability.

**Key ideas**
- One-pin / low-overhead current balancing without high-bandwidth inter-module links.  
- Compatibility with heterogeneous switching frequencies and bandwidths.  
- Beat-frequency/ripple interaction analysis and EMI mitigation.  
- Digital COT / current-mode variants and start-up/protection coordination for large arrays.

**Resources**: [Overview](/files/Multichip_PD_Overview.pdf) · [Demo video](/files/Multichip_demo.mp4)
