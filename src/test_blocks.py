import unittest

from blocks import BlockType, block_to_block_type

class TestBlocks(unittest.TestCase):
    def test_paragraph(self):
        block = "This is just a paragraph."
        expected_out = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_heading1(self):
        block = "# This is a heading."
        expected_out = BlockType.HEADING
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_heading2(self):
        block = "#### This is also a heading."
        expected_out = BlockType.HEADING
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_heading3(self):
        block = "###### This as well is a heading."
        expected_out = BlockType.HEADING
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_heading4(self):
        block = "####### This, however, is not one."
        expected_out = BlockType.HEADING
        self.assertNotEqual(block_to_block_type(block), expected_out)
    
    def test_code1(self):
        block = "```This is code```"
        expected_out = BlockType.CODE
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_code2(self):
        block = "```This is not code`` "
        expected_out = BlockType.CODE
        self.assertNotEqual(block_to_block_type(block), expected_out)

    def test_code3(self):
        block = "This is not code either``` "
        expected_out = BlockType.CODE
        self.assertNotEqual(block_to_block_type(block), expected_out)

    def test_code4(self):
        block = "Neither is this ``````"
        expected_out = BlockType.CODE
        self.assertNotEqual(block_to_block_type(block), expected_out)

    def test_quote1(self):
        block = "> This is a quote"
        expected_out = BlockType.QUOTE
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_quote2(self):
        block = ">This is also a quote"
        expected_out = BlockType.QUOTE
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_quote3(self):
        block = "> This is also a quote\n> And so is this"
        expected_out = BlockType.QUOTE
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_quote4(self):
        block = "> This is also a quote\nBut not this"
        expected_out = BlockType.QUOTE
        self.assertNotEqual(block_to_block_type(block), expected_out)

    def test_unord_list1(self):
        block = "* This is a list\n* With this"
        expected_out = BlockType.UNORD_LIST
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_unord_list2(self):
        block = "- This works\n- As well"
        expected_out = BlockType.UNORD_LIST
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_unord_list3(self):
        block = "* This is a list\n- With this"
        expected_out = BlockType.UNORD_LIST
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_unord_list4(self):
        block = "* This is a list\n* With this"
        expected_out = BlockType.UNORD_LIST
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_unord_list5(self):
        block = "* This is wrong however\n."
        expected_out = BlockType.UNORD_LIST
        self.assertNotEqual(block_to_block_type(block), expected_out)

    def test_unord_list6(self):
        block = "*As well as this."
        expected_out = BlockType.UNORD_LIST
        self.assertNotEqual(block_to_block_type(block), expected_out)

    def test_unord_list7(self):
        block = "*- As well as this."
        expected_out = BlockType.UNORD_LIST
        self.assertNotEqual(block_to_block_type(block), expected_out)

    def test_ord_list1(self):
        block = "1. This is\n2. An ordered\n3. List"
        expected_out = BlockType.ORD_LIST
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_ord_list2(self):
        block = "3. This is\n4. An ordered\n5. List"
        expected_out = BlockType.ORD_LIST
        self.assertEqual(block_to_block_type(block), expected_out)

    def test_ord_list3(self):
        block = "1. This\n2. Should\n2. Not work."
        expected_out = BlockType.ORD_LIST
        self.assertNotEqual(block_to_block_type(block), expected_out)

    def test_ord_list4(self):
        block = "1. Neither\n3. Should\n4. This"
        expected_out = BlockType.ORD_LIST
        self.assertNotEqual(block_to_block_type(block), expected_out)

    def test_ord_list5(self):
        block = "1.This is also illegal"
        expected_out = BlockType.ORD_LIST
        self.assertNotEqual(block_to_block_type(block), expected_out)

