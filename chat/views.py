'''
    Chat Application View
    '''
from django.shortcuts import render
from django.views.generic import DetailView
from chat.models import Room, Message


def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })


class RoomView(DetailView):
    model = Room
    template_name: str = ''

    def get(self, request, *args, **kwargs):
        chat_room, created = Room.objects.get_or_create(
            name=kwargs.get('room_name'))
        chat_messages = Message.objects.filter(room=chat_room)[0:25]
        return render(request, self.template_name, {
            'room_name': chat_room,
            'chat_messages': chat_messages
        })
