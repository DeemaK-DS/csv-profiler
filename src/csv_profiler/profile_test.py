def basic_profile(rows: list[dict[str, str]]) -> dict:
    if not rows:
        return {
            "source": None,
            "summary": {"rows": 0, "columns": 0},
            "columns": {},
            "notes": ["Empty dataset"],
        }

    column_names = list(rows[0].keys())
    column_profiles = {}

    for col in column_names:
        values = column_values(rows, col)
        col_type = infer_type(values)

        if col_type == "number":
            stats = numeric_stats(values)
        else:
            stats = text_stats(values)

        column_profiles[col] = {
            "type": col_type,
            "stats": stats,
        }

    return {
        "source": None,
        "summary": {
            "rows": len(rows),
            "columns": len(column_names),
        },
        "columns": column_profiles,
    }

    
# ------d2------

MISSING = {"", "na", "n/a", "null", "none", "nan"}
def is_missing(value: str | None) -> bool:
    if value is None:
     return True
    cleaned = value.strip().casefold()
    return cleaned in MISSING

def try_float(value: str) -> float | None:
    try:
      return float(value)
    except ValueError:
      return None
  
def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
     return "text"
    for v in usable:
     if try_float(v) is None:
      return "text"
    return "number"

def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
 return [row.get(col, "") for row in rows]

def numeric_stats(values: list[str]) -> dict:
    numbers = []
    missing = 0

    for v in values:
        if is_missing(v):
            missing += 1
            continue

        value = try_float(v)
        if value is None:
            raise ValueError(f"Non-numeric value found: {v!r}")

        numbers.append(value)

    count = len(numbers)

    if count == 0:
        return {
            "count": 0,
            "missing": missing,
            "unique": 0,
            "min": None,
            "max": None,
            "mean": None,
        }

    return {
        "count": count,
        "missing": missing,
        "unique": len(set(numbers)),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / count,
    }


def text_stats(values: list[str], top_k: int = 5) -> dict:
    counts = {}
    missing = 0

    for v in values:
        if is_missing(v):
            missing += 1
            continue

        if v in counts:
            counts[v] += 1
        else:
            counts[v] = 1

    total = sum(counts.values())

    sorted_items = sorted(
        counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    top = []
    for value, count in sorted_items[:top_k]:
        top.append({
            "value": value,
            "count": count
        })

    return {
        "count": total,
        "missing": missing,
        "unique": len(counts),
        "top": top,
    }

    
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  