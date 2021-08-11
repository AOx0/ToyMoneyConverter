converter_money = {
    'usd' = 1,
    'mxn' = 20.01,
    'euros' = 0.85,
    'pounds' = 0.72
}

def converter(amount, money_have, money_want, diccionario) -> float:
    return converter_1(amount(money_have)/amount(money_want), diccionario)


