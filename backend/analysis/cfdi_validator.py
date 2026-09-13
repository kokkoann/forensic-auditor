from decimal import Decimal, InvalidOperation

from lxml import etree

from analysis.blacklist_69b import check_rfc_69b


CFDI_NS = "http://www.sat.gob.mx/cfd/4"

TFD_NS = "http://www.sat.gob.mx/TimbreFiscalDigital"


def to_decimal(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return Decimal("0")


def add_finding(
    findings,
    rule_id,
    finding_type,
    severity,
    message,
    **extra
):
    finding = {
        "rule_id": rule_id,
        "type": finding_type,
        "severity": severity,
        "message": message
    }

    finding.update(extra)

    findings.append(finding)


def validate_cfdi(document: dict) -> dict:

    findings = []

    xml_text = document.get("xml_text", "")

    if not xml_text:
        return {
            "valid_basic_structure": False,
            "cfdi_data": {},
            "findings": [
                {
                    "rule_id": "CFDI_XML_EMPTY",
                    "type": "CFDI_STRUCTURE_ERROR",
                    "severity": "HIGH",
                    "message": "El documento XML no contiene información procesable."
                }
            ]
        }

    
    # 1. Parsear XML
    

    try:

        root = etree.fromstring(
            xml_text.encode("utf-8")
        )

    except Exception as exc:

        return {
            "valid_basic_structure": False,
            "cfdi_data": {},
            "findings": [
                {
                    "rule_id": "CFDI_XML_INVALID",
                    "type": "CFDI_STRUCTURE_ERROR",
                    "severity": "HIGH",
                    "message": f"El XML no pudo ser interpretado: {exc}"
                }
            ]
        }

    
    # 2. Comprobar nodo raíz
    

    root_name = etree.QName(root).localname

    if root_name != "Comprobante":

        add_finding(
            findings,
            "CFDI_ROOT_INVALID",
            "CFDI_STRUCTURE_ERROR",
            "HIGH",
            "El nodo raíz no corresponde a cfdi:Comprobante."
        )

    
    # 3. Datos principales del comprobante
    

    version = root.get("Version")
    subtotal = root.get("SubTotal")
    total = root.get("Total")
    fecha = root.get("Fecha")
    moneda = root.get("Moneda")
    tipo_comprobante = root.get("TipoDeComprobante")
    lugar_expedicion = root.get("LugarExpedicion")

    
    # 4. Validar versión CFDI
    

    if version != "4.0":

        add_finding(
            findings,
            "CFDI_VERSION_INVALID",
            "CFDI_STRUCTURE_ERROR",
            "HIGH",
            f"Se esperaba CFDI 4.0, pero se encontró versión {version}."
        )

    
    # 5. Campos básicos obligatorios
    

    required_root_fields = {
        "Version": version,
        "Fecha": fecha,
        "SubTotal": subtotal,
        "Moneda": moneda,
        "Total": total,
        "TipoDeComprobante": tipo_comprobante,
        "LugarExpedicion": lugar_expedicion
    }

    for field_name, value in required_root_fields.items():

        if value is None or str(value).strip() == "":

            add_finding(
                findings,
                f"CFDI_MISSING_{field_name.upper()}",
                "CFDI_MISSING_FIELD",
                "MEDIUM",
                f"Falta el atributo requerido {field_name}."
            )

    
    # 6. Buscar Emisor
    

    emisor = root.find(
        f"{{{CFDI_NS}}}Emisor"
    )

    issuer_rfc = None
    issuer_name = None

    if emisor is None:

        add_finding(
            findings,
            "CFDI_EMISOR_MISSING",
            "CFDI_STRUCTURE_ERROR",
            "HIGH",
            "No se encontró el nodo Emisor."
        )

    else:

        issuer_rfc = emisor.get("Rfc")
        issuer_name = emisor.get("Nombre")
        issuer_regime = emisor.get("RegimenFiscal")

        if not issuer_rfc:

            add_finding(
                findings,
                "CFDI_ISSUER_RFC_MISSING",
                "CFDI_MISSING_FIELD",
                "HIGH",
                "El emisor no contiene RFC."
            )

        if not issuer_regime:

            add_finding(
                findings,
                "CFDI_ISSUER_REGIME_MISSING",
                "CFDI_MISSING_FIELD",
                "MEDIUM",
                "El emisor no contiene Régimen Fiscal."
            )

    
    # 7. Buscar Receptor
    

    receptor = root.find(
        f"{{{CFDI_NS}}}Receptor"
    )

    receiver_rfc = None
    receiver_name = None

    if receptor is None:

        add_finding(
            findings,
            "CFDI_RECEPTOR_MISSING",
            "CFDI_STRUCTURE_ERROR",
            "HIGH",
            "No se encontró el nodo Receptor."
        )

    else:

        receiver_rfc = receptor.get("Rfc")
        receiver_name = receptor.get("Nombre")

        required_receiver_fields = {
            "Rfc": receiver_rfc,
            "DomicilioFiscalReceptor":
                receptor.get("DomicilioFiscalReceptor"),
            "RegimenFiscalReceptor":
                receptor.get("RegimenFiscalReceptor"),
            "UsoCFDI":
                receptor.get("UsoCFDI")
        }

        for field_name, value in required_receiver_fields.items():

            if not value:

                add_finding(
                    findings,
                    f"CFDI_RECEPTOR_{field_name.upper()}_MISSING",
                    "CFDI_MISSING_FIELD",
                    "MEDIUM",
                    f"El receptor no contiene {field_name}."
                )

    
    # 8. Conceptos
    

    conceptos_parent = root.find(
        f"{{{CFDI_NS}}}Conceptos"
    )

    conceptos = []

    if conceptos_parent is None:

        add_finding(
            findings,
            "CFDI_CONCEPTOS_MISSING",
            "CFDI_STRUCTURE_ERROR",
            "HIGH",
            "No se encontró el nodo Conceptos."
        )

    else:

        conceptos = conceptos_parent.findall(
            f"{{{CFDI_NS}}}Concepto"
        )

        if len(conceptos) == 0:

            add_finding(
                findings,
                "CFDI_CONCEPTOS_EMPTY",
                "CFDI_STRUCTURE_ERROR",
                "HIGH",
                "El CFDI no contiene conceptos."
            )

    
    # 9. Sumar importes de conceptos
    

    concept_total = Decimal("0")

    for index, concepto in enumerate(conceptos):

        importe = concepto.get("Importe")

        if importe:
            concept_total += to_decimal(
                importe
            )

        required_concept_fields = {
            "ClaveProdServ":
                concepto.get("ClaveProdServ"),
            "Cantidad":
                concepto.get("Cantidad"),
            "ClaveUnidad":
                concepto.get("ClaveUnidad"),
            "Descripcion":
                concepto.get("Descripcion"),
            "ValorUnitario":
                concepto.get("ValorUnitario"),
            "Importe":
                importe,
            "ObjetoImp":
                concepto.get("ObjetoImp")
        }

        for field_name, value in required_concept_fields.items():

            if not value:

                add_finding(
                    findings,
                    f"CFDI_CONCEPT_{index + 1}_{field_name.upper()}_MISSING",
                    "CFDI_MISSING_FIELD",
                    "MEDIUM",
                    (
                        f"El concepto {index + 1} "
                        f"no contiene {field_name}."
                    )
                )

    
    # 10. Comparar suma de conceptos vs subtotal
    

    subtotal_decimal = to_decimal(
        subtotal
    )

    if (
        conceptos
        and subtotal is not None
        and concept_total != subtotal_decimal
    ):

        difference = abs(
            concept_total - subtotal_decimal
        )

        add_finding(
            findings,
            "CFDI_SUBTOTAL_MISMATCH",
            "CFDI_AMOUNT_MISMATCH",
            "HIGH",
            (
                "La suma de los conceptos no coincide "
                "con el SubTotal del CFDI."
            ),
            calculated_subtotal=float(
                concept_total
            ),
            declared_subtotal=float(
                subtotal_decimal
            ),
            difference=float(
                difference
            )
        )

    
    # 11. Timbre Fiscal Digital
    

    complemento = root.find(
        f"{{{CFDI_NS}}}Complemento"
    )

    uuid = None
    fecha_timbrado = None

    if complemento is not None:

        timbre = complemento.find(
            f"{{{TFD_NS}}}TimbreFiscalDigital"
        )

        if timbre is not None:

            uuid = timbre.get("UUID")
            fecha_timbrado = timbre.get(
                "FechaTimbrado"
            )

    if not uuid:

        add_finding(
            findings,
            "CFDI_UUID_MISSING",
            "CFDI_STAMP_WARNING",
            "MEDIUM",
            (
                "No se encontró UUID del Timbre Fiscal Digital. "
                "Debe verificarse si se trata de un CFDI timbrado."
            )
        )

    
    # 12. SAT 69-B del emisor
    

    sat_69b = None

    if issuer_rfc:

        sat_69b = check_rfc_69b(
            issuer_rfc
        )

        if sat_69b.get("found"):

            findings.append(
                sat_69b
            )

    # 13. Datos estructurados para frontend / Gemini
    

    cfdi_data = {
        "version": version,
        "uuid": uuid,

        "issuer": {
            "rfc": issuer_rfc,
            "name": issuer_name
        },

        "receiver": {
            "rfc": receiver_rfc,
            "name": receiver_name
        },

        "fecha": fecha,
        "fecha_timbrado": fecha_timbrado,

        "subtotal": (
            float(to_decimal(subtotal))
            if subtotal is not None
            else None
        ),

        "total": (
            float(to_decimal(total))
            if total is not None
            else None
        ),

        "moneda": moneda,

        "tipo_comprobante":
            tipo_comprobante,

        "concept_count":
            len(conceptos),

        "calculated_concept_total":
            float(concept_total),

        "sat_69b":
            sat_69b
    }

    serious_findings = [
        finding
        for finding in findings
        if finding.get("severity")
        in {"HIGH", "MEDIUM"}
    ]

    return {
        "valid_basic_structure":
            len(serious_findings) == 0,

        "cfdi_data":
            cfdi_data,

        "findings":
            findings
    }