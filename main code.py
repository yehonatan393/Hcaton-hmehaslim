import arcade
import arcade.gui
import random
import arabic_reshaper
from bidi.algorithm import get_display

def fix_hebrew(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def wrap_text(text, max_chars):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            lines.append('')
            current_line = word

    lines.append(current_line.strip())
    return lines


description_text = """ברוכים הבאים למשחק זיהוי AI!
לפניכם יוצגו זוגות של תמונות – אחת אמיתית ואחת שנוצרה על ידי בינה מלאכותית.
המשימה שלכם: ללחוץ על התמונה שלדעתכם היא האמיתית.
שימו לב לפרטים הקטנים: אצבעות, השתקפויות וטקסטורות מוזרות...
ה-AI לא תמיד מושלם!"""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pics = [{'Ai':r"assets/WhatsApp Image 2026-04-13 at 17.31.58.jpeg",'real':r"assets/WhatsApp Image 2026-04-13 at 17.31.58 (1).jpeg"},
        {'Ai':r"assets/WhatsApp Image 2026-04-13 at 17.31.58 (2).jpeg",'real':r"assets/WhatsApp Image 2026-04-13 at 17.31.58 (3).jpeg"},
        {'Ai':r"assets/WhatsApp Image 2026-04-13 at 17.31.59.jpeg",'real':r"assets/WhatsApp Image 2026-04-13 at 17.31.59 (1).jpeg"}]

player_points = 0

class View1(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture(r"assets/WhatsApp Image 2026-04-13 at 17.36.55.jpeg")
        #start button
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        start_button = arcade.gui.UIFlatButton(text='Start', width=100, height=50, style={"normal": {"bg_color": arcade.color.GREEN},"hover": {"bg_color": arcade.color.DARK_GREEN},"press": {"bg_color": arcade.color.DARK_YELLOW}})
        start_button.center_x = SCREEN_WIDTH - 150
        start_button.center_y = 50
        start_button.on_click = self.continue_to_view2
        self.manager.add(start_button)

    def continue_to_view2 (self, event):
        self.window.show_view(View2())

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,arcade.rect.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        arcade.draw.draw_lbwh_rectangle_filled(0,0,SCREEN_WIDTH,100,arcade.color.DARK_BLUE)
        self.manager.draw()

        #להוסיף את הברוכים הבאים

class View2(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_CYAN)

        #continue button
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        continue_button = arcade.gui.UIFlatButton(text='continue', width=100, height=50, style={"normal": {"bg_color": arcade.color.GREEN},"hover": {"bg_color": arcade.color.DARK_GREEN},"press": {"bg_color": arcade.color.DARK_YELLOW},})
        continue_button.center_x = SCREEN_WIDTH - 150
        continue_button.center_y = 75
        continue_button.on_click = self.continue_to_view3
        self.manager.add(continue_button)

    def continue_to_view3(self, event):
        self.window.show_view(View3())

    def on_draw(self):
        self.clear()

        y = SCREEN_HEIGHT - 100
        paragraphs = description_text.split("\n")

        for paragraph in paragraphs:
            lines = wrap_text(paragraph, 50)

            for line in lines:
                fixed_line = fix_hebrew(line)
                arcade.draw_text(fixed_line,SCREEN_WIDTH - 50,y,arcade.color.BLACK,14,anchor_x="right")
                y -= 25
                y -= 10
        self.manager.draw()

class View3(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_YELLOW)
        arcade.AI = ''
        arcade.real = ''
        self.AI = r'assets/WhatsApp Image 2026-04-13 at 17.31.59.jpeg'
        self.real = r'assets/WhatsApp Image 2026-04-13 at 17.31.59 (1).jpeg'

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        txture = arcade.load_texture(self.AI)
        self.AI_button = arcade.gui.UITextureButton(texture=txture,
                                               width=SCREEN_WIDTH * 0.4,
                                               height=SCREEN_HEIGHT* 0.7,
                                               x= SCREEN_WIDTH//9,
                                               y=SCREEN_HEIGHT//6)
        self.manager.add(self.AI_button)
        self.txture2 = arcade.load_texture(self.real)
        self.real_button = arcade.gui.UITextureButton(texture=self.txture2,
                                                    width=SCREEN_WIDTH *0.4,
                                                    height=SCREEN_HEIGHT * 0.7,
                                                    x= SCREEN_WIDTH * 0.57 ,
                                                 y= SCREEN_HEIGHT//6)
        self.manager.add(self.real_button)
        self.real_button.on_click = self.real_button_pressed
        self.AI_button.on_click = self.AI_button_pressed

    def real_button_pressed(self, event):
        self.run_pics()
        self.clear()

    def AI_button_pressed(self, event):
        self.run_pics()
        self.clear()

    def run_pics(self):
        selected_pictures = random.choice(pics)
        AI_picture = selected_pictures['Ai']
        real_picture = selected_pictures['real']
        self.AI = arcade.load_texture(AI_picture)
        self.real= arcade.load_texture(real_picture)
        self.real_button.texture = self.real
        self.real_button.texture_pressed = self.real
        self.real_button.texture_hovered = self.real
        self.AI_button.texture = self.AI
        self.AI_button.texture_pressed = self.AI
        self.AI_button.texture_hovered = self.AI

    def on_draw(self) :
        self.clear()
        self.manager.draw()

window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,'Hacaton project 2026')
window.show_view(View1())
arcade.run()