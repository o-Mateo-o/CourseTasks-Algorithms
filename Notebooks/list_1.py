# List 1, Algorithms_and_Data_Structures-L, WUST-F13
# Mateusz Machaj, 12.10.2021

# the file is adapted to being used as a module
# code contains also a class presentation that are executed unless the file is imported

# NOTE 'getNum' and 'getDem' method names are unconsistent with PEP, but were explicitly given in the task

"""
A module contains a fraction class for representing rational numbers in an effective way.
It has a full set of a basic methods, making the class useful to perform many operations on rational numbers.
The class presetation is executed only if the code is running as a separate file.
"""


from __future__ import annotations
from typing import Any


class Fraction():
    """
    This class allows to store and use rational numbers as 'a/b' fractions.
    It handles the basic arithmetic (+, -, *, /, abs, **) and comparison operations,
    plus provides additional features to work with fractions.
    A number will be stored as an irreducible fraction,
    where numerator is a signed integer and denominator is always a positive integer.

    Attributes:
        num (int): Irreducible fraction's numerator - signed.
        dem (int): Irreducible fraction's denominator.
        sign (int): Fractions sign, numerator's sign.
    """

    def __init__(self, num: int, dem: int = 1) -> None:
        """Constructor method.
        Create an instance of a `Fraction` class and convert it to the irreducible format.

        Args:
            num (int): Fraction's numerator.
            dem (int, optional): Fraction's denominator. Defaults to 1.

        Raises:
            TypeError: Raised when any of the arguments is not an integer.
            ValueError: Raised when the give denominator equals 0.
        """
        if not (isinstance(num, int) and isinstance(dem, int)):
            raise TypeError(
                "Both arguments - numerator and denominator - are expected to be integers.")
        if dem == 0:
            raise ValueError("Denominator cannot have a value of 0.")

        sign_check = num*dem
        if sign_check > 0:
            self.sign = 1
        elif sign_check < 0:
            self.sign = -1
        else:
            self.sign = 0

        # Euclidean algorithm to determine the GCD
        a = abs(num)
        b = abs(dem)
        if a != 0:
            while a != b:
                if a > b:
                    a -= b
                elif a < b:
                    b -= a

        self.num = self.sign * int(abs(num) / b)
        self.dem = int(abs(dem) / b)

    # -----------
    # GET METHODS
    # -----------
    def getNum(self) -> int:
        """Give the value of the numerator (signed).

        Returns:
            int: Numerator's value
        """
        return self.num

    def getDem(self) -> int:
        """Give the value of the denominator (always positive).

        Returns:
            int: Denominator's value.
        """
        return self.dem

    # -----------------------
    # INTERNAL HELPER METHODS
    # -----------------------
    def _to_common_dem(self, other: Fraction) -> tuple[int, int, int]:
        """Reduce the fractions to the common denominator.

        Args:
            other (Fraction): Other fraction.

        Returns:
            tuple[int, int, int]: (This fraction's new numerator, Other fraction's new numerator,
                                        The common denominator)
        """
        return (self.num * other.dem, self.dem * other.num, self.dem * other.dem)

    def _type_to_fract(self, other: Any) -> Fraction:
        """Make sure that the given number can be used and is the `Fraction`.
        In case the second condition is not satisfied, convert the type.

        Args:
            other (Any): Other number.

        Raises:
            TypeError: Raised when the type of `other` is different than `int` or `Fraction`. 

        Returns:
            Fraction: `other` fraction with the proper type.
        """
        if isinstance(other, Fraction):
            return other
        elif isinstance(other, int):
            return Fraction(other, 1)
        else:
            raise TypeError(
                "Inappropriate argument type. Only Fractions and integers are acceptable.")

    # ------------------
    # ADDITIONAL METHODS
    # ------------------
    def invert(self) -> Fraction:
        """Invert the given fraction.

        Returns:
            Fraction: Inverted fraction.
        """
        return Fraction(self.dem, self.num)

    def mixed_number(self, str_repr: bool = True) -> Any:
        """Find the fraction's 'mixed number' representation. Prepare the 'official', unambiguous version and the 'readable' one.

        Args:
            str_repr (bool, optional): Version of the output,
            where `True` means the standard notation and `False` stands for the dictionary of features. Defaults to True.

        Returns:
            Any: (string) representation of the mixed number if the flag is `True`, else (dict) of the mixed number features.
        """
        result = {'sign': self.sign, 'integer': abs(
            self.num) // self.dem, 'fraction': Fraction(abs(self.num) % self.dem, self.dem)}
        if str_repr:
            result['sign'] = '-' if result['sign'] == -1 else ''
            return "{}( {} + {} )".format(result['sign'], result['integer'], result['fraction'])
        else:
            return result

    # --------------------
    # ARITHMETIC OPERATORS
    # --------------------
    def __mul__(self, other: Any) -> Fraction:
        """Multiply two rational numbers. Allow the operator to do so.

        Args:
            other (Any): Other number.

        Raises:
            TypeError: Raised when the type of `other` is different than `int` or `Fraction`.

        Returns:
            Fraction: Result of a multiplication.
        """
        other = self._type_to_fract(other)
        return Fraction(self.num * other.num, self.dem * other.dem)

    def __truediv__(self, other: Any) -> Fraction:
        """Divide one rational number by the other. Allow the operator to do so.

        Args:
            other (Any): Other number.

        Raises:
            TypeError: Raised when the type of `other` is different than `int` or `Fraction`.

        Returns:
            Fraction: Result of a true division.
        """
        other = self._type_to_fract(other)
        return self * other.invert()

    def __add__(self, other: Any) -> Fraction:
        """Sum two rational numbers. Allow the operator to do so.

        Args:
            other (Any): Other number.

        Raises:
            TypeError: Raised when the type of `other` is different than `int` or `Fraction`.

        Returns:
            Fraction: Result of an addition.
        """
        other = self._type_to_fract(other)
        num_a, num_b, comm_dem = self._to_common_dem(other)
        return Fraction(num_a + num_b, comm_dem)

    def __sub__(self, other: Any) -> Fraction:
        """Subrtract the second rational number from the first one. Allow the operator to do so.

        Args:
            other (Any): Other number.

        Raises:
            TypeError: Raised when the type of `other` is different than `int` or `Fraction`.

        Returns:
            Fraction: Result of a subtraction.
        """
        other = self._type_to_fract(other)
        num_a, num_b, comm_dem = self._to_common_dem(other)
        return Fraction(num_a - num_b, comm_dem)

    def __abs__(self: Fraction) -> Fraction:
        """Calculate the absolute value of the fraction.

        Returns:
            Fraction: Absolute value of the fraction.
        """
        return Fraction(abs(self.num), self.dem)

    def __pow__(self, index: int) -> Fraction:
        """Raise a fraction to a given integer power.

        Args:
            index (int): Integer-value power index.

        Raises:
            ValueError: Raised when the index is of the `Fraction` class but is not an integer.
            TypeError: Raised when the index is neither true integer nor fraction-integer.

        Returns:
            Fraction: Fraction raised to the given power.
        """
        index_final = 1
        if isinstance(index, Fraction):
            if index.dem != 1:
                raise ValueError(
                    "The index fraction does not represent an integer value.")
            else:
                index_final = index.num
        elif isinstance(index, int):
            index_final = index
        else:
            raise TypeError(
                "Inappropriate argument type. Integers and integer-fractions are acceptable as an index.")

        if index_final < 0:
            return Fraction(self.dem**abs(index_final), self.num**abs(index_final))
        else:
            return Fraction(self.num**abs(index_final), self.dem**abs(index_final))

    # --------------------
    # COMPARISON OPERATORS
    # --------------------
    def __lt__(self, other: Any) -> bool:
        """Compare two numbers and verify if the first one is less than the second.

        Args:
            other (Any): Other number.

        Raises:
            TypeError: Raised when the type of `other` is different than `int` or `Fraction`.

        Returns:
            bool: `True` if the value of the first is lower. 
        """
        other = self._type_to_fract(other)
        num_a, num_b, comm_dem = self._to_common_dem(other)
        return True if num_a < num_b else False

    def __le__(self, other: Any) -> bool:
        """Compare two numbers and verify if the first one is less than equal to the second.

        Args:
            other (Any): Other number.

        Raises:
            TypeError: Raised when the type of `other` is different than `int` or `Fraction`.

        Returns:
            bool: `True` if the value of the first is lower or equal. 
        """
        other = self._type_to_fract(other)
        num_a, num_b, comm_dem = self._to_common_dem(other)
        return True if num_a <= num_b else False

    def __gt__(self, other: Any) -> bool:
        """Compare two numbers and verify if the first one is greater than the second.

        Args:
            other (Any): Other number.

        Raises:
            TypeError: Raised when the type of `other` is different than `int` or `Fraction`.

        Returns:
            bool: `True` if the value of the first is greater. 
        """
        other = self._type_to_fract(other)
        num_a, num_b, comm_dem = self._to_common_dem(other)
        return True if num_a > num_b else False

    def __ge__(self, other: Any) -> bool:
        """Compare two numbers and verify if the first one is greater than or equal to the second.

        Args:
            other (Any): Other number.

        Raises:
            TypeError: Raised when the type of `other` is different than `int` or `Fraction`.

        Returns:
            bool: `True` if the value of the first is greater or equal. 
        """
        other = self._type_to_fract(other)
        num_a, num_b, comm_dem = self._to_common_dem(other)
        return True if num_a >= num_b else False

    def __eq__(self, other: Any) -> bool:
        """Compare two numbers and verify if the first one is equal to the second.

        Args:
            other (Any): Other number.

        Raises:
            TypeError: Raised when the type of `other` is different than `int` or `Fraction`.

        Returns:
            bool: `True` if values are equal. 
        """
        other = self._type_to_fract(other)
        condit_num = True if self.num == other.num else False
        condit_dem = True if self.dem == other.dem else False
        return condit_num and condit_dem

    def __ne__(self, other: Any) -> bool:
        """Compare two numbers and verify if the first one is not equal to the second.

        Args:
            other (Any): Other number.

        Raises:
            TypeError: Raised when the type of `other` is different than `int` or `Fraction`.

        Returns:
            bool: `True` if values are not equal. 
        """
        other = self._type_to_fract(other)
        isequal = self == other
        return not isequal

    # --------------------
    # VISUAL REPRESENTATION
    # --------------------
    def __repr__(self) -> str:
        """Return an official representation of a stored fraction.

        Returns:
            str: String representation of a stored fraction.
        """
        return "{num}/{dem}".format(num=self.num, dem=self.dem)

    def __str__(self) -> str:
        """Return a standard printed version of a stored fraction representation.

        Returns:
            str: String representation of a stored fraction.
        """
        return self.__repr__()


# --------------------
# ----PRESENTATION----
# --------------------
if __name__ == "__main__":
    # list of example lines
    ex = [("repr(Fraction(9, 18))", '1/2'),
          ("str(Fraction(9, 18))", '1/2'),
          ("Fraction(2, -4).getDem()", 2),
          ("Fraction(2, -4).getNum()", -1),
          ("Fraction(0, -43)", Fraction(0, 1)),
          ("Fraction(-4)", Fraction(-4, 1)),
          ("Fraction(1, 2) + Fraction(1, 3)", Fraction(5, 6)),
          ("Fraction(-1, 6) - Fraction(1, 3)", Fraction(-1, 2)),
          ("Fraction(1, 2) * Fraction(1, 3)", Fraction(1, 6)),
          ("Fraction(1, -2) / Fraction(-1, 3)", Fraction(3, 2)),
          ("Fraction(1, -2) + 2", Fraction(3, 2)),
          ("Fraction(1, -2) / -2", Fraction(1, 4)),
          ("abs(Fraction(-1, 2))", Fraction(1, 2)),
          ("Fraction(3, 4)**(-2)", Fraction(16, 9)),
          ("Fraction(1, 2) < Fraction(1, 3)", False),
          ("Fraction(-1, 2) >= Fraction(1, 3)", False),
          ("Fraction(50, 2) == Fraction(25, 1)", True),
          ("Fraction(1, 15) != Fraction(1, 10)", True),
          ("Fraction(-1, 2).invert()", Fraction(-2, 1)),
          ("Fraction(-7, 3).mixed_number()", "-( 2 + 1/3 )")]

    print('CLASS PRESENTATION:\n_________________________\n')

    assert_counter = 0

    for example in ex:

        print('>>>', example[0])
        result = eval(example[0])
        print(result)
        try:
            assert result == example[1]
        except AssertionError:
            print(" --- Wrong ---")
        else:
            print(" --- Correct ---")
            assert_counter += 1
        print('\n')

    print("TARGRET USAGE TEST RESULT: ", assert_counter, '/', len(ex))
