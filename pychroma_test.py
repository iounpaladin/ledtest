import random

from pychroma import Sketch, Controller


class TestSketch(Sketch):
  config_path = "config.json"

  def setup(self):
    self.frame_rate = 30
    self.keyboard.color_mode('hsv-normalized')
    self.mouse.color_mode('hsv-normalized')
    self.highlights = {
      'keyboard': {},
      'mouse': {}
    }
    self.decrease = 0.1
    self.color = 1/3
    self.fixed_names = {
      'left': 'left_strip',
      'middle': 'scroll',
      'right': 'right_strip'
    }

  def on_key_press(self, key):
    self.highlights['keyboard'][key] = 1

  def on_key_release(self, key):
    self.highlights['keyboard'][key] = 0.99

  def on_mouse_press(self, button):
    self.highlights['mouse'][self.fixed_names[button]] = 1

  def on_mouse_release(self, button):
    self.highlights['mouse'][self.fixed_names[button]] = 0.99

  def on_mouse_move(self, pos):
    self.highlights['mouse']['logo'] = 0.99

  def on_mouse_scroll(self, delta):
    self.highlights['mouse']['scroll'] = 0.99

  def update(self):
    self.color = random.random()

  def render(self):
        self.mouse.set_static((self.color, 1, 1))


with Controller('config.json') as controller:
    controller.run_sketch(TestSketch)
