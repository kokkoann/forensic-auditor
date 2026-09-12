from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SAT_69B_PATH = (
    BASE_DIR
    / "external_data"
    / "sat"
    / "Listado_completo_69-B.csv"
)


def load_69b() -> pd.DataFrame:
    df = pd.read_csv(
        SAT_69B_PATH,
        encoding="latin1",
        header=2
    )

    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    df["RFC"] = (
        df["RFC"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return df


def classify_69b_status(status: str) -> str:
    status = str(status).strip().lower()

    if status == "definitivo":
        return "HIGH"

    if status == "presunto":
        return "MEDIUM"

    if status == "desvirtuado":
        return "LOW"

    if status == "sentencia favorable":
        return "LOW"

    return "UNKNOWN"


def check_rfc_69b(rfc: str) -> dict:
    df = load_69b()

    rfc = str(rfc).strip().upper()

    matches = df[
        df["RFC"] == rfc
    ]

    if matches.empty:
        return {
            "type": "SAT_69B",
            "rfc": rfc,
            "found": False,
            "status": None,
            "severity": "NONE",
            "taxpayer_name": None
        }

    row = matches.iloc[0]

    status = str(
        row.get(
            "Situación del contribuyente",
            ""
        )
    ).strip()

    taxpayer_name = str(
        row.get(
            "Nombre del Contribuyente",
            ""
        )
    ).strip()

    return {
        "type": "SAT_69B",
        "rfc": rfc,
        "found": True,
        "status": status,
        "severity": classify_69b_status(status),
        "taxpayer_name": taxpayer_name
    }