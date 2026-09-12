import io
import pandas as pd


def parse_excel(file_bytes: bytes) -> dict:
    buffer = io.BytesIO(file_bytes)

    df = pd.read_excel(buffer)

    return {
        "format": "EXCEL",
        "columns": [str(col) for col in df.columns],
        "rows": df.fillna("").to_dict(orient="records"),
        "row_count": len(df)
    }