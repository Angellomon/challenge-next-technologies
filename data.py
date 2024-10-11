import csv
from typing import TypeAlias

DEFAULT_DATA_FILENAME = "data_prueba_tecnica.csv"

RowType: TypeAlias = list[str]
HeaderType: TypeAlias = list[str]
JSONElementType: TypeAlias = dict[str, str]


def get_headers_and_data_from_csv(
    filename: str = DEFAULT_DATA_FILENAME, headers_row: int = 0
) -> tuple[HeaderType, list[RowType]]:
    with open(
        filename,
        mode="r",
    ) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        line_count = 0
        headers = []
        data = []

        for row in csv_reader:
            if line_count == headers_row:
                headers = row.copy()

                line_count += 1
                continue

            if len(row) == 0:
                continue

            data.append(row.copy())

            line_count += 1

        print(line_count)

    return headers, data


def validate_data_structure(headers: HeaderType, data: list[RowType]):
    length_error = ValueError("Headers length is different from Data's row length")

    # maybe consider validate all data
    # for row in data:
    #     if len(headers) != len(row)
    #         raise length_error

    if len(headers) != len(data[0]):
        raise length_error


def transform_data_to_json(
    headers: HeaderType, data: list[RowType]
) -> list[JSONElementType]:
    validate_data_structure(headers, data)

    json_data = []

    for row in data:
        json_data.append(dict(zip(headers, [el if el != "" else None for el in row])))

    return json_data
