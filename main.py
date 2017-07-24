import webbrowser

from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

apiKey = 'd92fed2550c9424dac2967cb2b6da249'
url = "https://newsapi.org/v1/articles?source={}&sortBy=top&apiKey={}"

news = {}

source = None
article = None

sm = ScreenManager()


class LastScreen(Screen):
    def __init__(self, **kwargs):
        super(LastScreen, self).__init__(**kwargs)

        boxLayout = BoxLayout(orientation='vertical')
        for k, v in news[source].items():
            if article == k:
                button = Label(text=v['title'])
                boxLayout.add_widget(button)
                img = AsyncImage(source=v['urlToImage'], height=100)
                boxLayout.add_widget(img)
                button1 = Label(text=v['description'])
                boxLayout.add_widget(button1)
                try:
                    button2 = Label(text=v['author'])
                except ValueError:
                    button2 = Label(text='Without author')
                boxLayout.add_widget(button2)
                button3 = Button(text=v['url'], on_press=lambda a: webbrowser.open(v['url']))
                boxLayout.add_widget(button3)
        button4 = Button(text='Back', on_press=lambda a: self.open_screen())
        boxLayout.add_widget(button4)
        self.add_widget(boxLayout)

    def open_screen(self):
        self.manager.current = 'second_screen'


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)

        self.clear_widgets()
        gridLayout = GridLayout(cols=3)
        for k, v in news[source].items():
            button1 = Button(text=v['title'], size_hint_x=60, on_press=lambda a: self.open_lastscreen(k))
            gridLayout.add_widget(button1)
            img = AsyncImage(source=v['urlToImage'], size_hint_x=20)
            gridLayout.add_widget(img)
            try:
                button2 = Button(text=v['author'], size_hint_x=20)
            except ValueError:
                button2 = Button(text='Without author', size_hint_x=20)
            gridLayout.add_widget(button2)

        button = Button(text='Back', on_press=lambda a: self.open_screen())
        gridLayout.add_widget(button)
        self.add_widget(gridLayout)

    def open_screen(self):
        sm.add_widget(FirstScreen(name='first_screen'))
        self.manager.current = 'first_screen'

    def open_lastscreen(self, key):
        global article
        article = key
        sm.add_widget(LastScreen(name='last_screen'))
        self.manager.current = 'last_screen'


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)

        layout = GridLayout(cols=3)

        for s in ['bbc-news', 'bild', 'bloomberg']:
            self.req(s)

        button1 = Button(text='BBC News', size_hint_x=20, on_press=lambda a: self.open_screen('bbc-news'))
        button2 = Button(text='Is an operational business division of the British Broadcasting\n'
                              'Corporation (BBC) responsible for the gathering and broadcasting\n'
                              'of news and current affairs.', size_hint_x=60)
        button3 = Button(text='http://www.bbc.com/',
                         size_hint_x=20, on_press=lambda a: webbrowser.open('http://www.bbc.com/'))
        button4 = Button(text='Bild', size_hint_x=20, on_press=lambda a: self.open_screen('bild'))
        button5 = Button(text='The newspaper is a German tabloid published by Axel Springer AG.\n'
                              'The paper is published from Monday to Saturday.', size_hint_x=60)
        button6 = Button(text='http://www.bild.de/', size_hint_x=20,
                         on_press=lambda a: webbrowser.open('http://www.bild.de/'))
        button7 = Button(text='Bloomberg', size_hint_x=20, on_press=lambda a: self.open_screen('bloomberg'))
        button8 = Button(text='Is an international news agency headquartered in New York,\n'
                              'United States and a division of Bloomberg L.P.', size_hint_x=60)
        button9 = Button(text='https://www.bloomberg.com/', size_hint_x=20,
                         on_press=lambda a: webbrowser.open('https://www.bloomberg.com/'))

        for but in [button1, button2, button3, button4, button5, button6, button7, button8, button9]:
            layout.add_widget(but)

        self.add_widget(layout)

    def open_screen(self, key):
        global source
        source = key
        sm.add_widget(SecondScreen(name='second_screen'))
        self.manager.current = 'second_screen'

    def req(self, key):
        self.request = UrlRequest(url.format(key, apiKey), self.res)

    def res(self, request, data):
        count = 0
        n = {}
        for d in data['articles']:
            n.update({count: {
                'title': d['title'],
                'description': d['description'],
                'author': d['author'],
                'url': d['url'],
                'urlToImage': d['urlToImage'],
            }
            })
            count += 1
        news.update({
            data['source']: n
        })


class NewsApp(App):
    def build(self):
        sm.add_widget(FirstScreen(name='first_screen'))
        return sm


if __name__ == '__main__':
    NewsApp().run()
