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
האם העיניים שלכם חדות מספיק כדי להבדיל בין מציאות לזיוף?
לפניכם יוצגו זוגות של תמונות – אחת אמיתית ואחת שנוצרה על ידי בינה מלאכותית.
המשימה שלכם: ללחוץ על התמונה שלדעתכם היא האמיתית.
שימו לב לפרטים הקטנים: אצבעות, השתקפויות וטקסטורות מוזרות...
ה-AI לא תמיד מושלם!"""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pics = [{'Ai':r"assets/WhatsApp Image 2026-04-13 at 17.31.58.jpeg",'real':r"assets/WhatsApp Image 2026-04-13 at 17.31.58 (1).jpeg"},
        {'Ai':r"C:\Users\USER\Downloads\HACATON\WhatsApp Image 2026-03-16 at 7.32.56 PM.jpeg",'real':r"C:\Users\USER\Downloads\HACATON\WhatsApp Image 2026-03-16 at 7.34.25 PM.jpeg"},
        {'Ai':r"C:\Users\USER\Downloads\HACATON\WhatsApp Image 2026-03-16 at 7.42.45 PM.jpeg",'real':r"C:\Users\USER\Downloads\HACATON\WhatsApp Image 2026-03-16 at 7.38.44 PM.jpeg"},
        {'Ai':r"C:\Users\USER\Downloads\HACATON\WhatsApp Image 2026-03-16 at 7.52.12 PM.jpeg",'real':r"C:\Users\USER\Downloads\HACATON\WhatsApp Image 2026-03-16 at 7.53.45 PM.jpeg"}]

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
        self.manager.draw()

        lines = wrap_text(description_text, 40)

        y = SCREEN_HEIGHT - 100
        for line in lines:
            bidi_line = fix_hebrew(line)
            arcade.draw_text(bidi_line,700, y,arcade.color.BLACK,30,anchor_x="right")
            y -= 25

        #להוסיף את ההסבר על המשחק

class View3(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_YELLOW)
        arcade.AI = ''
        arcade.real = ''

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        continue_button = arcade.gui.UIFlatButton(text='continue', width=100, height=50, style={"normal": {"bg_color": arcade.color.GREEN},"hover": {"bg_color": arcade.color.DARK_GREEN},"press": {"bg_color": arcade.color.DARK_YELLOW},})
        continue_button.center_x = SCREEN_WIDTH - 150
        continue_button.center_y = 75
        continue_button.on_click = self.run_pics,
        self.manager.add(continue_button)

        AI_button = arcade.gui.UITextureButton()

    def run_pics(self):
        selected_pictures = random.choice(pics)
        AI_picture = selected_pictures['AI']
        real_picture = selected_pictures['real']
        self.AI = arcade.load_texture(AI_picture,)
        self.real= arcade.load_texture(real_picture)

    def on_draw(self) :
        self.clear()
        self.manager.draw()


        arcade.draw_lrbt_rectangle_filled(100,350,150,)
window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,'Hacaton project 2026')
window.show_view(View1())
arcade.run()