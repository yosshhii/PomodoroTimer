from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.utils import get_color_from_hex

Builder.load_file("C:\\Users\\blood\\Desktop\\kivygui\\programms\\PomodoroTimer\\pomodoro.kv")
Window.size = 600, 600


class ProgramLayout(Widget):
    pomodoro = 25 * 60
    short_break = 5 * 60
    long_break = 15 * 60
    timer_status = None
    current_time = pomodoro
    session_counter = 1
    work_status = True

    @staticmethod
    def format_time(time):
        minutes, seconds = time // 60, time % 60
        return f'{minutes:02}:{seconds:02}'

    def start_timer(self):
        self.timer_status = Clock.schedule_interval(self.update_timer, 1)
        self.ids.toggle_button.text = 'PAUSE'

    def stop_timer(self):
        self.timer_status.cancel()
        self.timer_status = None
        self.ids.toggle_button.text = 'START'

    def toggle_status(self):
        if not self.timer_status:
            self.start_timer()
        else:
            self.stop_timer()

    def update_timer(self, instance):
        if self.current_time > 0:
            self.current_time -= 1
            self.ids.time.text = self.format_time(self.current_time)
        else:
            self.stop_timer()
            self.switch_status()

    def switch_status(self):
        if self.work_status:
            self.work_status = not self.work_status
            self.toggle_button_style(0, False)
            if self.session_counter % 4 == 0:
                self.current_time = self.long_break
                self.toggle_button_style(2, True)
            else:
                self.current_time = self.short_break
                self.toggle_button_style(1, True)
        else:
            self.session_counter += 1
            self.work_status = not self.work_status
            self.current_time = self.pomodoro
            self.toggle_button_style(2, False)
            self.toggle_button_style(1, False)
            self.toggle_button_style(0, True)

        self.ids.time.text = self.format_time(self.current_time)

    def toggle_button_style(self, index, toggle_to):
        buttons = [self.ids.first_button, self.ids.second_button, self.ids.third_button]
        button = buttons[index].canvas.before.children
        if toggle_to:
            self.animate_button(button, get_color_from_hex('365E32'))
            button[2].pos = buttons[index].center_x - buttons[index].width / 2, buttons[index].center_y - buttons[index].height * 0.5 / 2
            button[2].size = buttons[index].width, buttons[index].height * 0.5
            button[2].radius = [14]
        else:
            self.animate_button(button, (0, 0, 0, 0))
        buttons[index].bold = toggle_to

    @staticmethod
    def animate_button(button, color):
        animation = Animation(rgba=color, duration=0.15)
        animation.start(button[0])


class PomodoroApp(App):
    def build(self):
        Window.clearcolor = '508D4E'
        return ProgramLayout()


if __name__ == '__main__':
    PomodoroApp().run()



