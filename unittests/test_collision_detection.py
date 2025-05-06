import unittest

import pygame.sprite

from dynamic_entity import DynamicEntity
from dynamic_entity import StaticEntity

from algorithms.collision_detection import CollisionDetection

class TestCollisionDetection(unittest.TestCase):
    def setUp(self):
        self.character = DynamicEntity(100, 100, 50, 50, (100, 200, 100))
        self.d_x, self.d_y = (1, 0)
        #FULL COVER
        self.box1 = StaticEntity(101, 100, 50, 50, (100, 200, 100))
        #PARTIAL COVER
        self.box2 = StaticEntity(150, 100, 50, 50, (100, 200, 100))
        #NO TOUCH
        self.box3 = StaticEntity(201, 100, 50, 50, (100, 200, 100))

        self.boxes = pygame.sprite.Group()
        self.boxes.add(self.box1)
        self.boxes.add(self.box2)
        self.boxes.add(self.box3)

        self.detect = CollisionDetection(self.character, (self.d_x, self.d_y))

    def test_cloning(self):
        clone = self.detect.create_clone()
        self.assertIsInstance(clone, DynamicEntity)
        self.assertNotEqual(clone, self.character)
        self.assertEqual( (clone.width, clone.height), (self.character.width, self.character.height) )
        self.assertEqual(clone.color, self.character.color)
        self.assertNotEqual( (clone.x, clone.y), (self.character.x, self.character.y) )
        self.assertEqual( (clone.x, clone.y), (self.character.x + self.d_x, self.character.y + self.d_y) )

    def test_collisions(self):
        self.assertTrue(self.detect.check_collision(self.boxes)[0])
        self.assertEqual(self.detect.check_collision(self.boxes)[1], 2)

        self.boxes.remove(self.box1)
        self.assertTrue(self.detect.check_collision(self.boxes)[0])
        self.assertEqual(self.detect.check_collision(self.boxes)[1], 1)

        self.boxes.remove(self.box2)
        self.assertFalse(self.detect.check_collision(self.boxes)[0])
        self.assertEqual(self.detect.check_collision(self.boxes)[1], 0)

    def test_out_of_bounds(self):
        #BOX INSIDE
        box = StaticEntity(50, 50, 50, 50, (100,200,100))
        #BOX ON EDGE
        box2 = StaticEntity(0, 0, 50, 50, (100, 200, 100))
        #BOX HALF OUT
        box3 = StaticEntity(-25, -25, 50, 50, (100, 200, 100))
        #BOX COMPLETELY OUT
        box4 = StaticEntity(300, 300, 50, 50, (100, 200, 100))

        self.d_x, self.d_y = (1, 0)

        #BOUNDING BOX
        bounds = StaticEntity(0, 0, 200, 200, (100, 200, 100))

        boundaries = pygame.sprite.Group()
        boundaries.add(bounds)

        # CHECK IF BOX INSIDE IS PROCESSED PROPERLY
        check = CollisionDetection(box,(self.d_x, self.d_y))
        is_collision, _ = check.check_collision(boundaries)
        self.assertTrue(is_collision)
        is_out = check.check_out_of_bounds(boundaries)
        self.assertFalse(is_out)

        # CHECK IF BOX INSIDE ON THE EDGE IS PROCESSED PROPERLY
        check = CollisionDetection(box2, (self.d_x, self.d_y))
        is_collision, _ = check.check_collision(boundaries)
        self.assertTrue(is_collision)
        is_out = check.check_out_of_bounds(boundaries)
        self.assertFalse(is_out)

        # CHECK IF BOX HALF INSIDE HALF OUTSIDE IS PROCESSED PROPERLY
        check = CollisionDetection(box3, (self.d_x, self.d_y))
        is_collision, _ = check.check_collision(boundaries)
        self.assertTrue(is_collision)
        is_out = check.check_out_of_bounds(boundaries)
        self.assertTrue(is_out)

        # CHECK IF BOX OUTSIDE IS PROCESSED PROPERLY
        check = CollisionDetection(box4, (self.d_x, self.d_y))
        is_collision, _ = check.check_collision(boundaries)
        self.assertFalse(is_collision)
        is_out = check.check_out_of_bounds(boundaries)
        self.assertTrue(is_out)


if __name__ == "__main__":
    unittest.main()