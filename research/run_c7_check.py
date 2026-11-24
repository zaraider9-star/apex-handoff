"""Refactor check: the shared engine must reproduce the Candidate 7 result exactly."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, sys.argv[1]); import engine as E
E.D = sys.argv[2]; E.CUTOFF = pd.Timestamp("2026-11-23")
ry = E.fred("DFII10")
gold = E.Inst("GOLD", "GLD", "GCF", 0.50, 0.02)
silver = E.Inst("SILVER", "SLV", "SIF", 0.03, 0.02)
fn = lambda L, inst: -np.sign(ry - ry.shift(L))
E.evaluate("C7 refactor check", gold, fn, [1, 5, 20], [1, 5, 20], silver, fn, pname="L")
