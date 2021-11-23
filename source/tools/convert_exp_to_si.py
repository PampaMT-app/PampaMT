'''
Tools PampaMT
Author: Patrick Rogger Garcia
Date: 2018/07/25

Class for convert number in scientific notation to number SI
'''


class NumberSI(object):

    def __init__(self):

        self.significand = ''
        self.exponent = ''
        self.unit = ''

    def read_number(self, number):
        """
        :param number: Number on format scientific notation
        :return: Set self.significand and self.exponent

        Read the number.
        """

        number = str(number)

        number = number.split('e')
        self.significand = number[0]
        self.exponent = number[1]

    def scientific_notation_to_SI(self):
        """
        Convert scientific notation in number SI, Ex.: mHz, kHz
        :return: String number SI
        """

        exponent = float(self.exponent)
        significand = float(self.significand)

        # List with [name, symbol, value]
        character = self.exponent_to_symbol()

        multiplier = -(character[2] - exponent)

        # Correct the number if exponent is different
        number_corretion = significand * (10 ** multiplier)

        # Show String, Ex.: 10 mHz, 1.886 Kg
        # print(str(round(number_corretion, 3)) + ' ' + character[1] + self.unit)

        return (str(round(number_corretion, 3)) + ' ' + character[1] + self.unit)

    def exponent_to_symbol(self):
        """
        Extract the exponent symbol
        :return: List with [name, symbol, exponent], more
        """

        exponent = float(self.exponent)

        self.cluster_of_symbol = [['femto', 'f', -15],
                                  ['pico', 'p', -12],
                                  ['nano', 'n', -9],
                                  ['micro', 'µ', -6],
                                  ['mili', 'm', -3],
                                  ['zero', ' ', +0],
                                  ['kilo', 'k', +3],
                                  ['mega', 'M', +6],
                                  ['giga', 'G', +9],
                                  ['tera', 'T', +12],
                                  ['peta', 'P', +15]]

        # Shared the nearest exponent
        i = 0
        for symbol in self.cluster_of_symbol:

            li = self.cluster_of_symbol[i][2]
            l_i = self.cluster_of_symbol[i + 1][2]

            if exponent <= self.cluster_of_symbol[0][2]:
                exponent_return = self.cluster_of_symbol[0]
                break

            elif (exponent >= li) and (exponent < l_i):
                exponent_return = symbol
                break
            else:
                exponent_return = self.cluster_of_symbol[-1]
            i += 1

        return exponent_return


if __name__ == '__main__':
    '''
    Example of use: 
    '''
    number = NumberSI()

    number.read_number('1.5258789062e-3')
    number.unit = 'Hz'
    number_convert = number.scientific_notation_to_SI()
