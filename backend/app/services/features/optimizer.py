"""Mean-variance portfolio optimization."""

import cvxpy as cp
import numpy as np


def mean_variance_opt(mu: np.ndarray, cov: np.ndarray, max_w: float = 0.35):
    n = len(mu)
    w = cp.Variable(n)
    gamma = 1.0  # risk aversion hyperparameter (tune later / expose to user)
    objective = cp.Maximize(mu @ w - gamma * cp.quad_form(w, cov))
    constraints = [cp.sum(w) == 1, w >= 0, w <= max_w]
    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.ECOS, verbose=False)
    
    # Check if solution exists
    if w.value is None or prob.status not in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
        # Fallback to equal weights if optimization fails
        return np.ones(n) / n
    
    return np.clip(np.array(w.value).flatten(), 0, 1)
