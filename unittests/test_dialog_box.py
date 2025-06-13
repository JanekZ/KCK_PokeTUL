import unittest
import pygame

from engine.dialog_box import DialogBox

class TestDialogBox(unittest.TestCase):
    def setUp(self):
        pygame.init()
        font = pygame.font.Font(None, 28)
        self.dialog_box = DialogBox(0,0,120,100, font)

    def test_empty_dialog_box(self):
        self.dialog_box.set_text('')
        self.assertEqual([['']],self.dialog_box.pages)
        self.assertEqual(0,self.dialog_box.current_page)

    def test_blank_dialog_box(self):
        self.dialog_box.set_text("                          ")
        self.assertEqual([['']],self.dialog_box.pages)

    def test_dialog_box_with_one_word(self):
        self.dialog_box.set_text("Test")
        self.assertEqual([["Test"]],self.dialog_box.pages)
        self.assertFalse(self.dialog_box.has_next_page())

    def test_dialog_box_with_two_short_words(self):
        self.dialog_box.set_text("Test this")
        self.assertEqual([["Test this"]],self.dialog_box.pages)
        self.assertFalse(self.dialog_box.has_next_page())

    def test_dialog_box_with_three_short_words(self):
        self.dialog_box.set_text("Test this again")
        self.assertEqual([["Test this", "again"]],self.dialog_box.pages)

    def test_dialog_box_with_full_page(self):
        self.dialog_box.set_text("Test this again and again until it ...")
        self.assertEqual([["Test this", "again and", "again", "until it ..."]],self.dialog_box.pages)
        self.assertFalse(self.dialog_box.has_next_page())

    def test_dialog_box_with_next_page(self):
        self.dialog_box.set_text("Test this again and again until it will be correct")
        self.assertEqual([["Test this", "again and", "again", "until it"],["will be", "correct"]],self.dialog_box.pages)
        self.assertTrue(self.dialog_box.has_next_page())

    def test_dialog_box_with_next_page_and_change_to_second_page(self):
        self.dialog_box.set_text("Test this again and again until it will be correct")
        self.assertEqual([["Test this", "again and", "again", "until it"], ["will be", "correct"]],self.dialog_box.pages)
        self.assertTrue(self.dialog_box.has_next_page())
        self.assertEqual(0, self.dialog_box.current_page)
        self.dialog_box.next_page()
        self.assertEqual(1, self.dialog_box.current_page)

    def test_dialog_bot_with_different_font(self):
        font = pygame.font.Font(None, 10)
        self.dialog_box.font = font
        self.dialog_box.set_text("Test this again and again until it will be correct")
        self.assertEqual([["Test this again and again until it", "will be correct"]],
                         self.dialog_box.pages)
        self.assertFalse(self.dialog_box.has_next_page())

