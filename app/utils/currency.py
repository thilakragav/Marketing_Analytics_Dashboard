"""
Global Currency Configuration and Conversion Utility for Marketing Intelligence Suite.

This module centralizes:
- Supported currencies and exchange rates (relative to USD)
- Central state management for the active global reporting currency
- Safe currency conversion for scalars, pandas Series, and DataFrames
- Standardized currency formatting (full and compact)
- Persistence of user currency preferences across page navigations and reloads
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# CONFIGURATION & EXCHANGE RATES (RELATIVE TO USD BASE)
# ==============================================================================

# Central exchange rates: Base is USD (1.0)
# Rates can easily be updated here or loaded from environment/configuration
CURRENCY_CONFIG: Dict[str, Dict[str, Any]] = {
    "USD": {
        "code": "USD",
        "symbol": "$",
        "rate": 1.0,
        "label": "USD ($)",
        "name": "US Dollar",
        "format_template": "${:,.2f}",
    },
    "INR": {
        "code": "INR",
        "symbol": "₹",
        "rate": 83.0,
        "label": "INR (₹)",
        "name": "Indian Rupee",
        "format_template": "₹{:,.2f}",
    },
    "EUR": {
        "code": "EUR",
        "symbol": "€",
        "rate": 0.92,
        "label": "EUR (€)",
        "name": "Euro",
        "format_template": "€{:,.2f}",
    },
    "GBP": {
        "code": "GBP",
        "symbol": "£",
        "rate": 0.79,
        "label": "GBP (£)",
        "name": "British Pound",
        "format_template": "£{:,.2f}",
    },
}

CURRENCY_OPTIONS: List[str] = [cfg["label"] for cfg in CURRENCY_CONFIG.values()]
DEFAULT_CURRENCY = "USD"

# Path for optional local preference persistence (survives browser reload)
PREFERENCES_FILE = Path(__file__).resolve().parents[2] / "config" / "user_preferences.json"


# ==============================================================================
# CODE & SYMBOL NORMALIZATION
# ==============================================================================

def normalize_currency_code(currency: Optional[str]) -> str:
    """
    Normalizes any currency representation ('USD ($)', 'INR', '₹', '€', etc.)
    to standard 3-letter currency code ('USD', 'INR', 'EUR', 'GBP').
    Defaults to 'USD' if unrecognized or None.
    """
    if not currency:
        return DEFAULT_CURRENCY

    cleaned = str(currency).strip()

    # Direct match on code
    if cleaned.upper() in CURRENCY_CONFIG:
        return cleaned.upper()

    # Match by label prefix (e.g. 'USD ($)' -> 'USD')
    for code, info in CURRENCY_CONFIG.items():
        if cleaned.upper().startswith(code):
            return code
        if info["symbol"] == cleaned:
            return code
        if info["label"] == cleaned:
            return code

    return DEFAULT_CURRENCY


# ==============================================================================
# GLOBAL CURRENCY STATE MANAGEMENT
# ==============================================================================

def _load_saved_preference() -> str:
    """Loads saved currency preference from config/user_preferences.json if available."""
    try:
        if PREFERENCES_FILE.exists():
            with open(PREFERENCES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                code = data.get("selected_currency")
                if code and code in CURRENCY_CONFIG:
                    return code
    except Exception:
        pass
    return DEFAULT_CURRENCY


def _save_preference(code: str) -> None:
    """Saves active currency preference to config/user_preferences.json."""
    try:
        PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PREFERENCES_FILE, "w", encoding="utf-8") as f:
            json.dump({"selected_currency": code}, f, indent=2)
    except Exception:
        pass


def get_selected_currency() -> str:
    """
    Retrieves the currently selected global reporting currency code.
    Reads from st.session_state -> saved preference -> default ('USD').
    """
    try:
        if hasattr(st, "session_state") and "selected_currency" in st.session_state:
            curr = st.session_state["selected_currency"]
            return normalize_currency_code(curr)
    except Exception:
        pass

    # Fallback to persisted preference file
    saved = _load_saved_preference()

    # Cache in session state if available
    try:
        if hasattr(st, "session_state"):
            st.session_state["selected_currency"] = saved
            st.session_state["currency_symbol"] = CURRENCY_CONFIG[saved]["symbol"]
            st.session_state["currency_rate"] = CURRENCY_CONFIG[saved]["rate"]
    except Exception:
        pass

    return saved


def set_selected_currency(currency_or_label: str) -> str:
    """
    Updates the global currency in session_state and persists it.
    Returns the normalized currency code.
    """
    code = normalize_currency_code(currency_or_label)
    info = CURRENCY_CONFIG[code]

    try:
        if hasattr(st, "session_state"):
            st.session_state["selected_currency"] = code
            st.session_state["currency_symbol"] = info["symbol"]
            st.session_state["currency_rate"] = info["rate"]
            st.session_state["reporting_currency"] = info["label"]
    except Exception:
        pass

    _save_preference(code)
    return code


def get_currency_symbol(currency: Optional[str] = None) -> str:
    """
    Returns the currency symbol ('$', '₹', '€', '£') for the specified currency
    or the currently selected global currency if None.
    """
    code = normalize_currency_code(currency) if currency else get_selected_currency()
    return CURRENCY_CONFIG.get(code, CURRENCY_CONFIG[DEFAULT_CURRENCY])["symbol"]


def get_currency_rate(to_currency: Optional[str] = None, from_currency: str = "USD") -> float:
    """
    Calculates the conversion rate from `from_currency` to `to_currency`.
    Defaults: from USD to the currently selected currency.
    """
    to_code = normalize_currency_code(to_currency) if to_currency else get_selected_currency()
    from_code = normalize_currency_code(from_currency)

    rate_to = CURRENCY_CONFIG.get(to_code, {}).get("rate", 1.0)
    rate_from = CURRENCY_CONFIG.get(from_code, {}).get("rate", 1.0)

    if rate_from == 0:
        return 1.0

    return float(rate_to / rate_from)


# ==============================================================================
# CONVERSION FUNCTIONS
# ==============================================================================

def convert_currency(
    value: Union[float, int, pd.Series, np.ndarray, None],
    from_currency: str = "USD",
    to_currency: Optional[str] = None
) -> Any:
    """
    Converts numeric monetary values from `from_currency` (default USD)
    to `to_currency` (default: globally selected currency).

    Accepts scalars, None, NaN, and pandas Series.
    Always safe: never mutates in-place.
    """
    if value is None:
        return None

    to_code = normalize_currency_code(to_currency) if to_currency else get_selected_currency()
    from_code = normalize_currency_code(from_currency)

    # Short-circuit if same currency
    if to_code == from_code:
        if isinstance(value, pd.Series):
            return value.copy()
        return value

    rate = get_currency_rate(to_currency=to_code, from_currency=from_code)

    if isinstance(value, pd.Series):
        return value * rate
    elif isinstance(value, np.ndarray):
        return value * rate
    elif isinstance(value, (int, float, np.number)):
        if pd.isna(value):
            return value
        return float(value * rate)
    else:
        # Fallback for unexpected non-numeric
        return value


# ==============================================================================
# FORMATTING UTILITIES
# ==============================================================================

def format_currency(
    value: Optional[float],
    currency: Optional[str] = None,
    convert_from: Optional[str] = "USD",
    decimals: int = 2,
    compact: bool = False
) -> str:
    """
    Formats a numeric value into a currency display string.

    Parameters:
    - value: The monetary value to format
    - currency: Target currency (defaults to selected currency)
    - convert_from: If provided (default "USD"), converts from that currency first.
                    Set to None if value is already converted.
    - decimals: Decimal places for display (default 2)
    - compact: If True, uses 'K' and 'M' suffixes (e.g. ₹83.0K, $1.2M)
    """
    if value is None or pd.isna(value):
        return "N/A"

    code = normalize_currency_code(currency) if currency else get_selected_currency()
    sym = get_currency_symbol(code)

    # Perform conversion if needed
    if convert_from is not None:
        val = convert_currency(value, from_currency=convert_from, to_currency=code)
    else:
        val = float(value)

    if pd.isna(val):
        return "N/A"

    if compact:
        abs_v = abs(val)
        if abs_v >= 1_000_000:
            return f"{sym}{val / 1_000_000:.2f}M"
        elif abs_v >= 1_000:
            return f"{sym}{val / 1_000:.1f}K"
        else:
            return f"{sym}{val:,.{decimals}f}"
    else:
        return f"{sym}{val:,.{decimals}f}"


def format_currency_label(text: str, currency: Optional[str] = None) -> str:
    """
    Replaces common currency markers in titles or axes with the active currency symbol.
    Example: 'Revenue ($)' -> 'Revenue (₹)'
    """
    sym = get_currency_symbol(currency)
    for existing in ["($)", "(₹)", "(€)", "(£)", "($ USD)", "(USD)"]:
        if existing in text:
            return text.replace(existing, f"({sym})")
    return f"{text} ({sym})"
