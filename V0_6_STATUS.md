# v0.6 candidate — named-step correspondence

Issue #20 now has an implementation candidate in `forward-simulation-track/`.
The frozen contract and the 124-theorem root source remain unchanged.

The candidate contains 12 new Lean 4.22.0 theorems, 43 pinned-runtime replay
transitions with generated kernel-checked certificates, EX-1/EX-2, required
MU-1..MU-8 (9 probes), five extra Lean mutants, and the 38 pinned multiblock
verifier tests. Its independent CI performs source, fixture, callable, and
axiom binding. The isolated README describes what the encoding assumes and
what executable replay establishes.

General proof: the encoded named concrete step relation implies abstract
append/reject/stutter matching under explicit digest correspondence.
Runtime connection: source-bound, bounded replay and source inspection; no
universal Python semantics or parser proof is supplied.

This document does not close issue #20 or change main's claim ceiling. Promotion
requires the frozen gate, including independent root CI and review of the exact
encoding against the source. W0 / O0 WITHHELD / production NOT GRANTED.
