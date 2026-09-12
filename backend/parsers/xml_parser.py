from lxml import etree


def parse_xml(file_bytes: bytes) -> dict:
    root = etree.fromstring(file_bytes)

    return {
        "format": "XML",
        "root_tag": root.tag,
        "attributes": dict(root.attrib),
        "xml_text": etree.tostring(
            root,
            pretty_print=True,
            encoding="unicode"
        )
    }