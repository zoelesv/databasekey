from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Bid,Listing,Comment,Watchlist,Closedbid,Alllisting
from datetime import datetime
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm

#show all active listings
def index(request):
    items = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "items": items
    })

#create listing
def create(request):
    # for a POST method, add a new list in Listing
    if request.method == "POST":
        listtable = Listing()
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        listtable.owner = request.user
        listtable.title = request.POST.get('title')
        listtable.description = request.POST.get('description')
        listtable.price = request.POST.get('price')
        listtable.category = request.POST.get('category')
        if request.POST.get('link'):
            listtable.link = request.POST.get('link')
        else:
            listtable.link = "https://wallpaperaccess.com/full/1605486.jpg"
        listtable.time = dt
        listtable.save()
        all = Alllisting()
        items = Listing.objects.all()
        for i in items:
            try:
                if Alllisting.objects.get(listingid=i.id):
                    pass
            except:
                all.listingid = i.id
                all.title = i.title
                all.description = i.description
                all.link = i.link
                all.save()

        return redirect('index')
    # If the form is invalid, re-render the page with existing information.
    else:
        return render(request, "auctions/create.html")

# display all detail about the listing with id
def listingpage(request,id):
    try:
        item = Listing.objects.get(id=id)
    except:
        return redirect('index')
    try:
        comments = Comment.objects.filter(listingid=id)
    except:
        comments = None
    if request.user.username:
        try:
            if Watchlist.objects.get(user=request.user.username,listingid=id):
                added=True
        except:
            added = False
        try:
            l = Listing.objects.get(id=id)
            if l.owner == request.user.username :
                owner=True
            else:
                owner=False
        except:
            return redirect('index')
    else:
        added=False
        owner=False

    return render(request,"auctions/listingpage.html",{
        "item":item,
        "error":request.COOKIES.get('error'),
        "errorgreen":request.COOKIES.get('errorgreen'),
        "comments":comments,
        "added":added,
        "owner":owner
    })



# for POST method add bid information to Bid
def bidsubmit(request, listingid):
    current_bid = Listing.objects.get(id=listingid)
    current_bid = current_bid.price
    #check if method is post, get the input -> add to table
    if request.method == "POST":
        user_bid = int(request.POST.get("bid"))
        if user_bid > current_bid:
            listing_items = Listing.objects.get(id=listingid)
            listing_items.price = user_bid
            listing_items.save()
            try:
                if Bid.objects.filter(id=listingid):
                    bidrow = Bid.objects.filter(id=listingid)
                    bidrow.delete()
                bidtable = Bid()
                bidtable.user = request.user.username
                bidtable.title = listing_items.title
                bidtable.listingid = listingid
                bidtable.bid = user_bid
                bidtable.save()

            except:
                bidtable = Bid()
                bidtable.user = request.user.username
                bidtable.title = listing_items.title
                bidtable.listingid = listingid
                bidtable.bid = user_bid
                bidtable.save()
            response = redirect('listingpage', id=listingid)
            response.set_cookie('errorgreen', 'bid successful!!!', max_age=3)
            return response
        else:
            response = redirect('listingpage', id=listingid)
            response.set_cookie('error', 'Bid should be greater than current price', max_age=3)
            return response
    else:
        return redirect('index')


# for POST method add comments information to comment
def cmntsubmit(request, listingid):
    if request.method == "POST":
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        c = Comment()
        c.comment = request.POST.get('comment')
        c.user = request.user.username
        c.time = dt
        c.listingid = listingid
        c.save()
        return redirect('listingpage', id=listingid)
    else:
        return redirect('index')

#Add watchlist
def addwatchlist(request, listingid):
    if request.user.username:
        w = Watchlist()
        w.user = request.user.username
        w.listingid = listingid
        w.save()
        return redirect('listingpage', id=listingid)
    else:
        return redirect('index')

#Remove watchlist
def removewatchlist(request, listingid):
    if request.user.username:
        try:
            w = Watchlist.objects.get(user=request.user.username, listingid=listingid)
            w.delete()
            return redirect('listingpage', id=listingid)
        except:
            return redirect('listingpage', id=listingid)
    else:
        return redirect('index')

#show all listing on watchlist
def watchlistpage(request, username):
    if request.user.username:
        try:
            w = Watchlist.objects.filter(user=username)
            items = []
            for i in w:
                items.append(Listing.objects.filter(id=i.listingid))
            return render(request, "auctions/watchlistpage.html", {
                "items": items
            })
        except:
            try:
                w = Watchlist.objects.filter(user=request.user.username)
                wcount = len(w)
            except:
                wcount = None
            return render(request, "auctions/watchlistpage.html", {
                "items": None,
                "wcount": wcount
            })
    else:
        return redirect('index')

#close bid
def closebid(request, listingid):
    if request.user.username:
        try:
            listingrow = Listing.objects.get(id=listingid)
        except:
            return redirect('index')
        cb = Closedbid()
        title = listingrow.title
        cb.owner = listingrow.owner
        cb.listingid = listingid
        try:
            bidrow = Bid.objects.get(listingid=listingid, bid=listingrow.price)
            cb.winner = bidrow.user
            cb.winprice = bidrow.bid
            cb.save()
            bidrow.delete()
        except:
            cb.winner = listingrow.owner
            cb.winprice = listingrow.price
            cb.save()
        try:
            if Watchlist.objects.filter(listingid=listingid):
                watchrow = Watchlist.objects.filter(listingid=listingid)
                watchrow.delete()
            else:
                pass
        except:
            pass
        try:
            brow = Bid.objects.filter(listingid=listingid)
            brow.delete()
        except:
            pass
        try:
            cblist = Closedbid.objects.get(listingid=listingid)
        except:
            cb.owner = listingrow.owner
            cb.winner = listingrow.owner
            cb.listingid = listingid
            cb.winprice = listingrow.price
            cb.save()
            cblist = Closedbid.objects.get(listingid=listingid)
        listingrow.delete()

        return render(request, "auctions/winningpage.html", {
            "cb": cblist,
            "title": title
        })

    else:
        return redirect('index')

#show all listings that were closed.
def closedlisting(request):
    items = []
    try:
        wonitems = Closedbid.objects.all()
        for w in wonitems:
            items.append(Alllisting.objects.filter(listingid=w.listingid))
    except:
        wonitems = None
        items = None
    return render(request, 'auctions/closedlisting.html', {
        "items": items,
        "wonitems": wonitems
        })

# show closed listing page
def closedlistingpage(request,id):
    closedbid = Closedbid.objects.get(listingid=id)
    item = Alllisting.objects.get(id=id)
    try:
        comments = Comment.objects.filter(listingid=id)
    except:
        comments = None

    return render(request,"auctions/closedlistingpage.html",{
        "item":item,
        "closedbid": closedbid,
        "comments":comments
    })

# show all categories available for active listing
def categories(request):
    items=Listing.objects.raw("SELECT * FROM auctions_listing GROUP BY category")

    return render(request,"auctions/categpage.html",{
        "items": items,
    })


def category(request,category):
    items = Listing.objects.filter(category=category)

    return render(request,"auctions/category.html",{
        "items":items,
        "cat":category
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


class register(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("index")
    template_name = "auctions/register.html"