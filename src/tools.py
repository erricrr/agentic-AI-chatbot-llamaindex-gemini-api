import math

session = dict()

def multiply(a: float, b: float) -> float:
    """useful tool to Multiply two numbers and returns the product
    make sure that both numbers a, b are real numbers and if not try to convert them to real numbers
    args:
        a: float
        b: float
    requires:
        only_real_numbers
    """
    return float(a) * float(b)


def add(a: float, b: float) -> float:
    """useful tool to Add two numbers and returns the sum,
    make sure that both numbers a, b are real numbers and if not try to convert them to real numbers
    args:
        a: float
        b: float

    requires:
        only_real_numbers
    """
    return float(a) + float(b)

# add complex math tools
def calculate_sin(a: float) -> float:
    """ useful tool to calculate the sin of a number
    IMPORTANT: the value of a will be in degrees, unless user specifically requests it to be in radians
    args: {"a": float}, required: True
    returns: sine of a degrees or radians if user requests
    """
    return math.sin(math.radians(float(a)))

def calculate_cos(a: float) -> float:
    """ useful tool to calculate the cos of a number
    IMPORTANT: the value of a will be in degrees, unless user specifically requests it to be in radians
    args: {"a": float}, required: True
    returns: cosine of a degrees or radians if user requests
    """
    return math.cos(math.radians(float(a)))



# add additional tools

def calculate_log(a: float) -> float:
    """ useful tool to calculate the logarithm of a number, smartly understands expects a float and returns a float and can access any other tools for solving complex problems
    args:
        a: float
    """
    return math.log(float(a))

def calculate_power(a: float, b: float) -> float:
    """ useful tool to calculate the exponential or power of a number a given the power b, smartly understands expects a float and returns a float
    detect cases like a^b and a**b route to this tool
    args:
        a: float
        b: float
    """
    return float(a) ** float(b)

def only_real_numbers(a: float) -> float:
    """ useful tool to verify if the number is real"""
    try:
        float(a)
    except ValueError:
        return f"{a} is not a real number so try converting it to a float and try again"

def convert_to_real_number(a: float) -> float:
    """ useful tool to convert a string to a real number"""
    try:
        return float(a)
    except ValueError:
        return f"{a} cannot be converted to a real number"

def miscellaneous() -> str:
    """CRITICAL: Use this tool ONLY for queries that have absolutely nothing to do with mathematics, calculations, or numerical reasoning.
    DO NOT USE THIS TOOL FOR ANY WORD PROBLEMS INVOLVING NUMBERS, QUANTITIES, RATES, TIME, MONEY, OR MEASUREMENTS.
    This tool should NOT be used for math word problems, even if they contain complex scenarios, rates, time calculations, etc.
    Math word problems should always be solved using the appropriate math tools (add, multiply, divide, etc.).
    Only use this tool for completely non-mathematical topics like politics, history, entertainment, etc.
    If there is ANY mathematical component to the query, DO NOT use this tool."""
    return "Rephrase and give this answer in words: Hi there, I can't help you with that, if you have any other maths questions please ask them"


def divide(a: float, b: float) -> float:
    """useful tool to divide two numbers and returns the quotient
    make sure that both numbers a, b are real numbers and if not try to convert them to real numbers
    args:
        a: float
        b: float
    requires:
        only_real_numbers
    """
    return float(a) / float(b)

def subtract(a: float, b: float) -> float:
    """useful tool to subtract two numbers and returns the difference
    make sure that both numbers a, b are real numbers and if not try to convert them to real numbers
    args:
        a: float
        b: float
    requires:
        only_real_numbers
    """
    return float(a) - float(b)
