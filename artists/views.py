from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import AuditLog
from .models import Artist
from .forms import ArtistForm
from django.contrib import messages
from accounts.decorators import role_required
from .forms import ArtistProfileForm
from django.db.models import Q
from django.core.paginator import Paginator
from core.utils import log_action

@login_required
@role_required(['admin', 'director','coach'])
def artist_list(request):

    query = request.GET.get('q')

    artists = Artist.objects.all()

    if query:

        artists = artists.filter(

            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(dance_style__icontains=query)

        )

    paginator = Paginator(artists, 5)

    page_number = request.GET.get('page')

    artists = paginator.get_page(page_number)

    return render(request, 'artists/artist_list.html', {
        'artists': artists
    })


@login_required
@role_required(['admin','coach'])
def add_artist(request):

    if request.method == 'POST':

        form = ArtistForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request,'Artist added successfully.')

            log_action(
            request.user,
            "ARTIST_CREATED",
            f"Artist created: {form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
            )

            return redirect('artist_list')

    else:
        form = ArtistForm()

    return render(request, 'artists/add_artist.html', {
        'form': form
    })


@login_required
@role_required(['admin','coach'])
def edit_artist(request, pk):

    artist = get_object_or_404(Artist, id=pk)

    if request.method == 'POST':

        form = ArtistForm(request.POST, instance=artist)

        if form.is_valid():

            form.save()

            messages.success(request,'Artist updated successfully.')

            log_action(
            request.user,
            "ARTIST_UPDATED",
            f"Artist ID {artist.id} updated"
            )

            return redirect('artist_list')

    else:
        form = ArtistForm(instance=artist)

    return render(request, 'artists/edit_artist.html', {
        'form': form
    })


@login_required
@role_required(['admin'])
def delete_artist(request, pk):

    artist = get_object_or_404(Artist, id=pk)

    artist.delete()

    log_action(
    request.user,
    "ARTIST_DELETED",
    f"Artist deleted: {artist.first_name} {artist.last_name} (ID {artist.id})"
    )

    messages.success(request,'Artist deleted successfully.')

    return redirect('artist_list')

@login_required
@role_required(['artist'])
def my_profile(request):

    artist = getattr(request.user, 'artist', None)

    if not artist:
        return redirect('/dashboard/')

    return render(
        request,
        'artists/my_profile.html',
        {
            'artist': artist
        }
    )

@login_required
@role_required(['artist'])
def edit_my_profile(request):

    artist = request.user.artist

    if request.method == 'POST':

        form = ArtistProfileForm(
            request.POST,
            request.FILES,
            instance=artist
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Profile updated successfully.'
            )

            log_action(
            request.user,
            "PROFILE_UPDATED",
            "Artist updated their own profile"
            )

            return redirect('my_profile')

    else:

        form = ArtistProfileForm(
            instance=artist
        )

    return render(
        request,
        'artists/edit_my_profile.html',
        {
            'form': form
        }
    )