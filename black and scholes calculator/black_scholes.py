import math

def norm_cdf(x):
    """Cumulative distribution function della normale standard N(0,1)"""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def norm_pdf(x):
    """Probability density function della normale standard N(0,1)"""
    return math.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)

def black_scholes(s_0, alpha, sigma, r, K, T, delta=0, t=0):
    """Calcola i prezzi di Call e Put con il modello Black-Scholes."""
    
    # Time to maturity
    tau = T - t
    
    if tau <= 0:
        print("ATTENZIONE: Opzione scaduta.")
        # Opzione scaduta
        call_price = max(s_0 - K, 0)
        put_price = max(K - s_0, 0)
        return {
            'd1': None,
            'd2': None,
            'N_d1': None,
            'N_d2': None,
            'call_price': call_price,
            'put_price': put_price
        }
    
    # Scontiamo i dividendi continui usando s * e^(-delta*(T-t))
    # Se delta è 0, s_0_w_dividends è uguale a s_0
    s_0_w_dividends = s_0 * math.exp(-delta * tau)
    
    # Calcoliamo d1 e d2 usando s_0_w_dividends
    d1 = (math.log(s_0_w_dividends / K) + (r + 0.5 * sigma**2) * tau) / (sigma * math.sqrt(tau))
    d2 = d1 - sigma * math.sqrt(tau)
    
    # N(d1) e N(d2) - CDF della normale standard
    N_d1 = norm_cdf(d1)
    N_d2 = norm_cdf(d2)
    N_minus_d1 = norm_cdf(-d1)
    N_minus_d2 = norm_cdf(-d2)
    
    # Prezzi Call e Put (formula standard con s_0_w_dividends)
    call_price = s_0_w_dividends * N_d1 - K * math.exp(-r * tau) * N_d2
    put_price = K * math.exp(-r * tau) * N_minus_d2 - s_0_w_dividends * N_minus_d1
    
    # ========== GRECHE ==========
    
    # PDF di d1
    phi_d1 = norm_pdf(d1)
    
    # Delta: sensibilità al prezzo del sottostante
    call_delta = math.exp(-delta * tau) * N_d1
    put_delta = -math.exp(-delta * tau) * N_minus_d1
    
    # Gamma: sensibilità del delta al prezzo (uguale per call e put)
    gamma = math.exp(-delta * tau) * phi_d1 / (s_0 * sigma * math.sqrt(tau))
    
    # Vega: sensibilità alla volatilità (uguale per call e put)
    vega = s_0 * math.exp(-delta * tau) * phi_d1 * math.sqrt(tau)
    
    # Theta: sensibilità al tempo (decay temporale)
    theta_call = (
        -s_0 * math.exp(-delta * tau) * phi_d1 * sigma / (2 * math.sqrt(tau))
        - r * K * math.exp(-r * tau) * N_d2
        + delta * s_0 * math.exp(-delta * tau) * N_d1
    )
    theta_put = (
        -s_0 * math.exp(-delta * tau) * phi_d1 * sigma / (2 * math.sqrt(tau))
        + r * K * math.exp(-r * tau) * N_minus_d2
        - delta * s_0 * math.exp(-delta * tau) * N_minus_d1
    )
    
    # Rho: sensibilità al tasso risk-free
    rho_call = K * tau * math.exp(-r * tau) * N_d2
    rho_put = -K * tau * math.exp(-r * tau) * N_minus_d2
    
    # Probabilità di finire ITM (in-the-money) in misura risk-neutral
    prob_itm_call = N_d2
    prob_itm_put = N_minus_d2
    
    return {
        'd1': d1,
        'd2': d2,
        'N_d1': N_d1,
        'N_d2': N_d2,
        'call_price': call_price,
        'N_minus_d1': N_minus_d1,
        'N_minus_d2': N_minus_d2,
        'put_price': put_price,
        'call_delta': call_delta,
        'put_delta': put_delta,
        'gamma': gamma,
        'vega': vega,
        'theta_call': theta_call,
        'theta_put': theta_put,
        'rho_call': rho_call,
        'rho_put': rho_put,
        'prob_itm_call': prob_itm_call,
        'prob_itm_put': prob_itm_put
    }


# Esempio di utilizzo
if __name__ == "__main__":
    # Parametri di esempio
    s_0 = 40
    alpha = 0.8
    sigma = 0.4
    r = 0.05
    K = 40
    T = 0.5
    delta = 0.02
    t = 0
    
    risultati = black_scholes(s_0, alpha, sigma, r, K, T, delta, t)
    
    print("=" * 60)
    print("BLACK-SCHOLES CALCULATOR")
    print("=" * 60)
    print(f"\nParametri:")
    print(f"  S_0 = {s_0}")
    print(f"  K = {K}")
    print(f"  r = {r}")
    print(f"  sigma = {sigma}")
    print(f"  T = {T}")
    print(f"  t = {t}")
    print(f"  delta = {delta}")
    print(f"\nRisultati intermedi:")
    print(f"  d1 = {risultati['d1']:.6f}")
    print(f"  d2 = {risultati['d2']:.6f}")
    print(f"  N(d1) = {risultati['N_d1']:.6f}")
    print(f"  N(d2) = {risultati['N_d2']:.6f}")
    print(f"\nPrezzi:")
    print(f"  Call = {risultati['call_price']:.4f}")
    print(f"  Put  = {risultati['put_price']:.4f}")
    print(f"\nGRECHE - CALL:")
    print(f"  Delta = {risultati['call_delta']:.6f}")
    print(f"  Gamma = {risultati['gamma']:.6f}")
    print(f"  Theta = {risultati['theta_call']:.6f}")
    print(f"  Vega  = {risultati['vega']:.6f}")
    print(f"  Rho   = {risultati['rho_call']:.6f}")
    print(f"  P(ITM) = {risultati['prob_itm_call']:.4f} ({risultati['prob_itm_call']*100:.2f}%)")
    print(f"\nGRECHE - PUT:")
    print(f"  Delta = {risultati['put_delta']:.6f}")
    print(f"  Gamma = {risultati['gamma']:.6f}")
    print(f"  Theta = {risultati['theta_put']:.6f}")
    print(f"  Vega  = {risultati['vega']:.6f}")
    print(f"  Rho   = {risultati['rho_put']:.6f}")
    print(f"  P(ITM) = {risultati['prob_itm_put']:.4f} ({risultati['prob_itm_put']*100:.2f}%)")
    print("=" * 60)