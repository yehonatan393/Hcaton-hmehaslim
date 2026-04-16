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

description_text_view1 = 'ברוך הבא!'

description_text_view2 = """ברוכים הבאים למשחק זיהוי AI!
לפניכם יוצגו זוגות של תמונות – אחת אמיתית ואחת שנוצרה על ידי בינה מלאכותית.
המשימה שלכם: ללחוץ על התמונה שלדעתכם היא האמיתית.
שימו לב לפרטים הקטנים: אצבעות, השתקפויות וטקסטורות מוזרות...
ה-AI לא תמיד מושלם!"""

description_text_view3='לחצו על התמונה האמיתית'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pics = [{'num':1,'Ai':r"assets/WhatsApp Image 2026-04-13 at 17.31.58.jpeg",'real':r"assets/WhatsApp Image 2026-04-13 at 17.31.58 (1).jpeg",'clue':''},
        {'num':2,'Ai':r"assets/WhatsApp Image 2026-04-13 at 17.31.58 (2).jpeg",'real':r"assets/WhatsApp Image 2026-04-13 at 17.31.58 (3).jpeg",'clue':''},
        {'num':3,'Ai':r"assets/WhatsApp Image 2026-04-13 at 17.31.59.jpeg",'real':r"assets/WhatsApp Image 2026-04-13 at 17.31.59 (1).jpeg",'clue':''}]

background_view2 = r"assets/WhatsApp Image 2026-04-13 at 17.36.55.jpeg"
clue_pic = r"assets/pngtree-cute-hand-drawn-cartoon-lamp-with-yellow-light-vector-png-image_14109462.png"
# class View1(arcade.View):
#     def __init__(self):
#         super().__init__()
#         self.background = arcade.load_texture(r"assets/WhatsApp Image 2026-04-13 at 17.36.55.jpeg")
#         #start button
#         self.manager = arcade.gui.UIManager()
#         self.manager.enable()
#         start_button = arcade.gui.UIFlatButton(text='Start', width=100, height=50, style={"normal": {"bg_color": arcade.color.GREEN},"hover": {"bg_color": arcade.color.DARK_GREEN},"press": {"bg_color": arcade.color.DARK_YELLOW}})
#         start_button.center_x = SCREEN_WIDTH - 150
#         start_button.center_y = 50
#         start_button.on_click = self.continue_to_view2
#         self.manager.add(start_button)
#
#     def continue_to_view2 (self, event):
#         self.window.show_view(View2())
#
#     def on_draw(self):
#         self.clear()
#         arcade.draw_texture_rect(self.background,arcade.rect.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT))
#         arcade.draw_lbwh_rectangle_filled(0,0,SCREEN_WIDTH,100,arcade.color.DARK_BLUE)
#         arcade.draw_text(fix_hebrew(description_text_view1), SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.7,arcade.color.BLACK, 40)
#         self.manager.draw()
#
#         #להוסיף את הברוכים הבאים

class View2(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture(background_view2)

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
        arcade.draw_texture_rect(self.background,arcade.rect.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT))

        y = SCREEN_HEIGHT - 100
        paragraphs = description_text_view2.split("\n")

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
        self.player_score = 0
        self.pic_height = SCREEN_HEIGHT*0.7
        self.pic_width = SCREEN_WIDTH*0.487
        arcade.set_background_color(arcade.color.CYAN)
        arcade.AI = ''
        arcade.real = ''
        self.AI = r'assets/WhatsApp Image 2026-04-13 at 17.31.59.jpeg'
        self.real = r'assets/WhatsApp Image 2026-04-13 at 17.31.59 (1).jpeg'

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        #תמונה AI
        txture = arcade.load_texture(self.AI)
        self.AI_button = arcade.gui.UITextureButton(texture=txture,
                                               width=self.pic_width,
                                               height=self.pic_height,
                                               x= 0,
                                               y=SCREEN_HEIGHT*0.133)
        self.manager.add(self.AI_button)
        #תמונה אמיתית
        self.txture2 = arcade.load_texture(self.real)
        self.real_button = arcade.gui.UITextureButton(texture=self.txture2,
                                                    width=self.pic_width,
                                                    height=self.pic_height,
                                                    x= SCREEN_WIDTH * 0.512 ,
                                                 y= SCREEN_HEIGHT*0.133)
        self.manager.add(self.real_button)
        self.real_button.on_click = self.real_button_pressed
        self.AI_button.on_click = self.AI_button_pressed

        #רמז
        self.txture3 = arcade.load_texture(clue_pic)
        self.clue_button = arcade.gui.UITextureButton(texture=self.txture3,
                                                      width=SCREEN_WIDTH*0.04,
                                                      height=SCREEN_HEIGHT*0.03,
                                                      x= SCREEN_WIDTH*0.95,
                                                      y=SCREEN_HEIGHT*0.0333)
        self.manager.add(self.clue_button)
        self.clue_button.on_click = ''

    def clue_button_clicked(self, event):
        arcade.draw_text()

    def real_button_pressed(self, event):
        self.run_pics()
        self.clear()
        self.player_score += 1

    def AI_button_pressed(self, event):
        self.run_pics()
        self.clear()
        self.player_score -= 1

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
        arcade.draw_lrbt_rectangle_filled(SCREEN_WIDTH*0.487,SCREEN_WIDTH*0.512,SCREEN_HEIGHT*0.133,SCREEN_HEIGHT*0.833,arcade.color.BLACK)
        arcade.draw_lrbt_rectangle_filled(0,SCREEN_WIDTH,SCREEN_HEIGHT*0.1,SCREEN_HEIGHT*0.133,arcade.color.BLACK)
        arcade.draw_lrbt_rectangle_filled(0,SCREEN_WIDTH,SCREEN_HEIGHT*0.833,SCREEN_HEIGHT*0.866,arcade.color.BLACK)

        arcade.draw_text(fix_hebrew(description_text_view3),SCREEN_WIDTH*0.35,SCREEN_HEIGHT*0.9,arcade.color.BLACK,20)

        arcade.draw_text(f'score: {self.player_score}',SCREEN_WIDTH*0.025,SCREEN_HEIGHT*0.9,arcade.color.BLACK,20)
window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,'Hacaton project 2026')
window.show_view(View2())
arcade.run()