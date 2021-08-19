from decimal import Decimal, InvalidOperation

messages = {
    'correct': 'Everything is correct',
    'wrong type': 'One or more parameters have wrong type',
}


def check_animal_attributes(name,age, price, description):
    """
    function check animal attributes for correct datatype
    attrs:
        name: str
        age: int
        price: str
        description: str
    return:
        bool True if all attributes are correct, else False
    """
    if not any((isinstance(name, str), isinstance(age, int), isinstance(description, str))):
        return False, messages['wrong type']
    
    if not('.' in price and len(price.split('.')) == 2):
        return False, "Don't specified . in price or not two signs after ."

    try:
        Decimal(price)        
    except InvalidOperation:
        return False, 'Price is string or incorrect number, please, specify it as 12.53'
    
    return True, messages['correct']


def check_specie_attributes(name, description):
    """
    function check specie attributes for correct datatype
    attrs:
        name: str
        description: str
    return:
        bool True if all attributes datatypes are correct else False
    """
    if not any((isinstance(name, str), isinstance(description, str))):
        return False, messages['wrong type']
    return True, messages['correct']


def check_center_attributes(login, password, address):
    """
    function check center attributes for correct datatype
    attrs:
        login: str
        password: str
        address: str
    return:
        bool True if all attributes are correct, else False
    """
    if not any((isinstance(login, str), isinstance(password, str), isinstance(address, str))):
        return False, messages['wrong type']
    return True, messages['correct']
