import unittest

import pygame.sprite

from dynamic_entity import DynamicEntity
from dynamic_entity import StaticEntity

from Algorithms.collision_detection import CollisionDetection

class TestCollisionDetection(unittest.TestCase):
    def setUp(self):
        self.character = DynamicEntity()
        self.character.set_position(100, 100)
        self.character.set_dimensions(50, 50)
        self.character.set_image((100, 200, 100))
        self.character.set_rect()
        self.d_x, self.d_y = (1, 0)
        #FULL COVER
        self.box1 = StaticEntity()
        self.box1.set_position(101, 100)
        self.box1.set_dimensions(50, 50)
        self.box1.set_image((100, 200, 100))
        self.box1.set_rect()
        #PARTIAL COVER
        self.box2 = StaticEntity()
        self.box2.set_position(150, 100)
        self.box2.set_dimensions(50, 50)
        self.box2.set_image((100, 200, 100))
        self.box2.set_rect()
        #NO TOUCH
        self.box3 = StaticEntity()
        self.box3.set_position(201, 100)
        self.box3.set_dimensions(50, 50)
        self.box3.set_image((100, 200, 100))
        self.box3.set_rect()
        self.boxes = pygame.sprite.Group()
        self.boxes.add(self.box1)
        self.boxes.add(self.box2)
        self.boxes.add(self.box3)

        self.detect = CollisionDetection(self.character, self.boxes, (self.d_x, self.d_y))

    def test_cloning(self):
        clone = self.detect.create_clone()
        self.assertIsInstance(clone, DynamicEntity)
        self.assertNotEqual(clone, self.character)
        self.assertEqual( (clone.width, clone.height), (self.character.width, self.character.height) )
        self.assertEqual(clone.color, self.character.color)
        self.assertNotEqual( (clone.x, clone.y), (self.character.x, self.character.y) )
        self.assertEqual( (clone.x, clone.y), (self.character.x + self.d_x, self.character.y + self.d_y) )

    def test_collisions(self):
        self.assertTrue(self.detect.check_collision()[0])
        self.assertEqual(self.detect.check_collision()[1], 2)

        self.boxes.remove(self.box1)
        self.assertTrue(self.detect.check_collision()[0])
        self.assertEqual(self.detect.check_collision()[1], 1)

        self.boxes.remove(self.box2)
        self.assertFalse(self.detect.check_collision()[0])
        self.assertEqual(self.detect.check_collision()[1], 0)

if __name__ == "__main__":
    unittest.main()