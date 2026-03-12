---
layout: archive
title: "Research"
permalink: /research/
author_profile: true
<style>
.chip-gallery {
  margin: 30px 0 40px 0;
}
.chip-gallery .row {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
  justify-content: center;
}
.chip-gallery .chip-card {
  flex: 1;
  max-width: 340px;
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}
.chip-gallery .chip-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}
.chip-gallery .chip-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}
.chip-gallery .chip-card .caption {
  padding: 8px 10px;
  font-size: 0.78em;
  color: #444;
  line-height: 1.4;
  border-top: 1px solid #e0e0e0;
}
.chip-gallery .chip-card .caption strong {
  display: block;
  font-size: 0.88em;
  color: #1a1a2e;
  margin-bottom: 2px;
}
<div class="chip-gallery">
  <div class="row">
    <div class="chip-card">
      <img src="/images/chip_sdsd.jpg" alt="SDSD Chip">
      <div class="caption">
        <strong>① SDSD Hybrid Converter</strong>
        IEEE TCAS-I 2023 · 180nm BCD
      </div>
    </div>
    <div class="chip-card">
      <img src="/images/chip_inductor_first.jpg" alt="Inductor-First Chip">
      <div class="caption">
        <strong>② Inductor-First Hybrid</strong>
        IEEE CICC 2023 / JSSC 2025 · 180nm BCD
      </div>
    </div>
  </div>
  <div class="row">
    <div class="chip-card">
      <img src="/images/chip_aux_transient.jpg" alt="Aux Transient Chip">
      <div class="caption">
        <strong>③ Easy-Add-On Transient Module</strong>
        PCB Prototype
      </div>
    </div>
    <div class="chip-card">
      <img src="/images/chip_dual_loop.jpg" alt="Dual-Loop Chip">
      <div class="caption">
        <strong>④ Dual-Loop LLSC (20MHz+1MHz)</strong>
        IEEE ISSCC Highlight · 55nm BCD
      </div>
    </div>
    <div class="chip-card">
      <img src="/images/chip_one_pin.jpg" alt="One-Pin Array Chip">
      <div class="caption">
        <strong>⑤ One-Pin Current Balancing Array</strong>
        IEEE CICC 2026 · 55nm BCD
      </div>
    </div>
  </div>
</div>
My research focuses on power management ICs (PMICs) for AI computing platforms—spanning battery-powered edge devices and high-current cloud accelerators. I design hybrid switched-capacitor/inductor DC-DC converters that simultaneously achieve high efficiency, high power density, fast transient response, and scalable current delivery.
---
1) Symmetric Double Step-Down (SDSD) Hybrid Converter
Challenge: In battery-powered devices, the input voltage swings widely (2.7–4.2 V for Li-ion), while the processor core needs a tight low voltage (~0.5–0.8 V). Conventional Double Step-Down (DSD) hybrids are constrained to duty cycles D < 0.5, limiting their usable conversion ratio range and leaving efficiency gaps at certain operating points.
Approach: By symmetrizing the DSD topology, I break the D < 0.5 constraint and extend the effective voltage conversion ratio (VCR) range without adding switching stages. The symmetric structure also equalizes inductor charging intervals, improving current density and reducing output ripple.
Highlights:
Extends hybrid converter VCR range beyond the traditional D < 0.5 limit
Improves efficiency across the full battery discharge range
Reduces inductor size and output capacitor requirements
Validated in silicon; cited by groups at Dartmouth College, SCUT, and others
📄 Published in IEEE TCAS-I (2023)
---
2) Inductor-First / Inductor-on-Ground Hybrid Converter
Challenge: Conventional hybrid converters place the inductor on the output (high-current) side, causing large DCR losses, high input current ripple, and dependence on bulky input capacitors—making "high efficiency + small volume + wide VCR" hard to achieve simultaneously.
Approach: I propose repositioning the inductor to the input or ground-referenced branch ("inductor-first" or "inductor-on-ground"), so energy buffering moves upstream. This makes input current quasi-continuous, dramatically reduces input capacitor requirements, and lowers effective conduction loss at high-current nodes.
Highlights:
Covers Vin = 3–5 V (Li-ion + 5V USB), Vout = 0.5–1.2 V, VCR up to 10:1
96.1% peak efficiency; 1.02 A/mm² chip-area current density (~2.3× over prior art)
Reduced EMI due to continuous input current
Passive components can be placed flexibly on PCB back or near-load area
📄 Published in IEEE CICC (2023); extended version in IEEE JSSC (2025)
---
3) Easy-Add-On Auxiliary Transient Module
Challenge: In 48V/12V bus-powered AI accelerator systems, load current slews at extremely high di/dt. If the main power stage is optimized for steady-state efficiency (large inductors, low bandwidth), transient undershoot/overshoot is severe and recovery is slow, forcing large voltage guardband.
Approach: I decouple the "efficiency" task from the "transient" task. The main high-voltage power stage handles steady-state conversion. A small, easy-to-integrate auxiliary module—built with low-voltage core devices (better FoM)—injects high di/dt current only during the critical transient window, without modifying the main stage.
Highlights:
Load-step undershoot: 115 mV → 13 mV (8.8×); recovery: 80 µs → 2.5 µs (32×)
Load-release overshoot: 145 mV → 22 mV (6.6×); recovery: 35 µs → 3 µs (11.7×)
Main stage efficiency unaffected; auxiliary module is "plug-in" compatible
Demonstrates "HV devices for steady-state, LV devices for transient" task-decoupling paradigm
📄 Manuscript in preparation
---
4) Single-Chip Dual-Loop Hybrid Converter (20 MHz + 1 MHz)
Challenge: High-VCR bus-powered supplies must deliver both high steady-state efficiency and fast transient response—but these goals create a fundamental tension in single-loop topologies: optimizing for efficiency limits bandwidth, and vice versa.
Approach: I implement a fast-slow dual-module architecture on a single chip with a dedicated dual-loop control: a slow module (≈1 MHz) handles the high-VCR, high-power path for efficiency; a fast module (≈20 MHz) handles transient current injection at high bandwidth. The two loops are designed for bandwidth separation and verified for coupled-loop stability.
Highlights:
Vout undershoot: 426 mV → 35 mV (12.2×); overshoot: 397 mV → 32 mV (12.4×)
Retains hybrid converter advantages in efficiency and passive volume
Dual-loop co-stability validated via small-signal modeling and silicon measurement
Establishes a reusable "fast-slow split + dual-loop" design paradigm
📄 Published in IEEE ISSCC (highlight paper)
---
5) Scalable Power Chiplet Array with One-Pin Current Balancing
Challenge: As single-package current scales toward hundreds of amperes, centralized parallel control (one PWM/CS line per phase) becomes a routing bottleneck: interconnect complexity grows as O(N), parameter mismatch causes current imbalance, and transient de-synchronization creates ringing and stability risks.
Approach: I propose distributed local feedback with a single shared one-pin bus for current self-balancing. Each converter unit performs autonomous local control; inter-module communication is reduced to O(1). The one-pin bus passively equalizes currents without high-bandwidth digital links, enabling robust scalability.
Highlights:
4-phase array: 12V → 1V, up to 22 A; 89.1% peak efficiency; 1.46 A/mm² current density
6A / 20ns load step: ~55 mV undershoot, 2.2 µs recovery
Measured inter-phase current mismatch stays small across all operating conditions
Directly applicable to Power Chiplet and vertical power delivery architectures
📄 Prototype validated; paper in preparation
