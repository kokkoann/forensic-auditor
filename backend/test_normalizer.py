from parsers.file_parser import parse_file
from normalizers.transaction_normalizer import normalize_transactions


with open("../test_transactions_normalizer.csv", "rb") as file:
    content = file.read()


document = parse_file(
    "test_transactions_normalizer.csv",
    content
)


result = normalize_transactions(
    document
)


print("\n=========================")
print("DOCUMENTO ORIGINAL")
print("=========================")

print(document)


print("\n=========================")
print("NORMALIZADO")
print("=========================")

print(result)