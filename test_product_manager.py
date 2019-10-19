from unittest import TestCase
import unittest
from abstract_product import AbstractProduct
from computer import Computer
from cellphone import Cellphone
from product_manager import ProductManager
import re
import inspect

class TestProductManager(TestCase):

    _product_manager = None

    def setUp(self):
        self.logPoint()
        self._product_manager = ProductManager()

        computer1 = Computer(1, "Huawei Matebook X Pro", 1600, 1200, "07/18/2019", "08/21/2019", True, "Nvidia Geforce", "Dbrand", "DDR4")
        self._product_manager.add(computer1)

        cellphone5 = Cellphone(5, "Pixel 4", 1000, 500, "03/21/2018", "04/21/2019", True, "G Camera", "Google Lock", 88)
        self._product_manager.add(cellphone5)

    def logPoint(self):
        currentTest= self.id().split('.')[-1]
        callingFunction= inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))

    def tearDown(self):
        products = self._product_manager.get_all()
        ids = []
        
        for product in products:
            id = product.get_id()
            ids.append(id)

        for id in ids:
            self._product_manager.delete(id)

        self._product_manager = None
    
    def test_add(self):
        """ 010A - Valid add """
        all_products = self._product_manager.get_all()
        self.assertTrue(len(all_products) == 2)
        """Add to products"""
        computer3 = Computer(3, "Macbook Pro", 2000, 1500, "05/19/2019", "09/22/2019", True, "A13 Bionic", "Dbrand", "DDR4")
        self._product_manager.add(computer3)
        all_products = self._product_manager.get_all()
        self.assertTrue(len(all_products) == 3)

    def test_add_invalid(self):
        """ 010B - Invalid add """
        undefined_computer = None
        self.assertRaisesRegex(ValueError, "Product cannot be none.", self._product_manager.add, undefined_computer)
    
    def test_get(self):
        """ 020A - Valid get """
        computer1 = self._product_manager.get(1)
        self.assertEqual("Huawei Matebook X Pro", computer1.get_name())

        cellphone5 = self._product_manager.get(2)
        self.assertEqual("Pixel 4", cellphone5.get_name())

    def test_get_invalid(self):
        """ 020B - Invalid get """
        not_number_id = "not number"
        self.assertRaisesRegex(ValueError, "ID is not a number!", self._product_manager.get, not_number_id)

    def test_get_all(self):
        """ 030A - Valid get_all """
        products = self._product_manager.get_all()
        self.assertEqual(2, len(products))
        for product in products:
            product_name = product.get_name()
            if product.get_id() == 1:
                self.assertEqual("Huawei Matebook X Pro", product_name)
            if product.get_id() == 2:
                self.assertEqual("Pixel 4", product_name)

    def test_get_all_by_type(self):
        """ 040A - Valid get_all_by_type """
        computers = self._product_manager.get_all_by_type(AbstractProduct.COMPUTER_TYPE)
        cellphones = self._product_manager.get_all_by_type(AbstractProduct.CELLPHONE_TYPE)
        self.assertEqual(1, len(computers))
        self.assertEqual(1, len(cellphones))
        self.assertEqual("Huawei Matebook X Pro", computers[0].get_name())
        self.assertEqual("Pixel 4", cellphones[0].get_name())

    def test_get_all_by_type_invalid(self):
        """ 040B - Invalid get_all_by_type """
        undefined_type = None
        self.assertRaisesRegex(ValueError, "Type cannot be undefined.", self._product_manager.get_all_by_type, undefined_type)

    def test_update(self):
        """ 050A - Valid update """
        computers = self._product_manager.get_all_by_type(AbstractProduct.COMPUTER_TYPE)
        computer1 = computers[0]
        old_computer_price = computer1.get_price()
        new_computer_price = old_computer_price + 100
        #new_computer1 = Computer(1, "Huawei Matebook X Pro", new_computer_price, 1200, 7/21/19, 8/23/19, True, "Nvidia Geforce", "Dbrand", "DDR4")
        new_computer1 = Computer(\
            computer1.get_id(),\
            computer1.get_name(),\
            new_computer_price,\
            computer1.get_cost(),\
            computer1.get_date_stocked(),\
            computer1.get_date_sold(),\
            computer1.get_is_sold(),\
            computer1.get_graphics_card(),\
            computer1.get_case(),\
            computer1.get_memory_type())
        self._product_manager.update(new_computer1)
        updated_computer = self._product_manager.get(1)

        self.assertEqual(computer1.get_id(), updated_computer.get_id())
        self.assertEqual(computer1.get_name(), updated_computer.get_name())
        self.assertNotEqual(computer1.get_price(), updated_computer.get_price())
        self.assertEqual(new_computer_price, updated_computer.get_price())

    def test_update_invalid(self):
        """ 050B - Invalid update """
        undefined_computer = None
        self.assertRaisesRegex(ValueError, "Product cannot be none.", self._product_manager.update, undefined_computer)

    def test_delete(self):
        """ 060A - Valid delete """
        products = self._product_manager.get_all()
        computer1 = products[0]
        self.assertEqual(AbstractProduct.COMPUTER_TYPE, computer1.get_type())
        self.assertEqual(1, computer1.get_id())
        self.assertEqual("Huawei Matebook X Pro", computer1.get_name())

        id = computer1.get_id()
        
        self._product_manager.delete(id)
    
        deleted = True
        products = self._product_manager.get_all()
        for product in products:
            if product.get_id() == id:
                deleted = False
                break

        self.assertTrue(deleted)

    def test_delete_invalid(self):
        """ 060B - Invalid delete """
        not_number_id = "not number"
        self.assertRaisesRegex(ValueError, "ID is not a number!", self._product_manager.delete, not_number_id)

if __name__ == "__main__":
    unittest.main()
