from analysis.blacklist_69b import check_rfc_69b


tests = [
    "AAA080808HL8",
    "AAA120730823",
    "AAA121206EV5",
    "RFCQUE_NO_EXISTE"
]


for rfc in tests:
    result = check_rfc_69b(rfc)

    print("\n------------------")
    print(result)