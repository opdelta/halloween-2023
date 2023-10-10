from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
import datetime
from django.conf import settings
from countdown.models import Countdown
from django.db.utils import IntegrityError
# Create your views here.
def countdown_view(request):
    return render(request, 'countdown.html')

def get_target_date(request):
    # Retrieve the target date from the database
    target = get_object_or_404(Countdown, id=2)

    # Return the target date as a JSON response
    return JsonResponse({'target_date': target.target_date})

def add_time(request, number, time_indicator, target_id=None):
    # Convert the number to an integer
    try:
        number = int(number)
    except ValueError:
        return JsonResponse({'error': 'Invalid number'}, status=400)

    # Define a dictionary to map time indicators to seconds
    time_mapping = {
        's': 1,  # seconds
        'm': 60,  # minutes
        'h': 3600,  # hours
    }

    # Check if the time indicator is valid
    if time_indicator not in time_mapping:
        return JsonResponse({'error': 'Invalid time indicator'}, status=400)

    # Calculate the added time in seconds
    added_time_seconds = number * time_mapping[time_indicator]

    try:
        # Retrieve the target date for id=2
        target = Countdown.objects.get(id=2)

        # Update the target date by adding the specified time
        target.target_date += datetime.timedelta(seconds=added_time_seconds)

        # Save the updated target date
        target.save()

        return JsonResponse({'message': f'Added {number}{time_indicator} to the time'})
    except Countdown.DoesNotExist:
        return JsonResponse({'error': 'Target with id=2 not found'}, status=404)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def remove_time(request, number, time_indicator, target_id=None):
    # Convert the number to an integer
    try:
        number = int(number)
    except ValueError:
        return JsonResponse({'error': 'Invalid number'}, status=400)

    # Define a dictionary to map time indicators to seconds
    time_mapping = {
        's': 1,  # seconds
        'm': 60,  # minutes
        'h': 3600,  # hours
    }

    # Check if the time indicator is valid
    if time_indicator not in time_mapping:
        return JsonResponse({'error': 'Invalid time indicator'}, status=400)

    # Calculate the removed time in seconds
    removed_time_seconds = number * time_mapping[time_indicator]

    try:
        # Retrieve the target date for id=2
        target = Countdown.objects.get(id=2)

        # Update the target date by subtracting the specified time
        target.target_date -= datetime.timedelta(seconds=removed_time_seconds)

        # Save the updated target date
        target.save()

        return JsonResponse({'message': f'Removed {number}{time_indicator} from the time'})
    except Countdown.DoesNotExist:
        return JsonResponse({'error': 'Target with id=2 not found'}, status=404)
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=400)
def reset_target_date(request):
    try:
        # Get the existing target date record or create a new one if it doesn't exist
        target, created = Countdown.objects.get_or_create(id=2)

        # Update the target date for October 28th 2023 at 23:00:00
        target.target_date = datetime.datetime(2023, 10, 28, 23, 0, 0)
        target.save()

        return JsonResponse({'message': f'Reset target date to {target.target_date}'})
    except IntegrityError as e:
        return JsonResponse({'error': str(e)}, status=400)