from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy import platform
from kivy.clock import Clock
from kivy,animation import Animation

# Розмір вікна (для ПК)
Window.size = (450, 700)

# Класи для екранів
class MenuScreen(Screen):
    def go_game(self):
        self.manager.current = "game"

    def go_settings(self):
        self.manager.current = "settings"

    def exit_app(self):
        App.get_running_app().stop()

class GameScreen(Screen):
    score = NumericProperty(0)
    def on_pre_enter(self, *args):
        self.score = 0
        self.ids.click_label.text = 'Clicks: 0'
        self.ids.level_complete.opacity = 0
        app = App.get_running_app()
        app.LEVEL = 0
        self.ids.fish.fish_index = 0
        return super().on_pre_enter(*args)
    
    def on_enter(self, *args):
        self.start_game()
        return super().on_enter(*args)
    
    def start_game(self):
        self.ids.new_fish()
    
    def level_complete(self, *args):
        self.ids.level_complete.opacity = 1
    
    def go_menu(self):
        self.manager.current = "menu"

class SettingsScreen(Screen):
    def go_menu(self):
        self.manager.current = "menu"

class Fish(Image):

    anim_play = False
    interraction_block = True
    COEF_MULT= 1.5
    angle = NumericProperty
    fish_current = None
    fish_index = 0
    hp_current = 0

    def on_kv_post(self,base_widget):
        self.GAME_SCREEN = self.parent.parent.parent
        return super().on_kv_post(base_widget)


    def on_touch_down(self, touch):
        if self.hp_current <= 0:
            self.defeated()
        if not self.collide_point(*touch.pos) or not self.opacity:
            self.hp_current -= 1
            self.GAME_SCREEN.score += 1
            self.GAME_SCREEN.ids.click_label.text = f"Clicks: {self.GAME_SCREEN.score}"    
        return super().on_touch_down(touch)
    
    def defeated(self):

        self.interraction_block=True
        anim = Animation(angle=self.angle +360,d = 1,t = "in_cubic")
        old_size= self.size.copy()
        old_pos = self.pos.copy()
        new_size= (self.size[0]*self.COEF_MULT*3,self.size[1]*self.COEF_MULT*3)
        new_pos = (self.pos[0]-(new_size[0]-self.size[0])/2,self.pos[1]-(new_size[1]-self.size[1])/2)
        anim &= Animation(size =(new_size),t = "im_out_bounce") + Animation(size = (old_size),duraction = 0)
        anim &= Animation(pos = (new_pos), t = "im_out_bounce") + Animation(pos =(old_pos),duraction =  0)
        anim &=Animation(opacity =0)
        anim.start(self)
    def swim(self):
        self.pos = (self.GAME_SCREEN.x-self.width,self.DAME_SCREEN.height /2)
        self.opacity = 1
        swim =Animation(x =self.GAME_SCREEN.width/2 - self.width/2,duraqction =1)
        swim.start(self)
        swim.blind(on_complate = lambda w,a:setattr(self,"interraction_block",False))

    def new_fish(self, *args):
        app = App.get_running_app()
        self.fish_current = app.LEVELS[app.LEVEL][self.fish_index]
        self.source = app.FISHES[self.fish_current]['source']
        self.hp_current = app.FISHES[self.fish_current]['hp']
        self.swim


# Головний застосунок
class ClickerApp(App):
    LEVEL = 0
    FISHES = {
        'fish1': {'source': 'fish1.png'},
        'fish2': {'source': 'fish2.jpg'}
    }
    LEVELS = [
        ['fish1', 'fish2']
    ]
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm

app = ClickerApp()
app.run()