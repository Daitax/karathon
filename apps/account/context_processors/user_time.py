def time(request):
    participant_time = request.user.participant.get_participant_time()
    return {"user_time": participant_time}