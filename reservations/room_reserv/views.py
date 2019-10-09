from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from room_reserv.models import *
from datetime import date

today = str(date.today())


class AllRooms(View):
    def get(self, request):
        rooms = Room.objects.all().order_by('id')
        today_reservations = Reservation.objects.filter(reservation_date__contains=today)
        id_list = [reservation.rooms_id for reservation in today_reservations]
        reserved = "".join([f"<tr><td>{room.name}</td></tr>" for room in rooms if room.id in id_list])
        room_list = "".join([f"<tr><td><a href='/room/{room.id}'>{room.name}</a></td>"
                             f"<td><sub><a href='/room/modify/{room.id}'>edytuj</a></sub></td>"
                             f"<td><sub><a href='/room/delete/{room.id}'>usuń</a></sub></td></tr>" for room in rooms])
        return render(request, "index.html", context={'room_list': room_list, 'reserved': reserved, 'today': today})


def room_search(request):
    name = request.GET.get('name')
    if request.GET.get('capacity') != '':
        capacity = request.GET.get('capacity')
    else:
        capacity = 1

    if request.GET.get('reservation_date') != '':
        reservation_date = request.GET.get('reservation_date')
    else:
        reservation_date = today
    projector = request.GET.get('projector')
    rooms = Room.objects.filter(name__icontains=name).filter(capacity__gte=capacity).filter(projector=projector)
    reservation_list = [reservation.rooms_id for reservation in
                        Reservation.objects.filter(reservation_date=reservation_date)]
    result = "".join([f'<li>sala: <a href="/room/{room.id}">{room.name}</a></li>' for room in rooms if
                      room.id not in reservation_list])
    if result == "":
        return render(request, 'search.html',
                      context={'room_list': 'Brak wolnych sal dla podanych kryteriów wyszukiwania'})
    return render(request, 'search.html', context={'room_list': result, 'reservation_date': reservation_date})


class AddRoom(View):
    def get(self, request):
        return render(request, "addroom.html", context={'info': 'Dodaj nową salę'})

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')
        if name and capacity and (projector == 'True' or projector == 'False'):
            new_room = Room.objects.create(name=name, capacity=capacity, projector=projector)
            return redirect(f'/room/{new_room.id}')
        return render(request, 'addroom.html', context={'info': 'Błędne dane, spróbuj jeszcze raz.'})


class RoomDetails(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        reservations = Reservation.objects.filter(rooms=room).filter(reservation_date__gte=today).order_by(
            'reservation_date')
        if room.projector:
            projector = 'Dostępny'
        else:
            projector = 'Brak'
        reservation_list = ''.join([f'<li>{reservation.reservation_date}</li>' for reservation in reservations])

        return render(request, 'roomdetails.html',
                      context={'name': room.name, 'capacity': room.capacity, 'projector': projector,
                               'reservation_list': reservation_list, 'room_id': room_id, 'today': today})

    def post(self, request, room_id):
        reservation_date = request.POST.get('reservation_date')
        comment = request.POST.get('comment')
        rooms = Room.objects.get(id=room_id)
        try:
            Reservation.objects.create(reservation_date=reservation_date, comment=comment, rooms=rooms)
        except IntegrityError:
            return render(request, 'reservation.html',
                          context={'info': 'Sala jest już zarezerwowana w tym dniu', 'back': f'/room/{room_id}'})
        else:
            return render(request, 'reservation.html', context={'info': 'Sala zarezerwowana', 'back': '/'})


class EditRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        return render(request, 'editroom.html', context={'info': f"Zmień informację o sali",
                                                         'room_name': Room.objects.get(id=room_id).name})

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        room.name = request.POST.get('name')
        room.capacity = request.POST.get('capacity')
        room.projector = request.POST.get('projector')
        room.save()
        if room.projector == "True":
            projector = 'Dostępny'
        else:
            projector = 'Niedostępny'
        return render(request, 'editroom_ok.html', context={'info': 'Dane sali zmienione', 'room_name': room.name,
                                                            'room_capacity': room.capacity,
                                                            'room_projector': projector})


class DeleteRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        return render(request, "deleteroom.html", context={'info': 'Usuń salę', 'room_name': room.name})

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        if request.POST.get('delete') == 'Tak':
            room.delete()
            return render(request, 'deleteroom_ok.html', context={'info': 'Sala usunięta'})
        return redirect('/')
