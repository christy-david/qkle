# from django.shortcuts import render,get_object_or_404,redirect
# from listing.models import Vehicle
# from .models import Chat
# from.forms import ChatMessageForm
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import never_cache

# @never_cache
# @login_required
# def new_chat(request,vehicle_pk):
#   vehicle = get_object_or_404(vehicle, pk=vehicle_pk)

#   if vehicle.sold_by == request.user:
#         return redirect('user_profile:user-listings')
    
#   chats = Chat.objects.filter(vehicle=vehicle).filter(members__in=[request.user.id])

#   if chats:
#         return redirect('chat:detail', pk=chats.first().id)

#   if request.method == 'POST':
#         form = ChatMessageForm(request.POST)

#         if form.is_valid():
#             chat = Chat.objects.create(vehicle=vehicle)
#             chat.members.add(request.user)
#             chat.members.add(vehicle.sold_by)
#             chat.save()

#             chat_message = form.save(commit=False)
#             chat_message.conversation = chat
#             chat_message.created_by = request.user
#             chat_message.save()

#             return redirect('listing:details', pk=vehicle_pk)
#   else:
#       form = ChatMessageForm()
    
#   return render(request, 'chat/new.html', {
#         'form': form
#   })
  




from django.shortcuts import render, get_object_or_404, redirect
from listing.models import Vehicle
from .models import Chat
from .forms import ChatMessageForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def new_chat(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)

    if vehicle.sold_by == request.user:
        return redirect('user_profile:user-listings')

    chats = Chat.objects.filter(vehicle=vehicle).filter(members__in=[request.user.id])

    if chats.exists():
        # Redirect to an existing chat
        chat = chats.first()
        return redirect('chat:detail', pk=chat.id)  # Use 'pk' instead of 'chat_id'

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)

        if form.is_valid():
            chat = Chat.objects.create(vehicle=vehicle)
            chat.members.add(request.user)
            chat.members.add(vehicle.sold_by)
            chat.save()

            chat_message = form.save(commit=False)
            chat_message.chat = chat
            chat_message.created_by = request.user
            chat_message.save()

            return redirect('listing:details', pk=vehicle_pk)
    else:
        form = ChatMessageForm()

    return render(request, 'chat/new.html', {'form': form})

@never_cache
@login_required
def inbox(request):
    chats = Chat.objects.filter(members__in=[request.user.id])

    return render(request, 'chat/inbox.html', {
        'chats': chats
    })

@never_cache
@login_required
def detail(request, pk):
    chat = get_object_or_404(Chat, members__in=[request.user.id], pk=pk)

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)

        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.chat = chat  # Set the chat field to the Chat object
            chat_message.created_by = request.user
            chat_message.save()

            # Additional logic as needed

            return redirect('chat:detail', pk=pk)
    else:
        form = ChatMessageForm()

    return render(request, 'chat/detail.html', {
        'chat': chat,
        'form': form
    })
