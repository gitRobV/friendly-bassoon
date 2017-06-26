
if len(validated['errors']) > 0:
    messages.error(request, "Hol'up, Try that shit again.")
    for err in validated['errors']:
        messages.error(request, err)
    return redirect('/login')
else:
    print validated['errors']
    request.session['user_id'] = validated['data']['id']
    messages.success(request, 'You have successfully logged in!')
    return redirect('/')
else:
return redirect('/login')













# if len(auth_input.errors) == 0:
#     try:
#         check_user = User.objects.get(email=auth_input.data['email'])
#     except:
#         check_user = False
#     if check_user:
#         pw_attempt = auth_input.data['password']
#         print pw_attempt
#         hashed_pw = check_user.password
#         print hashed_pw
#         if
#             auth_attempt = {
#                 'data': {
#                     'id': check_user.id,
#                     'email': check_user.email,
#                     'status': 'Authenticated'
#                 },
#                 'errors': []
#             }
#         else:
#             auth_attempt = {
#                 'data': auth_input.data,
#                 'errors': ['Password combination did not match our records. Please try again.']
#             }
#     else:
#         auth_attempt = {
#             'data': auth_input.data,
#             'errors': ['Email combination did not match our records. Please try again.']
#         }
# else:
#     auth_attempt = {
#         'data': auth_input.data,
#         'errors': auth_input.data
#     }
# return auth_attempt
