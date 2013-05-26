from unittest import TestCase
from firevalidator import *
from firevalidator.utils import length


class TestValidator(TestCase):

    int_validator = Validator(int, {
        C >= 5: "Number is too small",
        C % 2: "Number must be odd",
        C < 10: "Number is too big",
    })

    postal_validator = Validator(lambda s: s.split('-'), {
        length(C) == 2: 'Invalid format',
        C[0].isdigit(): 'First part isn\'t a number',
        C[1].isdigit(): 'Second part isn\'t a number',
        length(C[0]) == 2: 'First number hasn\'t equals two chars',
        length(C[1]) == 3: 'Second number hasn\'t equals three chars'
    }, lambda l: '-'.join(l))

    weird_validator = Validator(int, float, str)

    def test_valid_int(self):
        for i in ('5', 5, 7.0, '9'):
            x = self.int_validator.validate(i)
            self.assertIsInstance(x, int)

    def test_invalid_int(self):
        with self.assertRaises(ValidationError) as cm:
            self.int_validator.validate('4')

        self.assertEqual(cm.exception.message, "Number is too small")

        with self.assertRaises(ValidationError) as cm:
            self.int_validator.validate('6')

        self.assertEqual(cm.exception.message, "Number must be odd")

        with self.assertRaises(ValidationError) as cm:
            self.int_validator.validate(11)

        self.assertEqual(cm.exception.message, "Number is too big")

    def test_valid_postal(self):
        for s in ('23-123', '05-333', '69-666'):
            x = self.postal_validator.validate(s)
            self.assertIsInstance(x, str)

    def test_invalid_postal(self):
        with self.assertRaises(ValidationError) as cm:
            self.postal_validator.validate('XX.123')

        self.assertEqual(cm.exception.message, 'Invalid format')

        with self.assertRaises(ValidationError) as cm:
            self.postal_validator.validate('XX-123')

        self.assertEqual(cm.exception.message, 'First part isn\'t a number')

        with self.assertRaises(ValidationError) as cm:
            self.postal_validator.validate('12-XXX')

        self.assertEqual(cm.exception.message, 'Second part isn\'t a number')

        with self.assertRaises(ValidationError) as cm:
            self.postal_validator.validate('123-123')

        self.assertEqual(
            cm.exception.message, 'First number hasn\'t equals two chars')

        with self.assertRaises(ValidationError) as cm:
            self.postal_validator.validate('12-12')

        self.assertEqual(
            cm.exception.message, 'Second number hasn\'t equals three chars')

    def test_valid_weird(self):
        self.assertEqual(self.weird_validator.validate(5), '5.0')
        self.assertEqual(self.weird_validator.validate(5.5), '5.0')
        self.assertEqual(self.weird_validator.validate('5'), '5.0')

    def test_invalid_weird(self):
        self.assertNotEqual(self.weird_validator.validate(5), 5.0)
        self.assertNotEqual(self.weird_validator.validate(5.5), '5')
