from pydantic import BaseModel, Field


class CalculadoraNumerosNaturales(BaseModel):
    top: int = 100

    extracted: int | None = Field(None, le=100)

    def extract(self, num: int):
        if num > self.top:
            raise ValueError(f"number greater than top (top:{self.top}, num:{num})")

        self.extracted = num

    def calculate_missing(self):
        if self.extracted is None:
            raise ValueError("extracted number not defined")

        number_set = self._get_number_set()

        i = 0

        for number in number_set:
            # verifica que no haya IndexError
            if i >= len(number_set) - 1:
                break

            if number + 1 != number_set[i + 1]:
                return number + 1

            # if number_set[i] + 1 != number_set[i + 1]:
            #     return number_set[i] + 1

            i += 1

        return self.top  #

    def _get_number_set(self):
        if self.extracted is None:
            raise ValueError("extracted number not defined")

        return [i for i in range(0, self.top + 1) if i != self.extracted]


if __name__ == "__main__":
    calc = CalculadoraNumerosNaturales(top=100)
    calc.extract(100)

    print(calc.calculate_missing())
