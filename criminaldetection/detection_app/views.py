from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from detection_app.forms import LoginForm, LoginUpdate, PoliceForm, PoliceUpdate, CriminalForm, MissingForm
from detection_app.models import Login, Criminaldata, Missingdata


def index(request):
    return render(request, 'index.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_home')
            elif user.is_state:
                return redirect('state')
            elif user.is_police:
                return redirect('police')
            elif user.is_user:
                return redirect('user_home')
        else:
            messages.info(request, 'INVALID CREDENTIALS')
    return render(request, 'signin.html')


def sign_out(request):
    logout(request)
    return redirect('index')


def sign_up(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_user = True
            user.save()
            messages.info(request, 'state registered successful')
            return redirect('sign_in')
    return render(request, 'signup.html', {'form': form})


####################ADMINPANEL###########

def admin_home(request):
    return render(request, 'admintemp/index.html')


def state_register(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_state = True
            user.save()
            messages.info(request, 'state registered successful')
            return redirect('state_view')
    return render(request, 'admintemp/state_register.html', {'form': form})


def state_view(request):
    s = Login.objects.filter(is_state=True)
    return render(request, 'admintemp/state_view.html', {'s': s})


def state_update(request, id):
    s = Login.objects.get(id=id)
    form = LoginUpdate(instance=s)
    if request.method == 'POST':
        form = LoginUpdate(request.POST or None, instance=s)
        if form.is_valid():
            form.save()
            messages.info(request, 'state updated successful')
            return redirect('state_view')
    return render(request, 'admintemp/state_update.html', {'form': form})


def state_delete(request, id):
    s = Login.objects.get(id=id)
    if request.method == 'POST':
        s.delete()
        return redirect('state_view')
    else:
        return redirect('state_view')


def police_view_admin(request):
    p = Login.objects.filter(is_police=True)
    return render(request, 'admintemp/police_view.html', {'p': p})


def criminal_records(request):
    c = Criminaldata.objects.all()
    return render(request, 'admintemp/criminal.html', {'c': c})


def crimegraph(request):
    return render(request, 'admintemp/crime_st.html')

def detect_admin(request):
    import time

    import cv2
    import numpy as np
    import face_recognition
    import os

    path = 'media/criminal_data'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    print(type(classNames))

    def findEncodings(images):
        encodeList = []

        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        # img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            print(matchIndex)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                # if (label == 0):
                #     num = 'MY'
                #     value = write_read(num)
                #     break
                # elif (label == 1):
                #     num = 'NM'
                #     value = write_read(num)
                #     break

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord("q"):
            return redirect("admin_home")
            break
    return render(request,'admintemp/detect.html')

def detection_admin(request):
    return render(request, 'admintemp/detection.html')


####################STATEPANEL###########

def state(request):
    return render(request, 'statetemp/index.html')


def police_register(request):
    form = PoliceForm()
    if request.method == 'POST':
        form = PoliceForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_police = True
            user.save()
            messages.info(request, 'police registered successful')
            return redirect('police_view')
    return render(request, 'statetemp/police_register.html', {'form': form})


def police_view(request):
    p = Login.objects.filter(is_police=True)
    return render(request, 'statetemp/police_view.html', {'p': p})


def police_delete(request, id):
    p = Login.objects.get(id=id)
    if request.method == 'POST':
        p.delete()
        return redirect('police_view')
    else:
        return redirect('police_view')


##################POLICEPANEL###########

def police(request):
    return render(request, 'policetemp/index.html')


def profile(request):
    p = Login.objects.filter(username=request.user)
    return render(request, 'policetemp/profile.html', {'p': p})


def profile_edit(request, id):
    p = Login.objects.get(id=id)
    form = PoliceForm(instance=p)
    if request.method == 'POST':
        form = PoliceForm(request.POST or None, instance=p)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'policetemp/profile_edit.html', {'form': form})


def criminal_add(request):
    form = CriminalForm()
    if request.method == 'POST':
        form = CriminalForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            messages.info(request, 'criminaldata added Successful')
            return redirect('criminal')
    return render(request, 'policetemp/criminal_add.html', {'form': form})


def criminal(request):
    c = Criminaldata.objects.all()
    return render(request, 'policetemp/criminal.html', {'c': c})


def criminal_update(request, id):
    c = Criminaldata.objects.get(id=id)
    form = CriminalForm(instance=c)
    if request.method == 'POST':
        form = CriminalForm(request.POST or None, request.FILES or None, instance=c)
        if form.is_valid():
            form.save()
            messages.info(request, 'Criminal updated successful')
            return redirect('criminal')
    return render(request, 'policetemp/criminal_update.html', {'form': form})


def criminal_delete(request, id):
    c = Criminaldata.objects.get(id=id)
    if request.method == 'POST':
        c.delete()
        return redirect('criminal')
    else:
        return redirect('criminal')


def missing_add(request):
    form = MissingForm()
    if request.method == 'POST':
        form = MissingForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            messages.info(request, 'Missing Person added Successful')
            return redirect('missing')
    return render(request, 'policetemp/missing_add.html', {'form': form})


def missing(request):
    m = Missingdata.objects.all()
    return render(request, 'policetemp/missing.html', {'m': m})


def missing_update(request, id):
    c = Missingdata.objects.get(id=id)
    form = MissingForm(instance=c)
    if request.method == 'POST':
        form = MissingForm(request.POST or None, request.FILES or None, instance=c)
        if form.is_valid():
            form.save()
            messages.info(request, 'Missing Person Detail updated successful')
            return redirect('missing')
    return render(request, 'policetemp/missing_update.html', {'form': form})


def missing_delete(request, id):
    m = Missingdata.objects.get(id=id)
    if request.method == 'POST':
        m.delete()
        return redirect('missing')
    else:
        return redirect('missing')


##################USERPANEL###########

def user_home(request):
    return render(request, 'usertemp/index.html')

def detect(request):
    import time

    import cv2
    import numpy as np
    import face_recognition
    import os

    path = 'media/criminal_data'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    print(type(classNames))

    def findEncodings(images):
        encodeList = []

        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        # img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            print(matchIndex)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                # if (label == 0):
                #     num = 'MY'
                #     value = write_read(num)
                #     break
                # elif (label == 1):
                #     num = 'NM'
                #     value = write_read(num)
                #     break

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord("q"):
            return redirect("user_home")
            break
    return render(request,'usertemp/detect.html')


def detection_panel(request):
    return render(request, 'usertemp/detection.html')