# Oleksii Kurdysh — SBI integration into di-Higgs search workflow 

## Short description
The Higgs boson was discovered in 2012. The observation of Higgs boson pair (di-Higgs, HH) production remains one of the outstanding open questions in particle physics. Its study provides a direct test of whether the Standard Model accurately describes the Higgs sector. 
Related problem is measurement of the trilinear Higgs self-coupling $\kappa_{\lambda}$.
Depending on the value of this coupling, scenarios featuring a strong first-order electroweak phase transition in the early Universe may be constrained or excluded. Recent public ATLAS result on the subject is [1]. NSBI is the new approach for ATLAS, thus far used only once in [2] for different kind of problem.

## Simplified tasks for hackaton
Two stages of typical publication workflow are picked out and simplified: 
1. Discrimination between HH and other process that "look similar", as data collected by the detector doesn't have labels on which process it is. This is a classification task appropriate for NRE. Currenly taks is done by Boosted Decision Tree performance of which will serve as baseline.
2. $\kappa_{\lambda}$ inference for samples with known values. Appropriate to NLE.

Additional task which is closer to real life and is a combination of two above is an learning of test statistics, which in ATLAS (mostly frequentist) is likelihood ratio.

## Data used
ATLAS simulation of di-Higgs and single-Higgs processes. Five di-Higgs samples with different $\kappa_{\lambda}$ 300k events each. All single-H production modes samples with 300k-5m events each. Each sample is a tabular data with various information measured by the detector - around 40 quantities.

## Code availability
https://github.com/oleksii165/bbyy-nsbi

## References
1. ATLAS collaboration (2025).
  *Study of Higgs boson pair production in the $HH \rightarrow b\overline{b}\gamma\gamma$ final state with 308 $fb^{-1}$ of data collected at $\sqrt{s}=13$ TeV and 13.6 TeV by the ATLAS experiment*
  https://arxiv.org/abs/2507.03495.
2. ATLAS collaboration (2025).
  *An implementation of neural simulation-based inference for parameter estimation in ATLAS.*
  Rep. Prog. Phys. 88 (2025) 067801.
